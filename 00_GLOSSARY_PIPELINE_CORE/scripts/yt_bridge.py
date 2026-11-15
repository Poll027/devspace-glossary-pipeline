#!/usr/bin/env python3
"""YouTube bridge: YouTube blocks cloud IPs, so stage 07 (transcripts) and catalogue syncs run on a machine with a normal home IP and hand
their results back through a git branch (`yt-bridge`) of this repo. No inbound access, no extra service.

  VM  (stage 07):   python3 yt_bridge.py transcripts <batch_dir> <video_bank_dir>
                    Nothing missing from the bank -> runs fetch_videos.py offline and returns. Otherwise posts a job, then polls for the result
                    (exit 4 + "AWAITING MAC" if none arrives within WAIT_H hours; the supervisor retries).
  VM  (new channels): python3 yt_bridge.py catalogs <video_bank_dir> <channel_id> ...      (same wait; the catalogues land in video_bank/channel_catalogs)
  Mac (leave running): python3 yt_bridge.py worker [--once]  (needs yt-dlp; loops every 60 s; --once handles the waiting jobs and exits; Ctrl-C to stop)

Jobs: jobs/<id>.json on the branch. Results: results/<id>.tgz (+ results/<id>.done). A result is applied once; ids are batch ids or catalogs-<hash>.
# ponytail: git is the queue (latency ~1 min, no new infrastructure); a result only adds files to the bank, never overwrites one.
"""
import hashlib, io, json, os, subprocess, sys, tarfile, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REMOTE = os.environ.get("YT_BRIDGE_REMOTE", "https://github.com/Poll027/devspace-glossary-pipeline.git")
CLONE = Path(os.environ.get("YT_BRIDGE_DIR", Path.home() / "yt-bridge"))
BANK_MAC = Path(os.environ.get("YT_BANK_DIR", Path.home() / ".yt_bank"))  # the Mac's own cache: a video is fetched once, ever
WAIT_H = float(os.environ.get("YT_WAIT_H", 12))


def git(*a, ok=False):
    r = subprocess.run(["git", "-C", str(CLONE), "-c", "user.name=yt-bridge", "-c", "user.email=yt-bridge@localhost", *a], capture_output=True, text=True)
    if r.returncode and not ok:
        raise RuntimeError(f"git {' '.join(a)}: {(r.stdout + r.stderr)[-300:]}")
    return r.stdout.strip()


def sync():
    """Fresh checkout of the bridge branch (created empty on first use)."""
    if not (CLONE / ".git").exists():
        subprocess.run(["git", "clone", "-q", REMOTE, str(CLONE)], check=True)
    git("fetch", "-q", "origin", ok=True)
    if git("ls-remote", "--heads", "origin", "yt-bridge", ok=True):
        git("checkout", "-q", "-B", "yt-bridge", "origin/yt-bridge")
    elif git("branch", "--list", "yt-bridge", ok=True):
        git("checkout", "-q", "yt-bridge")
    else:
        git("checkout", "-q", "--orphan", "yt-bridge")
        git("rm", "-rfq", ".", ok=True)
        (CLONE / "README.md").write_text("yt-bridge: job queue between the cloud VM and a home-IP machine. See 00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py on main.\n")
        git("add", "-A")
        git("commit", "-qm", "init yt-bridge")


def push(msg):
    git("add", "-A")
    if git("status", "--porcelain"):
        git("commit", "-qm", msg)
    for _ in range(5):
        r = subprocess.run(["git", "-C", str(CLONE), "push", "-q", "origin", "yt-bridge"], capture_output=True)
        if r.returncode == 0:
            return
        git("pull", "-q", "--rebase", "origin", "yt-bridge", ok=True)
    raise RuntimeError("could not push the yt-bridge branch")


def tar_files(base, files):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for f in files:
            t.add(base / f, arcname=str(f))
    return buf.getvalue()


def untar_safe(data, dest):
    """Extract only plain relative files under catalogue/, transcripts/, channel_catalogs/ or the report; never overwrite an existing bank file."""
    n = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
        for m in t.getmembers():
            p = Path(m.name)
            ok = m.isfile() and not p.is_absolute() and ".." not in p.parts and p.parts[0] in ("catalogue", "transcripts", "channel_catalogs", "report")
            if not ok:
                continue
            if p.parts[0] == "report":
                continue  # handled by report_from
            out = dest / p
            if out.exists():
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(t.extractfile(m).read())
            n += 1
    return n


def report_from(data):
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
        for m in t.getmembers():
            if m.name == "report/transcript_sync_report.json":
                return t.extractfile(m).read()
    return None


def wait_result(jid):
    t0 = time.time()
    while time.time() - t0 < WAIT_H * 3600:
        sync()
        f = CLONE / "results" / f"{jid}.tgz"
        if f.exists() and (CLONE / "results" / f"{jid}.done").exists():
            return f.read_bytes()
        time.sleep(60)
    print(f"AWAITING MAC: no result for {jid} after {WAIT_H:g} h. Start `python3 {Path(__file__).name} worker` on a machine with a home IP.", flush=True)
    sys.exit(4)


