import json
from pathlib import Path
p = Path('batches/glossary_batch_laravel_vue_full_stack_developer/glossary_pass_a.part.all.json')
d = json.loads(p.read_text())
original = json.loads(p.read_text())
entries = {r['concept_id']: r for r in d['entries']}
def block(concept, ident):
    return next(b for b in entries[concept]['teaching_blocks'] if b['id'] == ident)
for ident in ('tb3', 'tb4'):
    b = block('vitest.vue_test_execution', ident)
    assert 'as jsdom' in b['content']
    b['content'] = b['content'].replace('as jsdom', 'as happy-dom')
b = block('php.application_exceptions', 'tb5')
assert "For return behavior, remember the brief's additional warning: a return" in b['content']
b['content'] = b['content'].replace("For return behavior, remember the brief's additional warning: a return", 'A return')
block('eloquent.filtered_queries', 'tb4')['content'] = "Suppose a supplied record listing contains these rows, shown as (id, status, amount): (1, 'open', 40), (2, 'closed', 90), (3, 'open', 70), and (4, 'open', 20). The listing requires status equal to 'open', amount greater than 30, and descending amount order. On the supplied model query, chain where('status', 'open'), where('amount', '>', 30), and orderBy('amount', 'desc'), then call get(). The two where predicates must both match; orderBy orders the survivors, and get retrieves the matching models. Predict the result using the same three displayed columns."
block('eloquent.filtered_queries', 'tb5')['content'] = "First evaluate status: records 1, 3, and 4 are 'open'; record 2 is excluded even though its amount is 90. Then evaluate amount greater than 30: records 1 and 3 survive, while record 4, with amount 20, is excluded. Sorting those survivors by amount descending gives the ordered rows (3, 'open', 70), then (1, 'open', 40), displayed as (id, status, amount). These are the models retrieved by get after the constraints. Filtering determined membership; ordering put record 3 before record 1. Choosing 'asc' instead would reverse these two rows; ascending is also the default."
block('vue.computed_derivations', 'tb4')['content'] = "Suppose a supplied reactive record collection contains (id, selected, amount) values (1, true, 4), (2, true, 6), and (3, false, 8). Inside the computed getter, use filter to keep records whose selected value is true. Initialize a local total at 0, traverse records 1 and 2 with for...of, and add their amounts: 0 + 4 = 4, then 4 + 6 = 10. Return 10 as the computed result, a derived ref. Now change record 2's reactive amount from 6 to 9 outside the getter. This tracked dependency change invalidates the cached result. On the next calculation, the same selection yields 0 + 4 + 9 = 13, so the derived total is 13 instead of 10. Record 3 remains excluded. Keep the local accumulator separate from the source records: the getter calculates the total without rewriting their amounts or performing requests."
allowed = {('vitest.vue_test_execution', 'tb3'), ('vitest.vue_test_execution', 'tb4'), ('php.application_exceptions', 'tb5'), ('eloquent.filtered_queries', 'tb4'), ('eloquent.filtered_queries', 'tb5'), ('vue.computed_derivations', 'tb4')}
for old, new in zip(original['entries'], d['entries']):
    for ob, nb in zip(old['teaching_blocks'], new['teaching_blocks']):
        if ob != nb:
            assert (new['concept_id'], nb['id']) in allowed
            assert {k:v for k,v in ob.items() if k != 'content'} == {k:v for k,v in nb.items() if k != 'content'}
    assert {k:v for k,v in old.items() if k != 'teaching_blocks'} == {k:v for k,v in new.items() if k != 'teaching_blocks'}
assert [r for r in [(1,'open',40),(2,'closed',90),(3,'open',70),(4,'open',20)] if r[1]=='open' and r[2]>30] == [(1,'open',40),(3,'open',70)]
assert sorted([(1,'open',40),(3,'open',70)], key=lambda r:r[2], reverse=True) == [(3,'open',70),(1,'open',40)]
assert sum(r[2] for r in [(1,True,4),(2,True,6),(3,False,8)] if r[1]) == 10
assert sum(r[2] for r in [(1,True,4),(2,True,9),(3,False,8)] if r[1]) == 13
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('entries:', len(d['entries']))
print('teaching_blocks:', sum(len(r['teaching_blocks']) for r in d['entries']))
print('changed blocks:', len(allowed))
