import json, pathlib, tempfile, os, contextlib, io, builtins, sys, unittest
B=pathlib.Path('batches/glossary_batch_learn_python').resolve()
examples=json.loads((B/'pass_a_examples.json').read_text())
expected={1:["<class 'int'>","<class 'float'>","Notebook order","13.5","True"],2:['3.4','3','2','8','20','14'],3:['True','False','False','True','False','True'],4:['False','True','True'],5:['13.5','3','-3','3'],6:['Medium'],7:['blue'],8:['red','green',"['navy', 'green']","['red', 'navy', 'green', 'yellow']"],10:['3','5'],11:['Quantity: 3; cost: 13.50'],12:['Hello','Hello'],13:['notebook 3','pen 2'],14:['15.5'],15:['3 8'],16:['14','17'],17:['5','3','3'],18:['Enter a numeric quantity'],19:['1.0','1.0'],20:['12'],21:['10'],22:['5'],23:['notebook','pen','notebook 3','pen 2'],24:['[6, 4]','{3: 6, 2: 4}'],25:["[{'label': 'notebook', 'quantity': '3'}]"],27:['Selected: notebook!'],28:['1 notebook','2 pen','3 pencil'],29:['False','True','True'],30:['5'],31:['3.0','No real square root for this input'],32:['2',"{'quantities': [3, 5]}"],33:['3','2','5','4'],34:['0','2','4','5','3','1'],36:['14','24'],37:['14','# is text here'],40:['Cost 14'],41:['blue',"['red', '', 'blue']","['red', 'blue']",'label'],44:['Quantity supplied 0','Quantity absent'],45:["<class 'str'>","<class 'bytes'>",'café'],46:['notebook 3','pen 2'],47:['[[9, 2], [5]]','[[9, 2]]'],48:['blue 2'],49:["raw text ' 3 '",'converted quantity 3'],52:['Invalid quantity','After recovery'],53:['Leaving conversion','3'],54:['6'],55:['1','2','1'],60:["['blue']","['red']"],61:["['red', 'blue', 'green']","['blue', 'red', 'green']"],62:["[('red', 2), ('blue', 3)]"],63:['File missing'],65:['15'],66:['False','True'],68:['notebook 3'],69:['5'],70:['3','12'],71:['12'],72:['5'],73:['14'],74:['Order rejected'],75:["['blue']",'[]'],76:['[3, 2]',"<class 'list'>"],79:['Order(quantity=3)','Quantity: 3'],80:['café'],82:['café'],84:['3','-3'],88:['12'],89:['orders.csv True'],100:['3','2','None','3','True'],101:['3','2'],102:['10'],103:['3','[2]','[]','[3, 2]'],104:['10','[]','10','10'],105:['[3, 2, 5, 4]','14'],106:['[6, 4]','[6, 4]'],110:['12','None']}
results=[]
old=os.getcwd(); old_argv=sys.argv
try:
 for i,code in examples:
  with tempfile.TemporaryDirectory() as td:
   os.chdir(td)
   pathlib.Path('orders.csv').write_text('label,quantity\nnotebook,3\n')
   pathlib.Path('label.txt').write_text('café',encoding='utf-8')
   pathlib.Path('source.bin').write_bytes(b'\x00\xffexample')
   responses=iter(['blue','done'] if i==7 else ['notebook'])
   local_builtins=dict(vars(builtins));local_builtins['input']=lambda prompt='':next(responses)
   env={'__name__':'__main__','__builtins__':local_builtins}
   sys.argv=['example.py','orders.csv','--verbose'] if i==89 else ['example.py']
   output=io.StringIO()
   with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
    exec(compile(code,f'example_{i}.py','exec'),env)
    if i==107:
     result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(env['CostTests']))
     assert result.wasSuccessful() and result.testsRun==2
   lines=output.getvalue().splitlines()
   if i in expected:assert lines==expected[i],(i,lines,expected[i])
   if i==0:assert env['cost']==20 and env['quantity']==5
   if i==9:assert env['first']=={'red','blue'} and env['first']|env['second']=={'red','blue','green'}
   if i==43:assert lines==['No quantities','Quantities available']
   if i==56:assert env['output']==pathlib.Path('project')/'orders.csv'
   if i==57:assert lines==['Quantity rejected']
   if i==77:assert lines[1:4]==['True','3','None']
   if i==83:assert pathlib.Path('copy.bin').read_bytes()==pathlib.Path('source.bin').read_bytes()
   results.append({'concept_index':i,'execution':'PASS','output':lines})
finally:os.chdir(old);sys.argv=old_argv
(B/'pass_a_example_check_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('Executed and checked',len(results),'Python snippets in isolated disposable directories.')
