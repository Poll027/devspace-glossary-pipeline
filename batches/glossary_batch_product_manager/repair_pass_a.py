import json
from pathlib import Path
p = Path('batches/glossary_batch_product_manager/glossary_pass_a.part.all.json')
data = json.loads(p.read_text())
before = json.loads(p.read_text())
entries = {r['concept_id']: r for r in data['entries']}
changed = {}
def block(cid, bid):
    changed.setdefault(cid, set()).add(bid)
    return next(b for b in entries[cid]['teaching_blocks'] if b['id'] == bid)

cid = 'stakeholder_communication.executive_communication'
b = block(cid, 'tb3')
b['content'] = 'First specify the objective of the update: approval asks leadership to authorize a proposed action; strategic buy-in asks for support for the proposed strategic approach; strategic direction asks leadership to guide which strategic course to pursue. Put that decision or ask at the start, then provide supporting detail. Lead with the headline and name the key risk or implication. Keep technical detail subordinate to the executive’s immediate information need.'
b = block(cid, 'tb4')
b['content'] = b['content'].replace('“We need a decision on moving the closing-summary release by two weeks.”', '“Please approve moving the closing-summary release by two weeks.” This update seeks approval for a specific timing change, not strategic buy-in for the product approach or strategic direction about which course to pursue.')

cid = 'agile_delivery.technical_feasibility_conversations'
b = block(cid, 'tb3')
b['content'] += ' Review a shared specification with engineering: use its proposed behavior and constraints to identify roadblocks, then agree on the features, requirements, and test plans it records. The specification makes the agreed scope and checks explicit rather than leaving the conversation as a list of uncertainties.'
b = block(cid, 'tb4')
b['content'] = b['content'].replace('Record the clarified implications and adjust the product proposal accordingly.', 'Use a shared specification to review this roadblock and agree on the feature, requirements, and test plan. For example, suppose engineering confirms that unfinished paid-order status is available for the selected day but historical status is not. Together specify a selected-day closing summary, require it to show unfinished paid orders for that day, and agree to test it with example orders that are paid and unfinished, paid and finished, and unpaid. Record the expected inclusion of only the paid, unfinished orders and exclude historical summaries from the agreed scope. This is an illustrative agreement, not a claim about a real system. Record the clarified implications and adjust the product proposal accordingly.')

cid = 'metrics_and_analytics.ab_testing'
b = block(cid, 'tb3')
b['content'] += ' In Amplitude’s Duration Estimator, select Estimate Duration. Add a traffic event and conversion success metric, or manually enter total daily traffic and baseline conversion. Set the relative minimum detectable effect (MDE), the smallest proportional improvement you want to detect, and the confidence level. Read the estimated days and users per day. For a plan exposing all that traffic, multiply days by users per day for an approximate total sample; divide by two for an equal two-variant allocation. These are traffic-based estimates derived from the outputs, not a separate sample-size output from the tool.'
b = block(cid, 'tb4')
b['content'] += ' For a planning example, select Estimate Duration and manually enter 1,000 total daily users and 40% baseline conversion. Set a 10% relative MDE (a rise from 40% to 44%) and 95% confidence. Suppose the displayed estimate is 20 days and 1,000 users per day. With all that traffic exposed, the approximate total is 20 × 1,000 = 20,000 users, or 10,000 per variant under equal two-variant allocation. The displayed outputs here are stipulated example data, not a calculation predicting what Amplitude will return for those inputs.'

cid = 'metrics_and_analytics.holdout_groups'
for bid in ['tb1', 'tb2']:
    b = block(cid, bid)
    b['content'] = b['content'].replace('a randomly selected subset', 'a subset of users')
b = block(cid, 'tb3')
b['content'] = b['content'].replace('Amplitude specifies a configurable range of 1–10%, not a universal requirement.', 'Amplitude requires choosing a percentage between 1% and 10% when creating the group, not a universal range for every holdout. Withholding more traffic can extend experiment duration, and Amplitude does not allow changing the percentage after creation.')
b = block(cid, 'tb4')
b['content'] = b['content'].replace('In Amplitude, the configurable range is 1–10%; that tool-specific range is not a universal requirement for every holdout.', 'In Amplitude, choose this 5% within the allowed 1–10% range at creation; that tool-specific range is not a universal requirement for every holdout. Before creating it, consider whether withholding 5% leaves enough traffic for the planned experiment duration: withholding more traffic can extend that duration. Do not plan to start at 5% and raise it later, because Amplitude prohibits changing the percentage after creation.')

cid = 'go_to_market.sales_and_support_enablement'
b = block(cid, 'tb3')
b['content'] += ' Build the FAQ by listing customer questions raised by the feature and recording answers in a support-team reference. For talking points, provide a brief product description, a short positioning statement, and value pillars that explain how the feature delivers value and addresses customer pain points. Build the known-limitations reference from the product requirements, listing specifically what is out of scope for the feature or release; update that list as the requirements evolve.'
b['fact_ids'] = ['f3', 'f4', 'f6', 'f7', 'f8']
b = block(cid, 'tb4')
b['content'] = b['content'].replace('A talking point is “Check remaining work in one view before closing.” Record the example limitation “This release does not edit payment history,”', 'Build the talking points around the stipulated behavior. Brief description: “A selected-day summary of unfinished paid orders.” Positioning: “For shop owners reviewing remaining work before closing, this summary brings unfinished paid orders for the selected day into one view.” Value pillars: “Visibility into remaining work—the summary shows unfinished paid orders, addressing the owner’s question about what still needs attention; a focused daily review—the selected-day scope keeps the review on that day’s remaining orders, addressing the difficulty of separating today’s work from other days.” These are intended values, not measured performance claims. Use the product requirements to record the example limitation “This release does not edit payment history,”')
b['content'] = b['content'].replace('These packet contents must match the actual agreed feature rather than promise unsupported cases.', 'For an illustrative requirements update, suppose the agreed requirements are clarified to exclude historical-day summaries from this release. Add “Historical-day summaries are out of scope for this release” to the known-limitations reference and revise the FAQ to specify that the selected day is the current closing day. Keep the payment-history limitation unless the requirements change it. These packet contents must match the actual agreed feature rather than promise unsupported cases.')
b['fact_ids'] = ['f1', 'f2', 'f3', 'f4', 'f6', 'f7', 'f8']
b = block(cid, 'tb5')
b['fact_ids'] = ['f1', 'f2', 'f3', 'f4', 'f7', 'f8']

# Verify that the patch touches only the five named entries and their named teaching blocks.
for old, new in zip(before['entries'], data['entries']):
    cid = old['concept_id']
    if cid not in changed:
        assert old == new
        continue
    assert {k:v for k,v in old.items() if k != 'teaching_blocks'} == {k:v for k,v in new.items() if k != 'teaching_blocks'}
    for ob, nb in zip(old['teaching_blocks'], new['teaching_blocks']):
        if ob['id'] not in changed[cid]:
            assert ob == nb
        else:
            assert {k:v for k,v in ob.items() if k not in ('content','fact_ids')} == {k:v for k,v in nb.items() if k not in ('content','fact_ids')}
assert {k:v for k,v in before.items() if k != 'entries'} == {k:v for k,v in data.items() if k != 'entries'}
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('Entries:', len(data['entries']))
print('Teaching blocks:', sum(len(r['teaching_blocks']) for r in data['entries']))
print('Changed entries:', len(changed), 'changed blocks:', sum(map(len, changed.values())))