def missing_ids(batch, bank):
    cands = json.loads((batch / "video_candidates.json").read_text())
    ids = {c["video_id"] for s in cands["searches"] for c in s["candidates"] if c["filter_verdict"] == "kept"}  # same selection as fetch_videos.py
    return sorted(i for i in ids if not (bank / "catalogue" / f"{i}.json").exists()), cands


def vm_transcripts(batch, bank):
    batch, bank = Path(batch).resolve(), Path(bank).resolve()
    miss, cands = missing_ids(batch, bank)
    if miss:
        jid = batch.name
        sync()
        (CLONE / "jobs").mkdir(exist_ok=True)
        (CLONE / "jobs" / f"{jid}.json").write_text(json.dumps({"id": jid, "type": "transcripts", "candidates": cands, "missing": miss}))
        push(f"job {jid}: {len(miss)} videos")
        print(f"[yt_bridge] posted job {jid} ({len(miss)} videos); waiting for the Mac worker", flush=True)
        data = wait_result(jid)
        print(f"[yt_bridge] applied {untar_safe(data, bank)} bank files", flush=True)
        rep = report_from(data)
        if rep:
            (batch / "transcript_sync_report.json").write_bytes(rep)
            print("[yt_bridge] transcript_sync_report.json written by the Mac run", flush=True)
            return 0
        print("[yt_bridge] the Mac result has no sync report (its fetch crashed); not falling back to a fetch from this IP", flush=True)
        return 5
    return subprocess.run([sys.executable, str(HERE / "fetch_videos.py"), str(batch), str(bank)]).returncode  # everything cached: offline, builds the report


def vm_catalogs(bank, ids):
    bank = Path(bank).resolve()
    jid = "catalogs-" + hashlib.sha1(",".join(sorted(ids)).encode()).hexdigest()[:10]
    sync()
    (CLONE / "jobs").mkdir(exist_ok=True)
    (CLONE / "jobs" / f"{jid}.json").write_text(json.dumps({"id": jid, "type": "catalogs", "channels": sorted(ids)}))
    push(f"job {jid}")
    data = wait_result(jid)
    print(f"[yt_bridge] applied {untar_safe(data, bank)} catalogue files", flush=True)
    return 0


def mac_job(job):
    if job["type"] == "catalogs":
        for c in job["channels"]:
            subprocess.run([sys.executable, str(HERE / "sync_catalogs.py"), str(BANK_MAC), c], check=False)
        files = [p.relative_to(BANK_MAC) for c in job["channels"] for p in [BANK_MAC / "channel_catalogs" / f"{c}.json"] if p.exists()]
        return tar_files(BANK_MAC, files)
    with tempfile.TemporaryDirectory() as td:
        b = Path(td) / job["id"]
        b.mkdir()
        (b / "video_candidates.json").write_text(json.dumps(job["candidates"]))
        BANK_MAC.mkdir(parents=True, exist_ok=True)
        r = subprocess.run([sys.executable, str(HERE / "fetch_videos.py"), str(b), str(BANK_MAC)])
        files = [p.relative_to(BANK_MAC) for p in BANK_MAC.rglob("*.json") if p.parts[-2] in ("catalogue", "transcripts")]
        want = {f"{i}.json" for i in job["missing"]}
        files = [f for f in files if f.name in want]  # only what this job asked for (the cache may hold more)
        rep = b / "transcript_sync_report.json"
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t:
            for f in files:
                t.add(BANK_MAC / f, arcname=str(f))
            if rep.exists():
                t.add(rep, arcname="report/transcript_sync_report.json")
        if r.returncode not in (0, 1):
            print(f"[worker] fetch_videos exited {r.returncode}", flush=True)
        return buf.getvalue()


def mac_worker(once=False):
    print("[worker] yt-bridge worker running; Ctrl-C to stop", flush=True)
    while True:
        try:
            sync()
            for jf in sorted((CLONE / "jobs").glob("*.json")) if (CLONE / "jobs").exists() else []:
                jid = jf.stem
                if (CLONE / "results" / f"{jid}.done").exists():
                    continue
                print(f"[worker] job {jid}", flush=True)
                data = mac_job(json.loads(jf.read_text()))
                (CLONE / "results").mkdir(exist_ok=True)
                (CLONE / "results" / f"{jid}.tgz").write_bytes(data)
                (CLONE / "results" / f"{jid}.done").write_text(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
                push(f"result {jid}")
                print(f"[worker] result {jid} pushed ({len(data)} bytes)", flush=True)
        except Exception as e:
            print(f"[worker] error: {e}", flush=True)
        if once:
            return
        time.sleep(60)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("transcripts", "catalogs", "worker"):
        print(__doc__)
        return 1
    if a[0] == "transcripts" and len(a) == 3:
        return vm_transcripts(a[1], a[2])
    if a[0] == "catalogs" and len(a) >= 3:
        return vm_catalogs(a[1], a[2:])
    if a[0] == "worker":
        mac_worker("--once" in a)
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
