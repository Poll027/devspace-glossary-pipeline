#!/usr/bin/env python3
"""Run a whole glossary batch unattended on AWS Bedrock: the orchestrator from START_HERE.md as a program.

    python3 run_pipeline.py batches/<batch_id> [--max-usd 300] [--plan] [--no-push]

Walks pipeline_manifest.json. A stage already gated PASS on disk (ledger hash matches) is skipped, so a
rerun resumes. Script stages run their RUN.md command. Generator/evaluator stages fan out over chunks
(canary first, then CHUNK_WORKERS in parallel, default 2), with mechanical checks before any evaluator call, an evaluator pass,
up to 3 repair rounds, then merge + gate. Stage 08/09 (detect + judge) run together per chunk.
Stops (exit 2, writes working/DRIVER_STOPPED.md, SNS if SNS_TOPIC_ARN is set) on: 3 failed rounds, a blocking
leakage/audit result, a failed script, or the spend cap. Fix the cause and rerun the same command.

Env: GEN_MODEL_ID (default Sonnet 4.6 profile), EVAL_MODEL_ID (default Opus 4.6 profile), MAX_USD, SNS_TOPIC_ARN, AWS_REGION.
# ponytail: sequential stages, chunk-level parallelism of 3; multi-path batches need an explicit chunks.json;
# a blocking stage-13 leakage result stops for a human instead of auto-routing the fix to stage 05/09/11.
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_ledger as UL  # noqa: E402
from bedrock_agent import Budget, BudgetExceeded, run_agent  # noqa: E402
from glm_generate import CORE, ROOT, ladder, load, load_env  # noqa: E402

SCRIPTS = CORE / "scripts"
TEMPLATE = ROOT / "01_GLOSSARY_PACK_TEMPLATE"
CONCEPT_CHUNKED = {"03_coverage_brief", "05_glossary_pass_a", "06_video_candidates", "11_reconciliation", "13_leakage_check"}
VIDEO_CHUNKED = {"08_segment_detection", "09_segment_judge"}
MIN_FANOUT = 150  # START_HERE: fan out from 150 concepts
MAX_ROUNDS = 3
VERDICT = re.compile(r"VERDICT:\s*(PASS_WITH_NONBLOCKING_CHANGES|PASS|FAIL)")


class Stuck(Exception):
    pass


class Ctx:
    def __init__(self, B, args):
        self.B, self.args = B, args
        self.id = B.name
        # None = use that role's model ladder (glm_generate.ladder); set GEN_MODEL_ID / EVAL_MODEL_ID to pin one model
        self.gen_pin, self.ev_pin = os.environ.get("GEN_MODEL_ID"), os.environ.get("EVAL_MODEL_ID")
        (B / "working").mkdir(exist_ok=True)
        self.budget = Budget(args.max_usd, B / "working" / "cost_log.jsonl")
        self.manifest = load(CORE / "pipeline_manifest.json")
        self.stage = {s["id"]: s for s in self.manifest["stages"]}
        self.env = {**os.environ, "PATH": f"{Path(sys.executable).parent}:{os.environ['PATH']}"}
        if self.gen_pin:
            self.env["GLM_MODEL_ID"] = self.gen_pin

    def _used(self, evaluator):
        """Models that actually ran for this role, from the cost log (the ladder may have fallen back); else the ladder head."""
        ms = set()
        try:
            for ln in open(self.B / "working" / "cost_log.jsonl"):
                m = json.loads(ln)["model"]
                if ("opus" in m) == evaluator:
                    ms.add(m)
        except FileNotFoundError:
            pass
        return ",".join(sorted(ms)) or ladder("EVAL" if evaluator else "GEN")[0]

    @property
    def gen(self):
        return self.gen_pin or self._used(False)

    @property
    def ev(self):
        return self.ev_pin or self._used(True)

    def log(self, msg):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
        print(line, flush=True)
        with open(self.B / "working" / "driver.log", "a") as f:
            f.write(line + "\n")

    def artifact(self, sid):
        return self.stage[sid]["outputs"][0]

    def part(self, sid, chunk):
        a = self.artifact(sid)
        return self.B / (a.replace(".json", f".part.{chunk}.json") if sid in CONCEPT_CHUNKED | VIDEO_CHUNKED else a)

    def sh(self, cmd, check=True, log=None):
        """Run a shell command. With log=<name>, output streams live to working/<name>.log (tail -f it) instead of being captured."""
        if log:
            lf = self.B / "working" / f"{log}.log"
            with open(lf, "w") as f:
                r = subprocess.run(cmd, shell=True, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, text=True, env=self.env)
            r.stdout, r.stderr = lf.read_text()[-2500:], ""
        else:
            r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, env=self.env)
        self.budget.check()
        if check and r.returncode:
            raise Stuck(f"command failed ({r.returncode}): {cmd}\n{(r.stdout + r.stderr)[-2500:]}")
        return r

    def py(self, script, *a):
        return f"{sys.executable} {SCRIPTS / script} " + " ".join(f"'{x}'" for x in a)

    def valid(self, sid, path):
        schema = Path(path).name.split(".part.")[0].replace(".json", "") + ".schema.json"
        if not (CORE / "schemas" / schema).exists():
            return True, "no schema"
        r = self.sh(self.py("schema_check.py", schema, path), check=False)
        return r.returncode == 0, (r.stdout + r.stderr)[-1500:]

    def agent(self, role, system, task, label):
        model = (self.gen_pin if role == "GEN" else self.ev_pin) or role
        return run_agent(model, system, task, self.budget, role=role, write_roots=[self.B, ROOT / "scratch"], label=label)


def agent_prompt(role):
    t = (ROOT / ".claude" / "agents" / ("glossary-generator.md" if role == "GEN" else "glossary-evaluator.md")).read_text()
    body = t.split("---", 2)[2].strip()
    return body + "\n\nYou have three tools: read_file, write_file (only under the batch folder), bash (run from the pack root; `python3` has jsonschema; there is no WebSearch, use curl for fetching). Pack root is the working directory. Finish by replying with the requested summary."


# ---------- chunks ----------
def concept_chunks(c):
    p = c.B / "chunks.json"
    ec = load(c.B / "extracted_concepts.json")
    concepts = sorted(ec["concepts"], key=lambda x: x["toc_sequence_position"])
    if len({x["path_id"] for x in concepts}) > 1 and not p.exists():
        raise Stuck("multi-path batch: write batches/<id>/chunks.json by hand (concept chunks per path)")
    if p.exists():
        return {k: v["concept_ids"] for k, v in load(p)["chunks"].items()}
    if len(concepts) < MIN_FANOUT:
        ids = [x["concept_id"] for x in concepts]
        p.write_text(json.dumps({"path_id": concepts[0]["path_id"], "chunks": {"all": {"regions": [], "concept_ids": ids}}}, indent=2))
        return {"all": ids}
    tiles, order = {}, []
    for x in concepts:
        t = x["toc_location"]["tile_id"]
        if t not in tiles:
            tiles[t] = {"region": x["toc_location"]["region_id"], "ids": []}; order.append(t)
        tiles[t]["ids"].append(x["concept_id"])
    chunks, cur, i = {}, [], 0
    canary_done = False
    regions, cur_regions = [], set()
    for t in order:
        ids, reg = tiles[t]["ids"], tiles[t]["region"]
        if not canary_done:
            cur += ids
            cur_regions.add(reg)
            if len(cur) >= 5:
                chunks["c0_canary"] = {"regions": sorted(cur_regions), "concept_ids": cur}; cur, cur_regions, canary_done = [], set(), True
            continue
        new_region = cur and reg not in cur_regions
        if cur and (len(cur) + len(ids) > 36 or (new_region and len(cur) >= 24)):
            i += 1; chunks[f"c{i}"] = {"regions": sorted(cur_regions), "concept_ids": cur}; cur, cur_regions = [], set()
        cur += ids; cur_regions.add(reg)
    if cur:
        i += 1; chunks[f"c{i}"] = {"regions": sorted(cur_regions), "concept_ids": cur}
    p.write_text(json.dumps({"path_id": concepts[0]["path_id"], "chunks": chunks}, indent=2))
    return {k: v["concept_ids"] for k, v in chunks.items()}


def video_chunks(c):
    p = c.B / "chunks_08.json"
    if p.exists():
        return {k: v["video_ids"] for k, v in load(p)["chunks"].items()}
    vids = []
    for s in load(c.B / "video_candidates.json")["searches"]:
        for x in s["candidates"]:
            if x["filter_verdict"] == "kept" and x["video_id"] not in vids:
                vids.append(x["video_id"])
    if len(vids) < MIN_FANOUT // 3:
        chunks = {"all": vids}
    else:
        chunks = {"c0_canary": vids[:5]}
        rest = vids[5:]
        n = max(1, round(len(rest) / 33))
        size = -(-len(rest) // n)
        for k in range(n):
            chunks[f"c{k + 1}"] = rest[k * size:(k + 1) * size]
    p.write_text(json.dumps({"path_id": load(c.B / "extracted_concepts.json")["paths"][0]["path_id"],
                             "chunks": {k: {"video_ids": v, "concept_count": 0} for k, v in chunks.items()}}, indent=2))
    return chunks


# ---------- agent task builders ----------
def scope_text(sid, chunk, ids):
    if chunk == "all":
        return "Cover the whole batch."
    what = "video ids" if sid in VIDEO_CHUNKED else "concept ids"
    return f"Fan-out chunk `{chunk}`: cover ONLY these {what}: {json.dumps(ids)}."


def generator_task(c, sid, chunk, ids, repair=None):
    part = c.part(sid, chunk).relative_to(ROOT)
    base = (f"Stage `{sid}`, batch folder `{c.B.relative_to(ROOT)}/`. Read `01_GLOSSARY_PACK_TEMPLATE/{sid}/GENERATOR.md` and follow it exactly, "
            f"plus the playbook sections it cites. Follow the 'Evaluation cost control' section of `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md` "
            f"(run your own mistakes checklist before finishing). {scope_text(sid, chunk, ids)}\n"
            f"Write `{part}`. Metadata: batch_id `{c.id}`, model `{c.gen}`, prompt_version `{sid}@v1`, real UTC generated_at, "
            f"parent_artifact_hashes = sha256 of the input artifacts the stage names. Build big files with a script, not by hand. "
            f"Validate with schema_check.py (see GENERATOR.md) before finishing.")
    if repair:
        base = (f"REPAIR ROUND for stage `{sid}`, artifact `{part}`. Evaluator findings follow. Change ONLY what the findings name; "
                f"advisory fixes may only reword, delete, move or cite, never add a new claim (skip one that would need a new claim). "
                f"Patch the existing file with a small script (do not rewrite it from scratch), then re-validate.\n\n{repair}")
    return base


def evaluator_task(c, sid, chunk, ids, prior=None):
    part = c.part(sid, chunk).relative_to(ROOT)
    t = (f"Evaluate stage `{sid}`, batch folder `{c.B.relative_to(ROOT)}/`. Read `01_GLOSSARY_PACK_TEMPLATE/{sid}/EVALUATOR.md` and follow it. "
         f"Artifact under evaluation: `{part}`. {scope_text(sid, chunk, ids)} Schema validity was already checked by script. "
         f"Follow the 'Evaluation cost control' section of `START_HERE.md` (depth by tier, sampling ceilings). "
         f"Label every defect BLOCKING or ADVISORY. End with `VERDICT: PASS` or `VERDICT: FAIL`, then one line per defect: "
         f"`BLOCKING|ADVISORY concept_id@path_id: what is wrong -> what fixes it`. Do not edit the artifact.")
    if prior:
        t += ("\n\nThis is a SCOPED re-evaluation after a repair. Check only the facts/blocks the repair changed against their sources and confirm nothing "
              f"else changed. Previous findings that were sent for repair:\n{prior}")
    return t


def parse_eval(text):
    m = VERDICT.findall(text)
    if not m:
        return None, []
    defects = [ln.strip() for ln in text.splitlines() if re.match(r"\s*[-*]?\s*(BLOCKING|ADVISORY)\b", ln)]
    verdict = m[-1]
    if verdict == "FAIL" and not any("BLOCKING" in d for d in defects):
        defects.append("BLOCKING (unparsed): " + text[-1200:])
    return verdict, defects


# ---------- per-stage specialisations (cheaper, mechanical parts in code) ----------
def generate(c, sid, chunk, ids):
    if sid == "08_segment_detection":
        c.sh(c.py("glm_generate.py", c.B, chunk), log=f"sub_08_{chunk}")
    elif sid == "11_reconciliation":
        c.sh(c.py("bedrock_reconcile.py", c.B, chunk), log=f"sub_11gen_{chunk}")
    else:
        c.agent("GEN", agent_prompt("GEN"), generator_task(c, sid, chunk, ids), f"{sid}:{chunk}:gen")
    ok, msg = c.valid(sid, c.part(sid, chunk))
    if not ok:
        raise Stuck(f"{sid}:{chunk} generation produced an invalid artifact:\n{msg}")


def evaluate(c, sid, chunk, ids, prior=None, only=None):
    if sid == "11_reconciliation":
        cmd = c.py("bedrock_evaluate.py", c.B, chunk) + (" --only " + " ".join(only) if only else "")
        c.sh(cmd, log=f"sub_11eval_{chunk}")
        rep = load(c.B / "working" / f"eval_11_{chunk}.json")
        if rep["not_evaluated_due_to_errors"]:
            return None, [f"EVAL ERROR concepts: {rep['not_evaluated_due_to_errors']}", *[f"{k}: {v}" for k, v in list(rep.get("error_details", {}).items())[:5]]]
        return rep["verdict"], [f"{d['severity']} {d['concept_id']}@{d.get('path_id', '')} {d['field']}: {d['problem']} -> {d['fix']}" for d in rep["defects"]]
    for _ in range(2):
        v, d = parse_eval(c.agent("EVAL", agent_prompt("EVAL"), evaluator_task(c, sid, chunk, ids, prior), f"{sid}:{chunk}:eval"))
        if v:
            return v, d
    return None, ["evaluator never produced a VERDICT"]


def repair(c, sid, chunk, ids, defects):
    c.agent("GEN", agent_prompt("GEN"), generator_task(c, sid, chunk, ids, repair="\n".join(defects)), f"{sid}:{chunk}:repair")
    ok, msg = c.valid(sid, c.part(sid, chunk))
    if not ok:
        raise Stuck(f"{sid}:{chunk} repair broke the schema:\n{msg}")


def chunk_gen_eval(c, sid, chunk, ids):
    """Generate (or reuse), then evaluate/repair up to 3 rounds. Returns number of unresolved advisories."""
    done = c.B / "working" / f"state_{sid}_{chunk}.json"
    if done.exists() and load(done).get("passed"):
        return load(done)["advisories"]
    part = c.part(sid, chunk)
    if not part.exists() or not c.valid(sid, part)[0]:
        c.log(f"{sid}:{chunk} generating")
        generate(c, sid, chunk, ids)
    prior, only = None, None
    for rnd in range(1, MAX_ROUNDS + 1):
        c.log(f"{sid}:{chunk} evaluating (round {rnd})")
        verdict, defects = evaluate(c, sid, chunk, ids, prior, only)
        (c.B / "working" / f"eval_{sid}_{chunk}_r{rnd}.txt").write_text(f"{verdict}\n" + "\n".join(defects))
        if verdict is None:
            raise Stuck(f"{sid}:{chunk} evaluator error: {defects}")
        blocking = [d for d in defects if d.lstrip("-* ").startswith("BLOCKING")]
        advisory = [d for d in defects if d not in blocking]
        if not blocking:
            if advisory:  # one reword-only repair, no re-evaluation (START_HERE)
                c.log(f"{sid}:{chunk} PASS with {len(advisory)} advisories; one repair, no re-evaluation")
                repair(c, sid, chunk, ids, advisory)
            done.write_text(json.dumps({"passed": True, "advisories": 0, "rounds": rnd}))
            return 0
        c.log(f"{sid}:{chunk} FAIL round {rnd}: {len(blocking)} blocking")
        if rnd == MAX_ROUNDS:
            raise Stuck(f"{sid}:{chunk} still failing after {MAX_ROUNDS} rounds:\n" + "\n".join(blocking[:15]))
        repair(c, sid, chunk, ids, defects)
        prior = "\n".join(defects)
        only = sorted({re.sub(r"^\W*(BLOCKING|ADVISORY)\s+", "", d).split("@")[0].split()[0] for d in defects if "@" in d}) or None


def fan_out(c, chunks, fn):
    names = list(chunks)
    results = {}
    first = names[0]
    results[first] = fn(first, chunks[first])  # canary alone
    rest = names[1:]
    if rest:
        errs = []
        with cf.ThreadPoolExecutor(int(os.environ.get("CHUNK_WORKERS", 2))) as ex:
            futs = {ex.submit(fn, n, chunks[n]): n for n in rest}
            for f in cf.as_completed(futs):
                try:
                    results[futs[f]] = f.result()
                except (Stuck, BudgetExceeded) as e:
                    errs.append(e)
        if errs:
            raise next((e for e in errs if isinstance(e, BudgetExceeded)), errs[0])
    return results


def merge(c, sid):
    a = c.artifact(sid)
    schema = a.replace(".json", ".schema.json")
    c.sh(c.py("merge_parts.py", c.B, a, schema))


def gate(c, sid, verdict="PASS", gen=None, ev=None, unresolved=0):
    UL.record(str(c.B), sid, c.artifact(sid), verdict, generator=gen or "none", evaluator=ev or "none", unresolved=unresolved)
    c.log(f"GATE {sid} {verdict}")


# ---------- stage runners ----------
def run_script_stage(c, sid):
    txt = (TEMPLATE / sid / "RUN.md").read_text()
    block = re.search(r"```bash\n(.*?)```", txt, re.S).group(1).replace("\\\n", " ").replace("<batch_id>", c.id)
    for line in [x.strip() for x in block.splitlines() if x.strip()]:
        c.log(f"{sid}: {line[:140]}")
        c.sh(line.replace("python3 ", f"{sys.executable} ", 1))


def run_gen_eval(c, sid):
    ids = concept_chunks(c) if sid in CONCEPT_CHUNKED else {"all": None}
    n = fan_out(c, ids, lambda ch, i: chunk_gen_eval(c, sid, ch, i))
    if sid in CONCEPT_CHUNKED:
        merge(c, sid)
    ok, msg = c.valid(sid, c.B / c.artifact(sid)) if sid not in ("00_preflight",) else (True, "")
    if not ok:
        raise Stuck(f"{sid} merged artifact invalid:\n{msg}")
    gate(c, sid, gen=c.gen, ev=c.ev, unresolved=sum(n.values()))


def judge_chunk(c, chunk, vids):
    part = c.part("09_segment_judge", chunk)
    props = load(c.part("08_segment_detection", chunk))["proposals"]
    want = {p["proposal_id"] for p in props}
    if part.exists() and c.valid("09_segment_judge", part)[0] and {j["proposal_id"] for j in load(part)["judgments"]} == want:
        return 0
    for attempt in range(2):
        text = c.agent("EVAL", agent_prompt("EVAL"),
                       f"Stage `09_segment_judge`, batch folder `{c.B.relative_to(ROOT)}/`. Read `01_GLOSSARY_PACK_TEMPLATE/09_segment_judge/EVALUATOR.md` and follow it. "
                       f"Judge EVERY proposal in `{c.part('08_segment_detection', chunk).relative_to(ROOT)}` ({len(want)} proposals) and write `{part.relative_to(ROOT)}` "
                       f"(a full segment_judgments schema document: batch_id `{c.id}`, model `{c.ev}`, prompt_version `09_segment_judge@v1`, parent hashes = sha256 of that proposals file, "
                       f"`coverage_briefs.json`, `extracted_concepts.json`). Follow the 'Evaluation cost control' section of START_HERE.md. End with VERDICT: PASS or FAIL "
                       f"(did you judge honestly and completely, not whether proposals were good) and list your rejections.", f"09:{chunk}")
        ok = part.exists() and c.valid("09_segment_judge", part)[0] and {j["proposal_id"] for j in load(part)["judgments"]} == want
        if ok and "VERDICT: FAIL" not in text:
            return 0
    raise Stuck(f"09:{chunk} judge did not produce a complete, valid judgments file")


def run_08_09(c):
    chunks = video_chunks(c)

    def one(chunk, vids):
        p = c.part("08_segment_detection", chunk)
        if not p.exists() or not c.valid("08_segment_detection", p)[0]:
            c.log(f"08:{chunk} detecting"); generate(c, "08_segment_detection", chunk, vids)
        c.log(f"09:{chunk} judging"); return judge_chunk(c, chunk, vids)
    fan_out(c, chunks, one)
    merge(c, "08_segment_detection"); merge(c, "09_segment_judge")
    gate(c, "08_segment_detection", gen=c.gen, ev="stage 09")
    gate(c, "09_segment_judge", ev=c.ev)


def run_evaluator_only(c, sid):
    chunks = concept_chunks(c) if sid in CONCEPT_CHUNKED else {"all": None}

    def one(chunk, ids):
        part = c.part(sid, chunk)
        if part.exists() and c.valid(sid, part)[0]:
            return 0
        for _ in range(2):
            text = c.agent("EVAL", agent_prompt("EVAL"),
                           f"Run stage `{sid}`, batch folder `{c.B.relative_to(ROOT)}/`. Read the instruction file in `01_GLOSSARY_PACK_TEMPLATE/{sid}/` "
                           f"({'INDEPENDENT_AUDIT.md' if sid.startswith('16') else 'EVALUATOR.md'}) and follow it. {scope_text(sid, chunk, ids)} "
                           f"Write `{part.relative_to(ROOT)}` yourself (metadata model `{c.ev}`, prompt_version `{sid}@v1`), validate it with schema_check.py, "
                           f"and end with the VERDICT line the instructions name.", f"{sid}:{chunk}")
            if part.exists() and c.valid(sid, part)[0] and VERDICT.findall(text):  # 13/16 report their own blocking result in the artifact
                return 0
        raise Stuck(f"{sid}:{chunk} evaluator did not produce a valid artifact")
    fan_out(c, chunks, one)
    if sid in CONCEPT_CHUNKED:
        merge(c, sid)
    rep = load(c.B / c.artifact(sid))
    if sid == "13_leakage_check" and rep.get("blocking_issue_count", 0) > 0:
        raise Stuck(f"13 leakage check found {rep['blocking_issue_count']} blocking issues; the fix belongs to stage 05/11 (or 09 for a leaking segment), then rerun downstream. See {c.artifact(sid)}.")
    if sid == "16_final_audit" and rep.get("verdict") == "FAIL":
        raise Stuck("16 independent audit verdict FAIL; see glossary_independent_audit_report.json")
    gate(c, sid, ev=c.ev)


def run_final_validation(c):
    sid = "15_final_validation"
    run_script_stage(c, sid)
    c.log("15: cross-artifact review")
    c.agent("EVAL", agent_prompt("EVAL"),
            f"Stage `{sid}`, batch folder `{c.B.relative_to(ROOT)}/`. Run `01_GLOSSARY_PACK_TEMPLATE/15_final_validation/CROSS_ARTIFACT_REVIEW.md` (the script already wrote "
            f"`glossary_validation_report.json`; amend that same file, and write `human_spot_check.md` in the batch folder). End with VERDICT: PASS or FAIL.", "15:review")
    rep = load(c.B / "glossary_validation_report.json")
    ok = c.valid(sid, c.B / "glossary_validation_report.json")[0]
    status = "PASS" if ok and rep.get("validation_status") == "PASS" else "FAIL"
    gate(c, sid, status, ev=c.ev)
    if status == "FAIL":
        raise Stuck("15 validation FAIL; see glossary_validation_report.json blocking_errors")


# ---------- plumbing ----------
def is_done(c, sid):
    g = next((g for g in UL.load_ledger(str(c.B))["gates"] if g["stage_id"] == sid), None) if (c.B / "glossary_stage_gate_ledger.json").exists() else None
    try:
        return bool(g and g["verdict"] == "PASS" and UL.artifact_hash(str(c.B), g["artifact"]) == g["artifact_hash"])
    except FileNotFoundError:
        return False


def git(c, msg, pull=False):
    if c.args.no_push:
        return
    cmds = ["git pull --rebase --autostash"] if pull else ["git add -A batches 00_GLOSSARY_PIPELINE_CORE/video_bank 00_GLOSSARY_PIPELINE_CORE/registry",
                                                          f"git commit -qm '{msg}' || true", "git push"]
    for cmd in cmds:
        r = c.sh(cmd, check=False)
        if r.returncode and "commit" not in cmd:
            c.log(f"git warning ({cmd}): {(r.stdout + r.stderr)[-300:]}")


def notify(c, subject, body):
    c.log(f"NOTIFY {subject}")
    (c.B / "working" / ("DRIVER_STOPPED.md" if "STOPPED" in subject else "DRIVER_DONE.md")).write_text(f"# {subject}\n\n{body}\n")
    topic = os.environ.get("SNS_TOPIC_ARN")
    if topic:
        try:
            import boto3
            boto3.client("sns", region_name=topic.split(":")[3]).publish(TopicArn=topic, Subject=subject[:100], Message=body[:20000])
        except Exception as e:
            c.log(f"SNS publish failed: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir"); ap.add_argument("--max-usd", type=float, default=float(os.environ.get("MAX_USD", 300)))
    ap.add_argument("--plan", action="store_true"); ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    load_env()
    B = Path(a.batch_dir); B = B if B.is_absolute() else ROOT / B
    B.mkdir(parents=True, exist_ok=True)
    c = Ctx(B, a)
    c.log(f"start {c.id}; cap ${a.max_usd}; generator {c.gen}; evaluator {c.ev}; spent so far ${c.budget.spent():.2f}")
    if not a.plan:
        git(c, "", pull=True)
    try:
        for st in c.manifest["stages"]:
            sid, kind = st["id"], st["kind"]
            if sid == "09_segment_judge":
                continue
            if sid == "15b_stage_gate_ledger":
                if not a.plan:
                    run_script_stage(c, sid)
                continue
            if sid == "16b_registry_merge":
                if (c.B / "working" / "DONE").exists() or a.plan:
                    c.log("16b: " + ("already done" if (c.B / "working" / "DONE").exists() else "would run")); continue
                git(c, "", pull=True); run_script_stage(c, sid); git(c, f"{c.id}: registry merge")
                (c.B / "working" / "DONE").write_text(time.strftime("%FT%T")); continue
            if sid == "08_segment_detection":
                done = is_done(c, sid) and is_done(c, "09_segment_judge")
            else:
                done = is_done(c, sid)
            if done:
                c.log(f"{sid}: gated PASS on disk, skipping"); continue
            if a.plan:
                c.log(f"{sid}: WOULD RUN ({kind})"); continue
            c.log(f"=== {sid} ({kind}) spent ${c.budget.spent():.2f}")
            if sid == "08_segment_detection": run_08_09(c)
            elif sid == "15_final_validation": run_final_validation(c)
            elif kind == "script": run_script_stage(c, sid); gate(c, sid)
            elif kind == "generate_evaluate": run_gen_eval(c, sid)
            elif kind == "evaluator_only": run_evaluator_only(c, sid)
            git(c, f"{c.id}: {sid} gated")
        if not a.plan:
            notify(c, f"DONE {c.id}", f"All stages gated and registry merged. Spend ${c.budget.spent():.2f}. Review list: batches/{c.id}/human_spot_check.md")
    except (Stuck, BudgetExceeded) as e:
        notify(c, f"STOPPED {c.id}", f"{e}\n\nSpend so far ${c.budget.spent():.2f}. Fix the cause, then rerun the same command (finished stages are skipped).")
        git(c, f"{c.id}: driver stopped, progress")
        sys.exit(2)


if __name__ == "__main__":
    main()
