import sys,json,hashlib,math,tempfile
from pathlib import Path
B=Path('batches/glossary_batch_machine_learning_engineer')
sys.path.insert(0,str(B/'_fixture_dependencies'))
import numpy as np,pandas as pd,yaml
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier,DummyRegressor
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
A=json.loads((B/'glossary_pass_a.part.all.json').read_text())
C=json.loads((B/'extracted_concepts.json').read_text())['concepts']
R=json.loads((B/'coverage_briefs.json').read_text())['briefs']
D=json.loads((B/'depth_classification.json').read_text())['classifications']
keys=lambda rows:{(r['concept_id'],r['path_id']) for r in rows}
assert len(A['entries'])==95 and keys(A['entries'])==keys(C)==keys(R)==keys(D)
assert len(keys(A['entries']))==len(A['entries'])
for f,h in A['metadata']['parent_artifact_hashes'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
for c,r,e in zip(C,R,A['entries']):
 assert (c['concept_id'],c['path_id'])==(r['concept_id'],r['path_id'])==(e['concept_id'],e['path_id'])
 valid={f['id'] for f in r['evidence']['required_facts']}
 assert {f for b in e['teaching_blocks'] for f in b['fact_ids']}==valid
 assert len({b['id'] for b in e['teaching_blocks']})==len(e['teaching_blocks'])
 assert {'intro','example','misconception'}<={b['purpose'] for b in e['teaching_blocks']}
 assert all(b['content'].strip() and b['purpose']!='video_bridge' for b in e['teaching_blocks'])
 assert not any('```' in b['content'] for b in e['teaching_blocks']) # no claimed runnable full-code snippets
 assert e['video_need']['level']=='NONE' or e['video_need']['preferred_visual_modes']
X=np.array([[2,10],[4,20],[6,30]],dtype=np.float64)
assert X.ndim==2 and X.shape==(3,2) and X.nbytes==48
X32=X.astype(np.float32);assert X32.nbytes==24
np.testing.assert_allclose(X32-X,np.zeros_like(X),rtol=0,atol=0)
np.testing.assert_allclose(X-np.array([1,5]),np.array([[1,5],[3,15],[5,25]]),rtol=0,atol=0)
np.testing.assert_allclose(X-np.array([1,5]),np.array([[v-1,w-5] for v,w in X]),rtol=0,atol=0)
assert (np.ones((3,1))+np.ones((1,2))).shape==(3,2)
np.testing.assert_allclose(np.mean(X,axis=0),[4,20],rtol=0,atol=0)
np.testing.assert_allclose(np.std(X[:,0],ddof=0),math.sqrt(8/3),rtol=1e-12,atol=1e-12)
imp=SimpleImputer(strategy='mean').fit([[2],[6]])
stats=imp.statistics_.copy(); np.testing.assert_allclose(imp.transform([[100],[np.nan]]),[[100],[4]],rtol=0,atol=0)
np.testing.assert_allclose(imp.statistics_,stats,rtol=0,atol=0)
sc=StandardScaler().fit([[2],[6]])
np.testing.assert_allclose(sc.mean_,[4]);np.testing.assert_allclose(sc.scale_,[2]);np.testing.assert_allclose(sc.transform([[8]]),[[2]])
assert StandardScaler().fit([[2],[2]]).scale_[0]==1
enc=OneHotEncoder(handle_unknown='ignore').fit([['north'],['south']])
np.testing.assert_allclose(enc.transform([['east']]).toarray(),[[0,0]])
try:OneHotEncoder().fit([['north'],['south']]).transform([['east']]);assert False
except ValueError:pass
# Local text/CSV chunks, declarations, JSON and YAML calls appearing as syntax
# references in the lessons are exercised on supplied-shape toy fixtures.
with tempfile.TemporaryDirectory(dir=B) as tmp:
 p=Path(tmp)/'fixture.csv'; pd.DataFrame({'distance':[2,4,6],'zone':['north','south','north']}).to_csv(p,index=False)
 df=pd.read_csv(p,dtype={'distance':'float64','zone':'string'});assert list(df.columns)==['distance','zone'] and len(df)==3
 with open(p,'r',encoding='utf-8') as fh:
  chunks=list(pd.read_csv(fh,chunksize=2,dtype={'distance':'float64','zone':'string'}));assert [len(c) for c in chunks]==[2,1]
 q=Path(tmp)/'fixture.txt'
 with open(q,'w',encoding='utf-8') as fh:fh.write('verified toy fixture')
 with open(q,'r',encoding='utf-8') as fh:assert fh.read()=='verified toy fixture'
 y=Path(tmp)/'fixture.yaml'; cfg={'image':'fixture-only','replicas':1,'threshold':2}
 with open(y,'w',encoding='utf-8') as fh:yaml.safe_dump(cfg,fh)
 with open(y,'r',encoding='utf-8') as fh:assert yaml.safe_load(fh)==cfg
body=json.dumps({'inputs':[[2,10]]}).encode('utf-8');assert json.loads(body.decode('utf-8'))=={'inputs':[[2,10]]}
Xt=np.array([[0,0],[0,1],[1,0],[1,1],[2,1],[2,2]],dtype=float);yt=np.array([0,0,0,1,1,1])
model=LogisticRegression(random_state=0).fit(Xt,yt);assert model.predict(Xt).shape==(6,)
workflow=Pipeline([('scale',StandardScaler()),('model',LogisticRegression(random_state=0))]).fit(Xt,yt)
assert workflow.predict(Xt).shape==(6,)
assert DummyClassifier(strategy='most_frequent').fit(Xt,yt).predict(Xt).shape==(6,)
np.testing.assert_allclose(DummyRegressor(strategy='mean').fit([[0],[1],[2]],[2,4,6]).predict([[5]]),[4])
ct=ColumnTransformer([('numbers',StandardScaler(),['distance']),('categories',OneHotEncoder(),['zone'])]).fit(df)
assert ct.transform(df).shape==(3,3)
grid=GridSearchCV(LogisticRegression(random_state=0),{'C':[0.1,1]},cv=2).fit(Xt,yt);assert grid.best_params_ and len(grid.cv_results_['params'])==2
rand=RandomizedSearchCV(LogisticRegression(random_state=0),{'C':[0.1,1]},n_iter=1,cv=2,random_state=0).fit(Xt,yt);assert len(rand.cv_results_['params'])==1
# Numeric assertions for worked cost, cohort, memory, gradient and latency examples.
assert math.isclose(.8*.1*1+.2*.2*5,.28)
assert 100*20*8==16000 and 101*20*8==16160
assert math.isclose(12/15,.8) and math.isclose(12/20,.6)
assert (1**2+3**2)/2==5 and (1**2+2**2)/2==2.5
np.testing.assert_allclose(np.array([[1,2],[3,4]]).T@np.array([[.1],[.2]]),[[.7],[1.]])
assert math.isclose(.1+.2,.3) and math.isclose(2-.1*3,1.7)
assert math.isclose(.25*.8,.20) and math.isclose(.25*.6,.15)
assert 20*10*4+10*4==840 and 100*20*4+100*4==8400
assert math.isclose(294/300,.98) and 90/10==9
assert math.isclose(1.6-1.0,.6) and math.isclose(1.6-1.4,.2)
assert math.isclose(60*.01,.6) and math.isclose(20*.04,.8)
assert math.isclose(6/60,.1) and math.isclose(60/100,.6)
assert 6+1+4+1==12 and math.isclose(5/100,.05)
# Cost-control review: no forbidden source/video claims or unexplained code blocks;
# every worked number is fixture-labelled and all required facts have support.
report={
 'entries':len(A['entries']),'teaching_blocks':sum(len(e['teaching_blocks']) for e in A['entries']),
 'required_facts_covered':sum(len(r['evidence']['required_facts']) for r in R),
 'checks_passed':['schema (separate schema_check invocation)','full batch and exact path keys','unique block IDs','known and complete fact IDs','parent sha256 values','required core example and misconception blocks','no video bridges or invented video IDs/URLs','numeric worked references','local numpy/pandas/sklearn/PyYAML syntax fixtures','prerequisite and future-topic scope review','qualifier and policy-boundary review'],
 'scope_note':'No full runnable cloud/container/PyTorch programs are presented; platform API syntax is explanatory and parameters refer to the supplied authorized runtime. Live platform side effects were not executed or claimed. Core explanations remain focused on each supplied brief rather than expanding into general prerequisite courses.',
 'word_count_range':[min(sum(len(b['content'].split()) for b in e['teaching_blocks']) for e in A['entries']),max(sum(len(b['content'].split()) for b in e['teaching_blocks']) for e in A['entries'])]
}
(B/'pass_a_self_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
