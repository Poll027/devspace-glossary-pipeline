exec(open('batches/glossary_batch_aws_devops_engineer/independent13/check.py').read().split('for i in range')[0])
for i in range(int(sys.argv[1]),int(sys.argv[2])):
 x=b[i];r=e[i];facts=c[i]['evidence']['required_facts'];ev=' '.join((q/f"s{si[z]['i']}.txt").read_text() for f in facts for z in f['source_refs']);ft=' '.join(f['statement'] for f in facts);known=tok(ev+' '+ft)
 text=' '.join(t['content'] for t in x['teaching_blocks']);anchor=' '.join(json.dumps(x[k],ensure_ascii=False) for k in ['assessment_anchors','practice_anchor','visual_anchor','teaching_notes']);allfields=text+' '+anchor
 print('\n###',i,r['concept_id']);print('Inline:',','.join(z['term'] for z in r['inline_vocabulary']))
 # Include assertions using concrete code/values and anything absent from source support.
 sentences=re.split(r'(?<=[.!?])\s+|\n+',text)
 novel=[]
 for s in sentences:
  sig={t for t in tok(s) if df[t]<8};new=sig-known
  if re.search(r'\d|--|\b(?:true|false|exception|always|never)\b',s) or len(new)>2:novel.append(s)
 print('REVIEW:', ' '.join(dict.fromkeys(novel)))
 extra=sorted(t for t in tok(anchor)-tok(text) if ('-' in t or '_' in t) and t not in ['tool_simulation','field_selection','data_table','fact_ids','allowed_syntax','blocked_syntax','observable_success','required_skill','starter_state_intent','live_code','annotated_screenshot','ui_state'] and not t.startswith(('verify_','identify_','determine_','distinguish_','recognize_','predict_','evaluate_','interpret_','configure_','select_','apply_','match_','justify_','record_','test_','check_','inspect_','document_','execute_','retain_','restore_','explain_','confirm_','preserve_','detect_','use_','gate_','report_','compare_','validate_','perform_','locate_','establish_','assess_','trace_','list_','run_')))
 if extra:print('ANCHOR terms',extra)
 # read all boundaries and assert frozen copies.
 assert set(r['blocked_knowledge_ids'])==set(x['context']['blocked_future_concepts'])
 assert set(r['allowed_knowledge_ids'])==set(z['concept_id'] for z in e[:i])
 assert x['coverage']['required_facts']==facts
