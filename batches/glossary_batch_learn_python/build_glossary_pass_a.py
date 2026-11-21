import json, hashlib, datetime, pathlib, re, ast
B = pathlib.Path('batches/glossary_batch_learn_python')
inputs = ['coverage_briefs.json', 'extracted_concepts.json', 'depth_classification.json']
briefs = json.loads((B/inputs[0]).read_text())
extracted = json.loads((B/inputs[1]).read_text())
depths = json.loads((B/inputs[2]).read_text())
cs = extracted['concepts']
bs = {(b['concept_id'], b['path_id']): b for b in briefs['briefs']}
ds = {(d['concept_id'], d['path_id']): d for d in depths['classifications']}
entries=[]
examples=[]
def add(i, intro, example, contrast, eids, mids, level='HIGH', reason=None):
    c=cs[i]; key=(c['concept_id'],c['path_id']); facts=bs[key]['evidence']['required_facts']
    blocks=[{'id':'tb1','purpose':'intro','content':intro,'fact_ids':[]},
            {'id':'tb2','purpose':'definition','content':facts[0]['statement'],'fact_ids':[facts[0]['id']]}]
    if len(facts)>1:
        blocks.append({'id':'tb3','purpose':'mechanism','content':' '.join(f['statement'] for f in facts[1:]),'fact_ids':[f['id'] for f in facts[1:]]})
    blocks.append({'id':'tb'+str(len(blocks)+1),'purpose':'example','content':example,'fact_ids':eids.split()})
    blocks.append({'id':'tb'+str(len(blocks)+1),'purpose':'misconception','content':contrast,'fact_ids':mids.split()})
    modes={'HIGH':['annotated_code','live_code'],'MEDIUM':['annotated_code'],'LOW':['annotated_code'],'NONE':[]}[level]
    if reason is None:
        reason={'HIGH':'Seeing the example execute, with the relevant values and control flow annotated, adds a changing-state demonstration to the text.', 'MEDIUM':'An annotated execution helps connect the interface to its result, although the written example supplies the essential explanation.', 'LOW':'The distinction fits in a short explanation and a static annotated example; moving demonstrations would add little.', 'NONE':'The definition and contextual contrast are sufficient; additional media would mostly repeat them.'}[level]
    notes=['Begin with this objective: '+bs[key]['learning_objective'],
           'Keep the example in the '+c['toc_location']['tile_title']+' tile focused on this operation, rather than introducing additional capabilities.']
    if c['blocked_knowledge_ids']:
        notes.append('Defer later concepts such as '+', '.join(c['blocked_knowledge_ids'][:3])+'.')
    external=[p for p in c['direct_prerequisite_ids'] if not p.startswith('python.')]
    if external: notes.append('Require the staged external foundations before this unit: '+', '.join(external)+'. Do not silently teach them here.')
    entries.append({'concept_id':key[0],'path_id':key[1],'teaching_blocks':blocks,'video_need':{'level':level,'reason':reason,'preferred_visual_modes':modes},'teaching_notes':notes})
    for match in re.finditer(r'```python\n(.*?)```',example,re.S): examples.append((i,match.group(1)))

add(0,"Suppose a small program needs to calculate the cost of three notebooks. You want names for the quantity, the unit price and the resulting cost, so the calculation can refer to the values you have chosen.",
'''Start with named numbers, then use them on the right of a later assignment:
```python
quantity = 3
unit_price = 4
cost = quantity * unit_price
quantity = 5
cost = quantity * unit_price
```
The first calculation binds cost to 12. Reassigning quantity binds it to 5; the following calculation then binds cost to 20. Read each assignment from its right-hand expression to its target name. Choose a name such as unit_price, not 2price. Quantity and quantity are different names, so changing capitalization is not a way to refer to the same binding.''',
    "Reassignment is not a request to keep calculating an earlier expression. It binds the target to the value of the right-hand expression at that assignment. In this example, calculate cost again after changing quantity if you want a new cost.", 'f1 f2 f3 f4', 'f1 f2')
add(1,"A program may need a whole-number quantity, a decimal price, a text label and a yes-or-no result. Before combining values, identify which kind each value represents.",
'''For a notebook calculation, inspect both the data and the result:
```python
quantity = 3
price = 4.5
label = "Notebook"
print(type(quantity))
print(type(price))
print(label + " order")
print(quantity * price)
print(quantity == 3)
```
The quantity has type int and the price has type float. Their product is the float 13.5. The text operation displays Notebook order, while the comparison displays True. You can also write a bool value directly as True or False. Here, a quoted label, a decimal price and a comparison result serve different needs in the same small program.''',
    "A number written inside quotes is text, not a numeric literal. Do not treat concatenating strings with + as the same operation as adding numeric values. Use type(value) when the kind of value is unclear.", 'f1 f2 f3 f4 f5 f6 f7', 'f1 f3 f6')
add(2,"You have 17 tokens to distribute in groups of five. The question includes both a total calculation and a grouping calculation, so choosing the operator matters.",
'''Compare the results of the related operations:
```python
print(17 / 5)
print(17 // 5)
print(17 % 5)
print(2 ** 3)
print((2 + 3) * 4)
print(2 + 3 * 4)
```
The first three results are 3.4, 3 and 2: division, the floored quotient and the remainder answer different questions. Exponentiation gives 8. The last two expressions give 20 and 14. Parentheses make the addition a group in the first of those expressions; without them, multiplication groups more tightly than addition. Trace the grouping before calculating the values.''',
    "// means a floored quotient, not ordinary division with an arbitrary display format. Likewise, parentheses change grouping rather than merely decorating an expression.", 'f1 f2 f3', 'f2 f3')
add(3,"A program deciding whether a quantity meets a limit needs a truth value, not another quantity. Translate the exact boundary in the question into a comparison.",
'''For a minimum quantity of three, compare the boundary itself:
```python
quantity = 3
print(quantity == 3)
print(quantity != 3)
print(quantity > 3)
print(quantity >= 3)
print(quantity < 3)
print(quantity <= 3)
```
These display True, False, False, True, False and True. The difference between > and >= is visible precisely at three. If the rule says at least three, equality belongs on the accepted side. If it says more than three, equality does not. Use the same boundary-focused reading for less than and at most.''',
    "Assignment with = and equality testing with == are different operations. An ordering test that includes equality must use <= or >= rather than the corresponding strict operator.", 'f1 f2 f3', 'f1 f2')
add(4,"Suppose a small eligibility calculation requires a sufficient quantity and a sufficient budget. There are two conditions, and the program needs one combined truth value.",
'''Name the individual conditions before combining them:
```python
quantity_ok = 3 >= 3
budget_ok = 12 >= 15
print(quantity_ok and budget_ok)
print(quantity_ok or budget_ok)
print(not budget_ok)
```
The outputs are False, True and True. Both conditions would need to be true for and. Only one needs to be true for or. In the and expression here, the second condition is needed because the first is true. In the or expression, the true first operand already determines the result, so the second operand is skipped. Parentheses can state the intended grouping when several logical operators appear together.''',
    "Do not read and and or as instructions that necessarily evaluate both operands. Short-circuiting can skip the second operand. For grouping, not binds more tightly than and, and and more tightly than or.", 'f1 f2 f3', 'f2 f3')
add(5,"A quantity may arrive as the text \"3\", while a calculation needs a number. Conversion gives you a new value suitable for the numeric calculation without requiring you to discard the original text.",
'''Keep the original and converted values under different names:
```python
quantity_text = "3"
quantity = int(quantity_text)
price = float("4.5")
print(quantity * price)
print(quantity_text)
print(int(-3.8))
print(str(quantity))
```
The product is 13.5, the original text still displays as 3, and converting -3.8 to int gives -3. The last call constructs text from the integer. Separately, int("three") raises ValueError rather than supplying the intended quantity. Treat suitable numeric text and an arbitrary word as different conversion inputs.''',
    "Converting a value does not automatically rebind the name holding the original. Also, conversion from float to int truncates toward zero; it is not a general rounding operation.", 'f1 f2 f3 f4 f5', 'f1 f5')
add(6,"A program classifying an order size needs to choose one response. The order in which you write the conditions determines which matching response is selected.",
'''Use aligned branches and an indented body for each:
```python
quantity = 5
if quantity >= 10:
    print("Large")
elif quantity >= 3:
    print("Medium")
else:
    print("Small")
```
The first test is false and the second is true, so this example displays Medium. At quantity 12, the first branch would run instead. A quantity below three reaches else because neither preceding condition is true. Read the branches from top to bottom, stopping at the first true condition rather than looking for every true condition independently.''',
    "An elif chain does not execute every branch whose condition could be true. Only the first true branch is selected, and else is used only when no condition is true.", 'f1 f2', 'f2')
add(7,"Suppose a program asks for a response until the user enters done. Repetition needs both a condition and a way for the value tested by that condition to change.",
'''A response loop obtains a fresh line inside its body:
```python
response = input("Enter a label, or done: ")
while response != "done":
    print(response)
    response = input("Enter a label, or done: ")
```
With entered lines blue and then done, the body displays blue once and stops on the next condition test. Entering done at the first prompt means the body never runs. The reassignment at the bottom obtains a new text response; without it, the test would keep using the old response. Input returns the line without its trailing newline.''',
    "A while loop is not guaranteed to run once. It tests before the body, and it can keep repeating if the values used in the condition never reach a stopping state.", 'f1 f2 f3 f4', 'f1 f2 f3')
add(8,"A program keeps three labels in a particular order, but one label needs correction and another must be added. A list supports both positional access and changes.",
'''Follow the list through a replacement and an append:
```python
labels = ["red", "blue", "green"]
print(labels[0])
print(labels[-1])
labels[1] = "navy"
labels.append("yellow")
print(labels[1:3])
print(labels)
```
The first and last original labels are red and green. After the updates, the list is ["red", "navy", "green", "yellow"]. The slice [1:3] contains navy and green, stopping before position three. Track positions separately from values: replacing an item changes the value at an existing position, whereas append places a value at the end.''',
    "The stop index in a slice is excluded. Selecting labels[1:3] does not include labels[3], and it returns a new list rather than being a single-item lookup.", 'f1 f2 f3 f4 f5', 'f2 f3')
add(9,"You want the distinct labels mentioned in two batches, not every repeated occurrence. A set answers that distinct-membership question without assigning sequence positions.",
'''Compare two sets of labels:
```python
first = set(["red", "blue", "red"])
second = {"blue", "green"}
print("red" in first)
print(first | second)
print(first & second)
empty = set()
```
The membership result is True. The union contains red, blue and green; the intersection contains blue. The repeated red in the original list contributes only one distinct element to first. Interpret the displayed sets by their members, not by the order in which a particular execution prints them. The separate empty set uses set().''',
    "{} is not an empty set; it creates a dictionary. A set is unordered, so it should not be read as a list with stable first and second positions.", 'f1 f2 f3 f4', 'f1 f2')
add(10,"A program needs to retrieve a quantity by its product label. This is a key-based lookup rather than a request for the first or second quantity in a sequence.",
'''Build a mapping, then update it by key:
```python
quantities = {"notebook": 3, "pen": 2}
print(quantities["notebook"])
quantities["notebook"] = 5
quantities["pencil"] = 4
print(quantities["notebook"])
```
The two lookups display 3 and 5. The existing notebook key keeps one associated value, now replaced by 5. The pencil assignment adds a new key-value pair. Looking up quantities["eraser"] separately would raise an error because this example never added that key. Decide which key you require before retrieving its value.''',
    "Adding a new value under an existing key does not create a second independent entry with that key. Dictionary keys are unique, and bracket lookup does not supply a fallback for an absent key.", 'f1 f2 f3', 'f1 f2 f3')
add(11,"Your program has calculated a cost, but the user needs a readable message containing both text and the number. Formatting puts values into a text result.",
'''Use braces for the expression and a colon for its presentation:
```python
quantity = 3
cost = 13.5
message = f"Quantity: {quantity}; cost: {cost:.2f}"
print(message)
```
This displays Quantity: 3; cost: 13.50. The literal text supplies the labels and punctuation, while the expressions inside braces supply the values. The .2f specification requests fixed-point presentation with two digits after the decimal point. You can use either single or double quotes around the string literal; choose delimiters that leave the intended text clear.''',
    "The two decimal digits belong to the formatted presentation. Do not confuse the displayed text 13.50 with an instruction that changes the numeric calculation itself.", 'f1 f2 f3', 'f3',level='LOW')
add(12,"A program repeats the same short greeting at several points. Give that action a function name so the definition and the moments of execution are easy to distinguish.",
'''Define the action once, then call it:
```python
def greet():
    print("Hello")

greet()
greet()
```
The definition binds greet to a function. Each call executes its indented body, so the example displays Hello twice. Read def greet(): as introducing the function and greet() as invoking it. The colon and indentation belong to the definition's block; the later calls are outside that block. This is the smallest useful distinction between making a function available and asking it to run.''',
    "A definition and a call are not interchangeable. Binding a name to a function is different from calling that function to execute its body.", 'f1 f2', 'f2')
add(13,"A greeting action should work with different labels. Rather than hard-coding one label in the body, give the function a parameter and supply an argument at each call.",
'''Match call values to definition names in order:
```python
def describe(label, quantity):
    print(label, quantity)

describe("notebook", 3)
describe("pen", 2)
```
Label and quantity are the parameters written in the definition. The first call supplies the arguments "notebook" and 3, so it displays notebook 3. The next call displays pen 2. For positional calls, the first value goes to the first parameter and the second to the second parameter. Trace those bindings before reading what the body does with them.''',
    "A parameter is not the particular value from one call. It is the name in the function definition; an argument is a value supplied when calling.", 'f1 f2 f3', 'f1 f3')
add(14,"A function calculates an order cost that the caller needs in a later calculation. Displaying the cost is not enough: the caller needs the calculated value as the call result.",
'''Return the expression and store the result:
```python
def order_cost(quantity, price):
    return quantity * price

cost = order_cost(3, 4.5)
print(cost + 2)
```
The function supplies 13.5 to the caller, so adding two displays 15.5. By contrast, a body containing only print(quantity * price) would display the product but reach its end without returning that product; its call result would be None. Return also ends the current call, so read it as both the result boundary and the stopping point for that call.''',
    "print and return have different roles. A displayed number is not automatically the function result, and a missing return does not implicitly return the last calculation.", 'f1 f2 f3 f4', 'f3 f4')
add(15,"A helper needs to give the caller both the smallest and largest quantity. A tuple can carry that fixed ordered pair as one returned value.",
'''Return a pair, then unpack it into two names:
```python
def bounds(values):
    return min(values), max(values)

smallest, largest = bounds([3, 8, 5])
print(smallest, largest)
one_item = (3,)
```
The call returns the tuple (3, 8), and unpacking binds smallest to 3 and largest to 8. Both targets correspond to the two values. The separate one_item example needs a comma to form a one-item tuple. Here the pair's order communicates which value is the lower bound and which is the upper bound.''',
    "A tuple is not a list whose items you can replace. Also, unpacking requires matching counts: a two-value pair is not unpacked into three ordinary targets.", 'f1 f2 f3 f4 f5', 'f1 f2 f3')
add(16,"An order helper normally uses the same fee, but some calls need another one. A default expresses the ordinary case while a keyword makes an override explicit.",
'''Define and call a helper with an optional fee:
```python
def cost(quantity, price, fee=2):
    return quantity * price + fee

print(cost(3, 4))
print(cost(3, 4, fee=5))
```
These display 14 and 17. The first call omits fee and uses its default. The second binds fee by name after the positional arguments. A call such as cost(3, 4, 2, fee=5) would bind fee twice and is not valid. Keep the distinction between required parameters and parameters with supplied defaults visible when reading the call.''',
    "Keyword arguments do not make duplicate bindings acceptable. Supply each parameter at most once, include required arguments and avoid keyword names the function does not accept.", 'f1 f2 f3', 'f2 f3',level='LOW')
add(17,"The module has a quantity name, and a helper also needs a quantity of its own. The same spelling can refer to different bindings depending on scope.",
'''Compare the local binding with an explicit module lookup:
```python
quantity = 3

def show():
    quantity = 5
    print(quantity)
    print(globals()["quantity"])

show()
print(quantity)
```
The output is 5, 3 and 3. The assignment in show changes its local binding, not the module binding. Without a local binding, ordinary lookup can read an enclosing or module name. A global quantity declaration would instead direct assignments to the module binding. Reading a name classified as local before assigning it can raise UnboundLocalError.''',
    "A same-named module value does not rescue a read of an unbound local name. Assigned function names are local throughout that function unless declared otherwise.", 'f1 f2 f3 f4 f5', 'f1 f4',level='MEDIUM')
add(18,"A quantity conversion should have a defined response when the entered text is unsuitable. Put the risky operation inside a protected body and name the failure you intend to handle.",
'''Handle invalid numeric text separately from the success path:
```python
text = "three"
try:
    quantity = int(text)
    print(quantity * 4)
except ValueError:
    print("Enter a numeric quantity")
```
This displays the recovery message. Once int(text) raises ValueError, the remaining print in the try body is skipped. With text "3", the product would display and the handler would be skipped. The handler matches this conversion failure; an exception of an unmatched type needs an outer matching handler or remains unhandled.''',
    "Recovery does not mean the failed conversion supplied a usable quantity. Remaining operations in that try body are skipped, so do not reason as though the multiplication ran after the failure.", 'f1 f2 f3 f4', 'f2 f3')
add(19,"A program needs a mathematical operation provided by a module. Importing determines which name you use to reach that operation.",
'''Compare the two import forms:
```python
import math
print(math.cos(0))
from math import cos
print(cos(0))
```
Both calls display 1.0. The first import binds the module name math, so the member is accessed as math.cos. The second binds cos directly in the importing namespace, so that call uses cos. Read the import statement before deciding whether the later call requires a module prefix. These are two ways to bind access to the same member, not two different cosine calculations.''',
    "import math does not by itself bind every member as a bare name. Use module.member for the module-import form, or import the particular member explicitly.", 'f1 f2 f3', 'f1 f2',level='MEDIUM')
add(20,"A working calculation is easier to review when its names and spacing communicate its structure. Apply a consistent style without changing the intended operations.",
'''A short helper can use readable names and four-space indentation:
```python
def order_cost(quantity, unit_price):
    cost = quantity * unit_price
    return cost

print(order_cost(3, 4))
```
The example displays 12. There are no extra spaces immediately inside the call parentheses or before its comma, and assignment uses a space on either side of =. Lowercase words separated with underscores make the function and variable names readable. For longer code, PEP 8 recommends 79-character code lines and 72-character comments or docstrings. These are style recommendations to keep in view as the program grows.''',
    "Do not turn a recommendation into a claim that every longer line is invalid syntax. Keep the recommended limits and the actual block indentation rule distinct.", 'f1 f2 f3 f4 f5', 'f5',level='LOW')
add(21,"Three quantities are stored in a list, and the program needs their total. A for loop processes each item while an accumulator keeps the running result.",
'''Initialize the total before visiting the items:
```python
quantities = [3, 2, 5]
total = 0
for quantity in quantities:
    total = total + quantity
print(total)
```
The successive totals are 3, 5 and 10, and the final output is 10. Each quantity is the next sequence item. The current total is reused on the right before the updated total is assigned. Keep initialization outside the body: the running value should continue from the previous item rather than begin again at zero for each one.''',
    "Putting total = 0 inside this loop would repeatedly discard the previous accumulated value. Distinguish preparing the accumulator once from updating it for each item.", 'f1 f2', 'f2')
add(22,"A quantity list includes a value to skip and a marker that means stop processing. The loop needs different actions for those two situations.",
'''Use conditional loop control:
```python
total = 0
for quantity in [3, 0, 2, -1, 8]:
    if quantity == -1:
        break
    if quantity == 0:
        continue
    total = total + quantity
print(total)
```
Zero skips the addition for that iteration. Minus one exits the loop, so eight is never added. The final total is 5. Trace the rest of the body only when neither control condition applies. In a nested loop, break would exit the innermost enclosing loop rather than every enclosing loop.''',
    "continue does not terminate the loop. It skips the remainder of the current body; break exits the innermost loop. Choose the operation that matches the stopping or skipping rule.", 'f1 f2 f3', 'f1 f2')
add(23,"An order mapping contains both labels and quantities. Decide whether the loop needs just the keys or the key-value pairs before choosing its traversal.",
'''Visit pairs explicitly when both parts are needed:
```python
quantities = {"notebook": 3, "pen": 2}
for label in quantities:
    print(label)
for label, quantity in quantities.items():
    print(label, quantity)
```
The first loop visits notebook and pen as keys. The second displays notebook 3 and pen 2 together. For lists and tuples, sequence order supplies the progression. For a set, there are no sequence positions to follow. The collection type therefore changes what a direct item traversal means; do not infer it from the variable name alone.''',
    "Iterating a dictionary directly does not yield its values or key-value tuples. Use mapping.items() when the loop needs each key together with its associated value.", 'f1 f2 f3 f4 f5', 'f4 f5')
add(24,"You want a new collection of doubled positive quantities from an existing list. A comprehension places the selection and the computed result in one expression.",
'''Read the source, condition and result expression together:
```python
quantities = [3, -1, 2]
doubled = [quantity * 2 for quantity in quantities if quantity > 0]
by_quantity = {quantity: quantity * 2 for quantity in quantities if quantity > 0}
print(doubled)
print(by_quantity)
```
The list contains [6, 4], and the dictionary maps 3 to 6 and 2 to 4. Minus one fails the condition and contributes nothing to either result. In the dictionary expression, identify the key expression before the colon and the value expression after it. Both constructions build new collections from the accepted items.''',
    "The condition selects which source items contribute; it is not a value placed in the result. Keep filtering separate from the expression that calculates each accepted result.", 'f1 f3', 'f1 f3')
add(25,"A small program now needs to read saved text and import a CSV table. Opening a file gives a resource that should be closed, and the selected mode determines the operation.",
'''For an illustrative CSV file whose contents are label,quantity followed by notebook,3, collect row dictionaries:
```python
import csv
with open("orders.csv", "r", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows)
```
The result contains one dictionary with label "notebook" and quantity "3". The header supplies the keys and is not returned as a data row. For ordinary text, source.read() reads the remaining contents; a text-mode destination.write(text) writes text. Managed opening closes the file after the body. If you open without with, explicitly close the file when finished.''',
    "Choosing w is not a harmless way to inspect a file: it replaces existing contents. Also, the CSV header normally becomes dictionary keys, not another returned data row.", 'f1 f2 f3 f4 f5 f6', 'f1 f6')
add(26,"Before storing an order-related value, ask what the program will do with it. Positional updates, a fixed pair, distinct membership and key lookup call for different collections.",
'''For example, keep editable quantities in [3, 2, 5], fixed lower and upper bounds in (2, 5), distinct labels in {"notebook", "pen"}, and quantities by label in {"notebook": 3, "pen": 2}. A list allows replacing the item at a position. A tuple keeps a fixed ordered group. A set supports asking whether a label belongs, without a sequence position. A dictionary supports retrieving a quantity by its label and preserves insertion order. Choose by the access and update needed, rather than by which literal is shortest.''',
    "Insertion order does not turn a dictionary into a positional sequence. Its lookup is by key. Sets likewise have no sequence positions, even if a particular display looks ordered.", 'f1 f2 f3 f4', 'f3 f4',level='LOW')
add(27,"An interactive order helper asks for a label and prints a compact response. Input obtains text; output controls how the response is displayed.",
'''Customize the separators in the display:
```python
label = input("Label: ")
print("Selected", label, sep=": ", end="!\\n")
```
If the user enters notebook, the output line is Selected: notebook! followed by a newline. Input supplies notebook as text without the entered line's trailing newline. With no customized sep or end, print separates multiple values with spaces and ends with a newline. Treat the returned input and the displayed prompt as distinct parts: the prompt asks the question, while the assigned result is the entered text.''',
    "input does not include its displayed prompt in the returned value. It also returns text, so a numeric calculation needs a suitable conversion rather than assuming entered digits already form a number.", 'f1 f2', 'f1',level='MEDIUM')
add(28,"A program should display numbered labels for the user. The numbering is a counter alongside each value, not a reason to manage a separate counter assignment yourself.",
'''Unpack each enumerate pair:
```python
labels = ["notebook", "pen", "pencil"]
for position, label in enumerate(labels, start=1):
    print(position, label)
```
This displays 1 notebook, 2 pen and 3 pencil. Enumerate supplies both the counter and the corresponding element. The start=1 setting changes the first counter from the default zero to one. Read position as the supplied display counter in this example; the original list still has its own zero-based indices.''',
    "Changing enumerate start does not change the list or its indexing rules. It changes the counter paired with each element.", 'f1 f2', 'f1 f2',level='MEDIUM')
add(29,"Two calculations intended to represent the same decimal amount may differ slightly as floats. State how close is close enough instead of assuming exact equality expresses the requirement.",
'''Compare using tolerances:
```python
import math
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.000001, 0.0, abs_tol=0.00001))
```
The results are False, True and True. Many decimal fractions do not have exact binary floating-point representations. The last comparison deliberately allows a small absolute difference near zero. Choose tolerances that match the example's requirement; the defaults are a relative tolerance of 1e-9 and an absolute tolerance of 0.0.''',
    "A comparison near zero does not gain a positive absolute allowance from the default abs_tol. Supply an appropriate positive absolute tolerance when a small nonzero difference should count as close.", 'f1 f2 f3', 'f3')
add(30,"A loop contains a condition, and a final report belongs after the loop. Indentation is what makes those three levels of grouping visible to Python.",
'''Trace the groups in this program:
```python
total = 0
for quantity in [3, -1, 2]:
    if quantity > 0:
        total = total + quantity
print(total)
```
The addition belongs to the if body, which belongs to the for body. The report is dedented to the outer level and displays 5 after the loop. Four spaces mark each level here. Moving the report into the loop would put it in a different group; moving the addition out of the if would remove that condition's grouping around the update.''',
    "Indentation is not only a visual preference. It determines grouping, and inconsistent indentation can be invalid. A colon begins a compound statement header whose multi-line body must be indented.", 'f1 f2 f3', 'f1 f2')
add(31,"A small numeric helper needs a real square root. Use the documented module function and recognize when the supplied value is outside that operation's real-valued scope.",
'''Call the function through math:
```python
import math
print(math.sqrt(9))
try:
    print(math.sqrt(-1.0))
except ValueError:
    print("No real square root for this input")
```
The first call displays 3.0. The second raises ValueError and reaches the handler. The contrast is about the accepted real-valued operation: these math functions operate on real rather than complex values. Identify the invalid argument instead of expecting a complex result from this function.''',
    "math.sqrt(-1.0) does not return a complex square root. It raises ValueError for this invalid real operation.", 'f1 f2', 'f2',level='MEDIUM')
add(32,"An order record contains a list of quantities inside a dictionary. Reaching one quantity requires selecting the outer entry before the inner position.",
'''Follow the path to the nested value:
```python
order = {"quantities": [3, 2]}
print(order["quantities"][1])
order["quantities"][1] = 5
print(order)
```
The first lookup displays 2. The outer key selects the list, and the inner index selects its second item. Assigning at that final index replaces 2 with 5, so the quantities list becomes [3, 5]. Read the selections one at a time rather than treating the whole expression as an unexplained special name.''',
    "An update at the final selected position changes that nested value, not necessarily the entire outer collection. Identify exactly which list index or dictionary key is the assignment target.", 'f1 f2', 'f2')
add(33,"A table-like list contains several rows, and each row has its own cells. A nested loop makes the row-by-row traversal explicit.",
'''Use the selected row as the inner source:
```python
rows = [[3, 2], [5, 4]]
for row in rows:
    for cell in row:
        print(cell)
```
The outputs are 3, 2, 5 and 4. For the first outer item, the inner loop visits both cells before the outer loop proceeds to the next row. Then the second row's inner traversal starts. Trace the current row before asking which cell is current; the inner loop source is different for each outer item in this example.''',
    "Nested row traversal is not a single synchronized step through both loops. The inner traversal runs for the current outer item before the outer traversal moves on.", 'f1 f2', 'f1 f2')
add(34,"A program needs every second integer position from zero up to a limit. Range expresses the start, excluded stop and step directly.",
'''Compare increasing and decreasing ranges:
```python
for index in range(0, 6, 2):
    print(index)
for index in range(5, 0, -2):
    print(index)
```
The first loop displays 0, 2 and 4; the second displays 5, 3 and 1. In neither case is the stop value included. A positive step continues below the stop, while a negative step continues above it. With range(3), the defaults instead supply zero, one and two. State the step explicitly when the task requires every second integer position.''',
    "The stop is excluded, not the last guaranteed value. A negative step also needs a direction compatible with reaching values above its stop, and a step of zero is not allowed.", 'f1 f2 f3', 'f1 f2')
add(35,"A saved program is ready to run outside an interactive session. Choose the interpreter explicitly, then pass the script path as its argument.",
'''Suppose report.py contains print("Ready"). An invocation of the form selected_python report.py runs it with the executable represented by selected_python. Replace that placeholder with the actual chosen executable, not a guessed runtime label. The message goes to standard output by default. For a script requesting an exit status, import sys and call sys.exit(0) for the illustrative successful status or sys.exit(2) for an illustrative abnormal status. Inspect the process status separately from its printed messages: they communicate different things.''',
    "A printed success message is not itself a process exit status. Zero indicates successful termination and a nonzero status indicates abnormal termination.", 'f1 f2 f3', 'f2 f3',reason='A terminal demonstration can show the chosen executable, script output and process termination as distinct parts of one run.')
add(36,"The same calculation may appear alone in an interactive session or on the right of an assignment. Distinguish evaluating a value from binding a name to that value.",
'''Trace grouping and current values:
```python
quantity = 3
cost = quantity * 4 + 2
quantity = 5
print(cost)
print((quantity + 1) * 4)
```
The displayed results are 14 and 24. The cost assignment evaluates its right side with quantity equal to 3. The later expression uses the now-current quantity of 5, with parentheses grouping its addition. In interactive mode, entering a non-None expression value by itself displays it. Assignment instead evaluates the right-hand expression and binds its result to the target.''',
    "Left-to-right evaluation does not erase operator precedence. Use precedence and parentheses to establish grouping while tracing evaluations in their specified order.", 'f1 f2 f3', 'f3')
add(37,"A reviewer needs to understand why a calculation includes a fee. A comment can record that reason, provided it remains accurate as the code changes.",
'''An inline comment can explain a chosen rule:
```python
quantity = 3
cost = quantity * 4 + 2  # This example includes a fixed fee of two.
print(cost)
print("# is text here")
```
The calculation displays 14. The comment extends to the physical line's end and is ignored by syntax. In the quoted string, # is ordinary text rather than the start of a comment. If the fee changes, revise or remove the comment so it does not contradict the code. Avoid adding an inline comment to every obvious assignment.''',
    "A comment is not evidence that the code implements its description. Read the operation itself, and keep the comment accurate rather than leaving an outdated explanation.", 'f1 f2 f3', 'f2 f3',level='LOW')
add(38,"For a quick calculation, use an interactive session instead of preparing a script. The prompts show where new commands and continuation lines belong.",
'''An illustrative session reads:
```text
>>> quantity = 3
>>> quantity * 4
12
```
Type quantity = 3 and then quantity * 4, without typing the >>> prompt characters. The later expression uses the binding created in the session and displays 12. A continuation prompt appears as ... when more input belongs to the command. In tutorial session examples, a line without a prompt is output, not another command to copy. Starting the interpreter without a script enters this interactive mode.''',
    "The prompt markers are not part of the Python source you enter. Distinguish prompted input from unprompted output before copying a session example.", 'f1 f2 f3', 'f3',level='MEDIUM')
add(39,"A saved source file has to be valid before its statements can execute. Keep the source, compilation step and runtime use of values conceptually separate.",
'''Consider a file containing quantity = 3 followed by cost = quantity * 4. At runtime the first assignment binds quantity to 3, and the second uses that current value to bind cost to 12. Invalid source syntax instead raises SyntaxError when compilation is attempted. In CPython, compilation produces bytecode used by the interpreter. Top-level module statements execute on first import or when the file is run as a script. This model explains where parsing validity and changing runtime bindings fit without requiring you to inspect bytecode instructions.''',
    "Bytecode is a CPython implementation detail, not a guarantee about every Python implementation. Do not turn this explanatory model into a universal claim about internal execution machinery.", 'f1 f2 f3 f4', 'f2',level='LOW')
add(40,"A long calculation or call needs several physical lines for readability. Delimiters allow continuation without introducing another block of statements.",
'''Keep one expression inside its parentheses:
```python
cost = (
    3 * 4
    + 2
)
print(
    "Cost",
    cost,
)
```
The result displayed is Cost 14. The expression remains intact across its physical lines. The call uses a hanging indent for its arguments. Parentheses, square brackets and braces allow this kind of implicit continuation without backslashes. Read the opening and closing delimiters before interpreting continuation whitespace as a block boundary.''',
    "Continuation indentation is not the rule that groups compound-statement bodies. Preserve delimiters and the expression when splitting a long call; do not mistake it for a newly indented suite.", 'f1 f2 f3', 'f2',level='LOW')
add(41,"Entered labels may contain surrounding spaces and inconsistent letter case. Separate cleanup at the edges from splitting text into fields.",
'''Compare explicit delimiters with whitespace splitting:
```python
text = "  Blue  "
print(text.strip().lower())
print("red,,blue".split(","))
print("  red   blue  ".split())
print("xylabelyx".strip("xy"))
```
The outputs represent blue, ["red", "", "blue"], ["red", "blue"] and label. The explicit comma preserves an empty field between repeated commas. Whitespace splitting groups runs of whitespace and omits leading and trailing empty fields. In the final call, x and y are removable edge characters, not a required literal prefix or suffix. Interior whitespace is not removed by strip().''',
    "strip(\"xy\") does not mean remove exactly one prefix xy and one suffix xy. Its argument describes removable characters at the edges; it is not a literal substring-removal rule.", 'f1 f2 f3 f4 f5', 'f1 f2 f4 f5')
add(42,"A program can fail before execution begins or during a syntactically valid operation. The error report tells you which kind of investigation is needed.",
'''Compare two small cases in isolation. The source if quantity > 0 without a following colon is invalid syntax; repair the reported syntax before tracing its execution. The valid expression int("three") instead raises ValueError when executed because the text is unsuitable. A syntax report identifies where the parser detected the problem. A runtime report identifies an exception type and explanation. Read those details before deciding whether to repair source structure or investigate a supplied runtime value.''',
    "Invalid source syntax does not produce an executable code object for that source. Do not invent a runtime branch trace for it before repairing the syntax.", 'f1 f2 f3', 'f3',level='LOW')
add(43,"A helper should report when its quantity collection is empty. A truth test can express that guard directly, without comparing the collection to a boolean literal.",
'''Use the collection itself as the condition:
```python
quantities = []
if not quantities:
    print("No quantities")
quantities = [3]
if quantities:
    print("Quantities available")
```
Both messages display at their corresponding stages. Empty built-in collections have false truth values; nonempty ones have true truth values. The same distinction applies to empty and nonempty built-in strings, while zero is false and nonzero numbers are true. False and None are also false in a truth test.''',
    "Truth testing does not require collection == True. Use if collection or if not collection for the intended nonempty or empty guard.", 'f1 f2', 'f2',level='LOW')
add(44,"A quantity of zero may be a legitimate result, while None represents absence. A guard that rejects every false value would fail to distinguish those cases.",
'''Test absence explicitly:
```python
quantity = 0
if quantity is not None:
    print("Quantity supplied", quantity)
quantity = None
if quantity is None:
    print("Quantity absent")
```
Both messages display. None is the singleton commonly used for an absent value. Identity testing with is asks whether the operands are the same object, and is not asks whether they differ. In this example the first guard accepts zero because zero is not None. Choose the absence test rather than a broad truth test when zero or an empty value is allowed by the task.''',
    "False truth and absence are not interchangeable. A truth test also rejects legitimate zero or empty values; value is None targets the absence marker specifically.", 'f1 f2 f3', 'f3',level='LOW')
add(45,"A label is text inside the program but may need an encoded binary payload at a boundary. Keep the text and its encoded bytes as distinct values.",
'''Encode, then decode with the matching encoding:
```python
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")
print(type(text))
print(type(payload))
print(restored)
```
The types are str and bytes, and the restored text is café. Encoding produces bytes from Unicode text; decoding interprets bytes as text under an encoding. A payload whose bytes are invalid for the chosen decoding raises UnicodeDecodeError. Match the decoding encoding to the encoded data rather than treating any bytes value as already-readable text.''',
    "bytes and str are not two names for the same kind of value. Recovering the intended text requires a matching decoding encoding, and invalid bytes can cause a decoding failure.", 'f1 f2 f3 f4', 'f1 f3 f4')
add(46,"Two lists contain labels and corresponding quantities. Parallel traversal pairs the entries, but it also has a rule for unequal lengths.",
'''Unpack each paired tuple:
```python
labels = ["notebook", "pen", "pencil"]
quantities = [3, 2]
for label, quantity in zip(labels, quantities):
    print(label, quantity)
```
This displays notebook 3 and pen 2. The trailing pencil has no corresponding quantity, so it is omitted. Zip pairs the corresponding elements and stops at the shorter input by default. Before using the pairs as a complete report, account for that stopping rule rather than assuming every entry in the longer list was visited.''',
    "Zip does not supply a missing value for unmatched trailing entries by default. Stopping at the shortest input can omit data from a longer one.", 'f1 f2 f3', 'f3',level='MEDIUM')
add(47,"A helper receives a list, and you want to know whether changing it can affect the caller. Follow object sharing, not just the different names used in the code.",
'''Compare an alias and a shallow copy:
```python
original = [[3, 2]]
alias = original
copied = original.copy()
alias.append([5])
copied[0][0] = 9
print(original)
print(copied)
```
Original becomes [[9, 2], [5]], while copied becomes [[9, 2]]. Alias and original name the same outer list, so appending through alias is visible through original. Copied has its own outer list but shares the original inner list. The nested update is consequently visible in both. A list slice original[:] likewise makes a shallow copy.''',
    "A new name is not automatically a new object. A shallow copy separates top-level list changes, but it does not make every nested mutable element independent.", 'f1 f2 f3', 'f1 f3')
add(48,"Repeated labels need to be summarized by frequency. A Counter gives a label-to-count mapping and can identify a most frequent entry.",
'''Count labels and guard the result before selecting its first pair:
```python
from collections import Counter
counts = Counter(["blue", "red", "blue"])
pairs = counts.most_common(1)
if pairs:
    label, count = pairs[0]
    print(label, count)
```
This displays blue 2. Most_common(1) returns a list containing the selected pair, not the pair alone. For an empty counter that list is empty, so the guard matters. Pairs are ordered by descending count, and tied counts follow first encounter. Use that documented rule when interpreting a tie rather than assigning a separate ranking meaning to it.''',
    "Do not index the first most_common result without checking that it exists. An empty counter returns an empty list rather than a fabricated winning label.", 'f1 f2 f3', 'f2 f3')
add(49,"A conversion is producing an unexpected result. Add a small, labeled observation at the point where the value is available instead of guessing its state from the final output.",
'''Inspect the text before conversion and the number afterward:
```python
text = " 3 "
print("raw text", repr(text))
quantity = int(text)
print("converted quantity", quantity)
```
The representation exposes the surrounding spaces and quotes around the text. The second diagnostic displays converted quantity 3. These observations refer to the values at those execution points. Move an observation only after deciding which binding or operation you want to investigate, and remove the print call when that diagnostic output is no longer needed.''',
    "A diagnostic placed before a later reassignment cannot reveal the later value. Align the observation point with the binding or operation you are investigating.", 'f1 f2 f3', 'f3')
add(50,"A reusable helper needs documentation that callers can inspect. Put its purpose and calling details in a docstring rather than leaving the interface implicit.",
'''The first string in the function body supplies its docstring:
```python
def cost(quantity, unit_price):
    """Calculate an order cost.

    Arguments are numeric quantity and unit_price.
    Return their product.
    """
    return quantity * unit_price

help(cost)
```
Help displays the function's signature and documentation. Document applicable exceptions as part of an interface when they apply, along with arguments and return values. Public modules, classes and methods also need docstrings. In this example the concise first line introduces purpose, and the blank line separates it from the calling details.''',
    "A string placed later in the body is not the function's first-statement docstring. Put interface documentation first, and keep it consistent with the actual arguments and returned value.", 'f1 f2 f3 f4', 'f2 f3',level='LOW')
add(51,"An error handler names Exception, but not every built-in exceptional event belongs under that class. Read the hierarchy before deciding which scope the handler covers.",
'''For a missing file, the relevant chain is BaseException, Exception, OSError, FileNotFoundError. ValueError is another subclass of Exception. In contrast, KeyboardInterrupt, SystemExit and GeneratorExit sit directly under BaseException rather than Exception. Thus a handler for Exception covers ordinary application failures from that branch, not those three direct BaseException subclasses. Sketching these relationships makes the distinction visible without treating all failure names as unrelated labels.''',
    "Exception is not the root of the whole hierarchy. BaseException is the root, and the distinction matters when reasoning about which exception classes a handler matches.", 'f1 f2 f3', 'f1 f3',reason='A hierarchy diagram can show parent and subclass relationships more clearly than a flat list of exception names.')
add(52,"A conversion helper fails inside a caller's protected operation. Track where the exception travels and where execution resumes after recovery.",
'''Let an outer handler recover:
```python
def quantity(text):
    return int(text)

try:
    value = quantity("three")
    print("Converted", value)
except ValueError:
    print("Invalid quantity")
print("After recovery")
```
The conversion failure propagates from the helper to the caller's matching handler. The converted-value print is skipped, and execution continues after the try/except statement, displaying After recovery. Matching includes subclasses and examines handlers in written order. Without a matching handler in the call chain, the exception would be unhandled.''',
    "Recovery does not resume at the failed conversion. It continues after the try/except statement; the skipped operations in the protected body are not retried automatically.", 'f1 f2 f3 f4', 'f1 f4',level='MEDIUM')
add(53,"A protected operation has a cleanup action that must be considered when it finishes normally, fails or returns. Finally makes that exit action explicit.",
'''Trace cleanup on a returning path:
```python
def read_quantity(text):
    try:
        return int(text)
    finally:
        print("Leaving conversion")

print(read_quantity("3"))
```
The cleanup message appears before the returned 3 is displayed. With unsuitable numeric text, the finally body still executes and the unhandled ValueError is re-raised after it completes normally. Place supplied release operations in this aligned body when that is the intended cleanup boundary. Keep the exit action distinct from the calculation's return value.''',
    "A return inside finally can replace a pending return or suppress a pending exception. Do not add one as though it were a harmless cleanup statement.", 'f1 f2 f3', 'f3',level='MEDIUM')
add(54,"A helper should apply a caller-selected calculation. Passing the function itself lets the receiving helper call it with the value it is processing.",
'''Keep the bare function distinct from a call result:
```python
def double(value):
    return value * 2

def apply(operation, value):
    return operation(value)

chosen = double
print(apply(chosen, 3))
```
The output is 6. The definition binds double to a function object, chosen stores that callable, and apply invokes it through its operation parameter. Passing double(3) instead would pass the result of an earlier call, not the function object needed here. Follow the call parentheses carefully to see when execution actually happens.''',
    "A bare function name and name(arguments) are different values in this context: the former refers to the function, while the latter performs a call. Pass the function when the helper needs to invoke it later.", 'f1 f2 f3 f4', 'f1 f4')
add(55,"A factory can create a small counter with state belonging to that factory call. A returned nested function can keep using its enclosing binding.",
'''Rebind enclosing state explicitly:
```python
def make_counter():
    count = 0
    def advance():
        nonlocal count
        count = count + 1
        return count
    return advance

counter = make_counter()
print(counter())
print(counter())
other = make_counter()
print(other())
```
The outputs are 1, 2 and 1. Counter uses the enclosing count after its creating call has finished. Nonlocal directs the update to that existing enclosing binding. The separate factory call has its own local state, so other begins from its own zero rather than continuing counter's state.''',
    "An ordinary assignment in the nested function is not automatically an enclosing-scope rebind. Use nonlocal for the existing nearest enclosing binding when that is the intended state update.", 'f1 f2 f3 f4', 'f1 f3')
add(56,"A program needs an output path under a chosen directory. Construct the path deliberately and distinguish a relative child from an absolute replacement.",
'''For a relative illustrative base:
```python
from pathlib import Path
base = Path("project")
output = base / "orders.csv"
print(output)
```
The result represents project/orders.csv using the platform's path conventions. Because this base is relative, its interpretation depends on the working directory. A chosen explicit base directory can avoid that unintended dependence. An absolute right operand instead replaces the preceding base; on POSIX, Path("/work/project") / "/tmp/orders.csv" represents /tmp/orders.csv, not a path below /work/project. Treat that platform-specific example as a path-construction demonstration, not a file operation.''',
    "The / operator does not guarantee that an absolute child stays under a preceding base. Trace whether each operand is relative or absolute before relying on the destination.", 'f1 f2 f3', 'f2 f3',reason='A path diagram and annotated construction can show when a child is appended and when an absolute operand replaces the base.')
add(57,"A helper requires a nonnegative quantity. If a value violates that requirement, signal a specific failure with context instead of producing a misleading result.",
'''Raise at the value-contract boundary:
```python
def cost(quantity):
    if quantity < 0:
        raise ValueError("quantity must be nonnegative")
    return quantity * 4

try:
    cost(-1)
except ValueError:
    print("Quantity rejected")
```
The handler displays Quantity rejected. The supplied numeric argument has an appropriate type but an inappropriate value for this example's stated requirement. The message provides context, and the specific exception supports a precise handler. Choose a more precise exception where the operation's documented failure calls for one.''',
    "Raising is not merely displaying an error message. It signals an exception that needs matching handling, and specificity lets callers distinguish the intended failure.", 'f1 f2 f3', 'f1 f3')
add(58,"A helper call fails, and the report contains several source locations. Read the report as a path to the immediate failing operation, not as an undifferentiated wall of text.",
'''Suppose a script calls read_quantity("three"), and that helper's return int(text) fails. The final report line identifies ValueError and its explanatory message. The preceding frames identify the script call and the helper's conversion line, including file and line information. Follow the call chain down to the most recent failing operation, then inspect that statement and its input. This separates the place that requested the work from the operation that immediately failed.''',
    "The caller's frame is useful context, but it need not be the immediate failing statement. Use the most recent failing frame together with the final exception type and message.", 'f1 f2 f3', 'f2 f3',reason='An annotated traceback can connect each frame to the source call chain and highlight the final failing statement.')
add(59,"A suspicious branch needs inspection while the program is paused. The debugger lets you see current values and choose whether to step into a call.",
'''In a script, place breakpoint() after quantity = 3 and before the branch using quantity. At the default pdb prompt, p quantity prints the current value and l lists nearby source. Use n to execute the next line without stepping into a called function, or s to step into a call. The command b line_number sets a breakpoint at the chosen source line; replace the placeholder with an actual line number. Use c to continue until another breakpoint or termination. Inspect the branch-controlling values at the pause rather than inferring them from an eventual report.''',
    "n and s do not have the same stepping behavior. Choose whether to enter a called function, and do not confuse debugger commands with Python source statements.", 'f1 f2 f3 f4', 'f3',reason='A debugger demonstration shows pausing, inspecting variables and stepping through changing execution state.')
add(60,"A helper that appends labels should create fresh storage when the caller omits its list. A mutable default can unintentionally carry earlier modifications into later calls.",
'''Create the list during the call:
```python
def add_label(label, labels=None):
    if labels is None:
        labels = []
    labels.append(label)
    return labels

print(add_label("blue"))
print(add_label("red"))
```
The results are ["blue"] and ["red"]. Each omitted-list call enters the None branch and creates a fresh list. A definition with labels=[] instead evaluates that default once at definition time; appending to it can retain changes across calls. Keep a caller-supplied list and the omitted-argument case conceptually separate.''',
    "A mutable default is not rebuilt automatically on every call. The None guard is what creates fresh per-call state in this pattern.", 'f1 f2', 'f1 f2')
add(61,"A list of order records should be arranged by quantity without changing the original list. A key function supplies the value used for each record's comparison.",
'''Name the key calculation:
```python
def quantity_key(record):
    return record["quantity"]

records = [{"label": "blue", "quantity": 3}, {"label": "red", "quantity": 2}, {"label": "green", "quantity": 3}]
ordered = sorted(records, key=quantity_key)
print([record["label"] for record in ordered])
print([record["label"] for record in records])
```
The outputs are ["red", "blue", "green"] and ["blue", "red", "green"]. The equal-quantity blue and green entries keep their relative order. Reverse=True requests reverse ordering, and str.lower can act as a lowercase text key when sorting labels rather than records.''',
    "The key function returns the comparison key, not a rearranged record. Sorted returns a new list and does not mutate the original list; equal keys retain relative order.", 'f1 f2 f3 f4', 'f1 f2 f3')
add(62,"A short sorting key may not need a separately named function. A lambda can express that one-expression calculation at the call site.",
'''Sort pairs by their quantity:
```python
pairs = [("blue", 3), ("red", 2)]
ordered = sorted(pairs, key=lambda pair: pair[1])
print(ordered)
```
The result is [("red", 2), ("blue", 3)]. The lambda takes a pair and supplies its second item's value as the key. Its result is the value of the expression after the colon. Read it like a tiny anonymous function, not a separate loop or a block of statements.''',
    "A lambda is restricted to one expression. If the calculation needs a statement body, do not force that body into lambda syntax.", 'f1 f2', 'f2',level='LOW')
add(63,"A file import should report a missing file differently from another operating-system failure. Handler order determines whether the specific recovery can be reached.",
'''Place the subclass handler first:
```python
try:
    with open("missing-example.txt", "r") as source:
        print(source.read())
except FileNotFoundError:
    print("File missing")
except OSError:
    print("Other file operation failure")
```
For a missing file, the first handler runs. FileNotFoundError is a subclass of OSError, so placing the broad OSError handler first would match that failure before the specific response. The first matching handler is selected; order the specific branch before its parent when their recovery actions differ.''',
    "Handlers are not ranked automatically by specificity. Written order matters, so a broad parent handler can make a later subclass-specific handler unreachable for its matching failures.", 'f1 f2 f3', 'f1 f2 f3')
add(64,"A failed operation might reflect invalid input, a code typo or inadequate access rights. Choose a response based on the reported cause rather than blaming every failure on the input.",
'''Compare three isolated reports. ValueError from int("three") identifies unsuitable numeric text, so request correction of that input. NameError for a misspelled quantity name means the implementation cannot find the name, so correct the code rather than rejecting valid user text. PermissionError during a file operation reports inadequate access rights, which needs an access-failure report. These cases belong to different diagnostic categories even when they interrupt the same larger task.''',
    "Do not treat PermissionError as proof that the path or implementation is inherently wrong. Report inadequate access rights, just as a misspelled implementation name calls for code correction rather than input rejection.", 'f1 f2 f3', 'f2 f3',level='LOW')
add(65,"A wrapper should pass through the caller's arguments without manually duplicating every parameter. Collection and expansion syntax represent the two sides of that forwarding.",
'''Collect arguments in the wrapper and expand them at the target call:
```python
def target(quantity, price=4):
    return quantity * price

def wrapper(*args, **kwargs):
    return target(*args, **kwargs)

print(wrapper(3, price=5))
```
The result is 15. Inside wrapper, args contains the remaining positional arguments as a tuple and kwargs contains additional keyword arguments as a dictionary. The target call expands them back into positional and keyword bindings. The wrapper should not add another price argument when the caller already supplied price.''',
    "Forwarding does not relax the rule against binding one parameter twice. Adding an explicit argument alongside expanded caller arguments can duplicate a binding.", 'f1 f2 f3 f4', 'f2 f4',level='MEDIUM')
add(66,"A program needs separate objects belonging to the same kind. Start by distinguishing the class definition from the instances created by calls.",
'''Define a minimal class and compare instances:
```python
class Order:
    pass

first = Order()
second = Order()
alias = first
print(first is second)
print(first is alias)
```
The results are False and True. The class statement creates the class object Order, and the two calls create distinct instances. Alias refers to the same instance as first. The pass statement supplies the otherwise empty class body. Identity asks whether references point to the same object, not merely whether their objects were made by the same class.''',
    "Two ordinary calls to the same class do not produce shared identity. A shared alias and two distinct instances are different cases.", 'f1 f2 f3', 'f2 f3')
add(67,"A program is about to create a report file. The mode choice determines whether an existing report is read, replaced, extended or protected against replacement.",
'''Suppose report.txt already contains First. Opening it with r reads that content. Opening with a and writing Second appends rather than replacing First. Opening with w truncates the existing content before the new writing, while x fails with FileExistsError because the destination already exists. For a report that must be new, use x and handle FileExistsError as the existing-destination case. With no mode supplied, open uses r. Make the choice before opening, not after discovering that earlier contents disappeared.''',
    "Do not recover from an exclusive-create collision by silently switching to w. That would change the requirement from avoiding replacement to truncating an existing file.", 'f1 f2 f3 f4 f5', 'f2 f4 f5',reason='A controlled before-and-after file demonstration shows read, truncation, append and exclusive-create behavior.')
add(68,"Each order object needs its own label and quantity when it is created. Initialization binds those supplied constructor values to the new instance's attributes.",
'''Store arguments on self:
```python
class Order:
    def __init__(self, label, quantity):
        self.label = label
        self.quantity = quantity

order = Order("notebook", 3)
print(order.label, order.quantity)
```
The output is notebook 3. Instantiation automatically invokes __init__ on the new instance with the constructor arguments. Self refers to that instance, while label and quantity are the supplied parameter bindings. The assignments establish its attributes, so later instance access retrieves the stored values.''',
    "__init__ initializes an already-created instance. It is not a function for returning a replacement object as the result of construction.", 'f1 f2 f3', 'f3')
add(69,"An order object needs an operation that changes its quantity. An instance method receives the object so it can use that object's current state.",
'''Read and update the receiving instance:
```python
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def add(self, amount):
        self.quantity = self.quantity + amount

order = Order(3)
order.add(2)
print(order.quantity)
```
The final quantity is 5. In order.add(2), order is passed implicitly as self and 2 is passed as amount. The method reads self.quantity, calculates the new value and assigns it back to that same instance's attribute. Trace the receiving instance before tracing the change.''',
    "The call order.add(2) does not require you to pass order again as an ordinary argument. The instance is already supplied implicitly as self.", 'f1 f2 f3', 'f1 f3')
add(70,"A class may offer an alternative constructor and a calculation that needs no object state. Distinguish those interfaces from ordinary instance methods.",
'''Compare the implicit arguments:
```python
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    @classmethod
    def from_text(cls, text):
        return cls(int(text))
    @staticmethod
    def cost(quantity, price):
        return quantity * price

order = Order.from_text("3")
print(order.quantity)
print(Order.cost(3, 4))
```
The outputs are 3 and 12. The class method receives cls implicitly and constructs through it. The static method receives neither an implicit instance nor a class. An ordinary instance method instead receives the instance and can use its state.''',
    "Adding a method inside a class does not make all three calling conventions identical. Classmethod supplies cls; staticmethod supplies no implicit first argument.", 'f1 f2 f3', 'f2 f3')
add(71,"An order report can use another object to perform a calculation. Store that collaborator and delegate the operation rather than putting every action in one class.",
'''Call through the stored collaborator:
```python
class Calculator:
    def cost(self, quantity):
        return quantity * 4

class Report:
    def __init__(self, calculator):
        self.calculator = calculator
    def total(self, quantity):
        return self.calculator.cost(quantity)

report = Report(Calculator())
print(report.total(3))
```
The result is 12. Report holds a Calculator object as instance data and delegates the calculation through self.calculator.cost(quantity). Follow the attribute to the collaborator before reading its method call. This demonstrates an object holding and using another object.''',
    "A collaborator attribute is an object reference, not the earlier result of its method. Delegate through the stored object when the receiving method needs work performed.", 'f1 f2', 'f1 f2')
add(72,"Clients of an order object need a clear public operation. Supporting state can use a non-public naming convention without pretending the name enforces access control.",
'''Expose an operation over supporting attributes:
```python
class Order:
    def __init__(self, quantity):
        self._quantity = quantity
    def add(self, amount):
        self._quantity = self._quantity + amount
        return self._quantity

order = Order(3)
print(order.add(2))
```
This displays 5. The public add method operates on the receiving instance's supporting _quantity attribute. The leading underscore convention signals non-public implementation use. Clients are expected to use the public interface rather than managing that supporting state directly.''',
    "A leading underscore does not make an attribute truly inaccessible. It signals a convention, not enforced access protection.", 'f1 f2 f3 f4', 'f1 f2',level='LOW')
add(73,"A specialized order keeps a base quantity and adds a fee. Inherited initialization and overridden methods need explicit delegation where the specialized operation uses base behavior.",
'''Use super inside the derived methods:
```python
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def cost(self):
        return self.quantity * 4

class FeeOrder(Order):
    def __init__(self, quantity, fee):
        super().__init__(quantity)
        self.fee = fee
    def cost(self):
        return super().cost() + self.fee

print(FeeOrder(3, 2).cost())
```
The result is 14. The derived initialization runs inherited initialization before adding fee. Its cost override delegates to the next class in method resolution order, then adds the specialized amount.''',
    "Super is a delegation of lookup to the next class in method resolution order. Do not describe it as an unconditional call to a fixed named parent in every possible hierarchy.", 'f1 f2 f3', 'f2')
add(74,"An application wants a named failure for its own order rule. A custom exception gives callers a specific class to raise and handle.",
'''Define the failure and catch it at a surrounding boundary:
```python
class InvalidOrder(Exception):
    pass

def check_quantity(quantity):
    if quantity < 0:
        raise InvalidOrder("negative quantity")
    return quantity

try:
    check_quantity(-1)
except InvalidOrder:
    print("Order rejected")
```
The recovery displays Order rejected. The class derives from Exception and the pass statement supplies its body. Raising an instance with a message signals the application-specific failure, while the surrounding handler names that class. This keeps the failure identity visible in both the producer and the recovery boundary.''',
    "A custom failure name is not merely a printed label. Define an exception class, raise it and handle that class at the intended boundary.", 'f1 f2', 'f1 f2')
add(75,"Two order objects each need their own list of labels. Putting a mutable list in the class body instead would give them shared state unless an instance shadows it.",
'''Initialize separate lists on each instance:
```python
class Order:
    def __init__(self):
        self.labels = []

first = Order()
second = Order()
first.labels.append("blue")
print(first.labels)
print(second.labels)
```
The outputs are ["blue"] and []. Each __init__ call assigned a new instance list. If labels = [] were instead stored only in the class body, the list would be shared by instances that had not shadowed it. Ask where the attribute is created before deciding whether an update is isolated.''',
    "Different instances do not guarantee separate mutable class attributes. Store per-instance mutable data on self during initialization when independent state is required.", 'f1 f2 f3', 'f2 f3')
add(76,"A program exchanges JSON text with another component. Use Python values at the calculation boundary and serialization or deserialization at the text boundary.",
'''Inspect a round trip with a tuple value:
```python
import json
record = {"quantities": (3, 2), "active": True}
text = json.dumps(record)
restored = json.loads(text)
print(restored["quantities"])
print(type(restored["quantities"]))
```
The restored quantities are [3, 2], with type list. Lists and tuples both encode as arrays, and those arrays decode as lists. Supported default values include dictionaries, strings, numbers, booleans and None as well. JSON object keys are strings, so a non-string Python dictionary key need not retain its original type through a round trip.''',
    "A successful round trip is not a guarantee that every Python type stays identical. Tuples decode as lists, and non-string dictionary keys may lose their original key type.", 'f1 f2 f3 f4', 'f3 f4')
add(77,"A helper receives an object and needs to inspect its available interface. Use runtime inspection with the documented limits instead of assuming every visible name is public.",
'''Inspect an illustrative instance:
```python
class Order:
    def __init__(self):
        self.quantity = 3

order = Order()
print(type(order))
print(isinstance(order, Order))
print(getattr(order, "quantity"))
print(getattr(order, "missing", None))
print(dir(order))
```
Isinstance is True, the quantity is 3 and the fallback for missing is None. Isinstance also accepts instances of subclasses. Dir attempts to list relevant names but is not guaranteed complete. Names beginning with an underscore conventionally signal internal use rather than a public interface.''',
    "Dir is an inspection aid, not a guaranteed complete public-API specification. Read underscore names as conventionally internal and use documented interfaces rather than every discovered attribute.", 'f1 f2 f3 f4 f5', 'f3 f5')
add(78,"A program places a completed report in an output directory. Directory construction, traversal and rename all need their documented path and platform rules.",
'''Construct the destination from the chosen directory. If directory represents an explicit output directory, directory.mkdir(parents=True, exist_ok=True) allows that directory to exist and creates missing parents. For a supplied source and filename, target = directory / filename followed by source.rename(target) uses the constructed target rather than a bare relative filename. Inspect directory.iterdir() as an arbitrary-order traversal of immediate entries. Before any rename, inspect whether the target already exists: replacement behavior differs between Unix and Windows.''',
    "A relative rename target is resolved against the working directory, not the source's parent. Rename can replace an existing target file on Unix when permitted, whereas Windows raises FileExistsError for an existing target.", 'f1 f2 f3 f4 f5', 'f3 f4',reason='A controlled filesystem demonstration can show constructed destinations and before-and-after directory contents, with platform-specific behavior identified.')
add(79,"An order object needs a convenient display for users and a more explicit representation for inspection. Special methods let those two representations be defined separately.",
'''Provide both string results:
```python
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def __repr__(self):
        return f"Order(quantity={self.quantity})"
    def __str__(self):
        return f"Quantity: {self.quantity}"

order = Order(3)
print(repr(order))
print(order)
```
These display Order(quantity=3) and Quantity: 3. Repr uses the information-rich representation; print uses the convenient string representation. If __str__ is absent, the default representation uses __repr__. Both methods return str values.''',
    "__repr__ and __str__ should return strings, not print their own messages in place of a returned representation.", 'f1 f2 f3', 'f1 f2',level='MEDIUM')
add(80,"A saved label containing non-ASCII text must be decoded under the intended encoding. Make the text encoding explicit at the file boundary.",
'''For a disposable illustrative text file:
```python
with open("label.txt", "w", encoding="utf-8") as destination:
    destination.write("café")
with open("label.txt", "r", encoding="utf-8") as source:
    print(source.read())
```
The output is café. The write encodes text as UTF-8, and the read decodes the file's bytes using UTF-8. Choosing the encoding is not a cosmetic display preference; it identifies how the bytes are interpreted. If a file contains bytes invalid under the selected encoding, reading can raise UnicodeDecodeError.''',
    "A file's name does not establish its encoding. The selected decoding must match the bytes for correct text, and an invalid selected decoding can fail.", 'f1 f2 f3', 'f2 f3')
add(81,"An order import can fail because the file is absent, its bytes cannot be decoded, or the CSV parser detects a problem. Rows also need explicit field validation.",
'''At the import boundary, use specific handlers for FileNotFoundError, UnicodeDecodeError and csv.Error, reporting missing source, decoding failure and parser failure separately. For an illustrative header label,quantity, a row containing only notebook yields a missing quantity filled with None by default. A row containing notebook,3,extra puts the excess field under the default None key. DictReader's restval and restkey rules mean these row lengths do not automatically become csv.Error. Check the required row fields as well as handling parser-reported failures.''',
    "Handling csv.Error is not a complete row-shape check. Missing and excess fields can be represented in the resulting dictionary, so validate required fields explicitly.", 'f1 f2 f3 f4 f5', 'f4',reason='A file-import demonstration can contrast missing files, decoding failures, parser errors and row dictionaries requiring validation.')
add(82,"An opened file needs a defined exit boundary even when its body raises. Managed resource use separates entering the resource from leaving it.",
'''Use with around the file operation:
```python
with open("label.txt", "r", encoding="utf-8") as source:
    text = source.read()
print(text)
```
After entry succeeds, the body reads the text and leaving it closes this file. If the body instead raises an exception, leaving the body still closes the file. For a general context manager, its exit method runs on normal or exceptional completion after successful entry, and it may suppress an exception. Keep that general possibility distinct from the specific file-closing behavior demonstrated here.''',
    "Do not promise that every context manager necessarily propagates every body exception unchanged. A context manager may suppress an exception; with an opened file, the key taught behavior is closure on exit.", 'f1 f2 f3', 'f2 f3')
add(83,"A binary payload should be copied without text decoding. Read and write bytes using binary modes, with a deliberate destination choice.",
'''For a supplied source and a disposable destination:
```python
with open("source.bin", "rb") as source:
    with open("copy.bin", "wb") as destination:
        payload = source.read()
        destination.write(payload)
```
The read returns bytes, and the write accepts that bytes value. No text decoding or encoding is inserted into this copy. Both files use managed opening and close after their respective bodies. The wb destination is created or truncated, so use this example only with a destination whose replacement is intended.''',
    "wb is not a non-destructive append or exclusive-create mode. It can truncate an existing destination, and binary writing expects bytes rather than str.", 'f1 f2 f3 f4', 'f1 f2')
add(84,"A report needs the signed number of days between two calendar dates. Parse the supplied text with an explicit format before subtracting the date values.",
'''Separate parsing from date arithmetic:
```python
from datetime import datetime
first = datetime.strptime("2025-03-01", "%Y-%m-%d").date()
second = datetime.strptime("2025-03-04", "%Y-%m-%d").date()
print((second - first).days)
print((first - second).days)
```
The outputs are 3 and -3. Strptime uses the year-month-day format, and date() obtains the calendar date. Subtraction returns a timedelta, whose days gives this signed calendar-date difference. Check which date is later and which subtraction the requirement asks for before interpreting the sign.''',
    "The difference is signed, not always an absolute distance. Reversing the order of subtraction reverses the sign in this calendar-date example.", 'f1 f2 f3 f4', 'f3 f4')
add(85,"Two scripts need the same order-cost helper. Move its definition into a sibling module so each script can import the shared implementation.",
'''For example, helpers.py contains def cost(quantity, price): with an indented return quantity * price. In a sibling report.py, write import helpers and call helpers.cost(3, 4), or use from helpers import cost and call cost(3, 4). The module filename without .py supplies the import name helpers. In ordinary script invocation, the script directory is included in the module search path, which permits this sibling-module arrangement. Follow the import binding before reading the later helper call.''',
    "The ordinary sibling import uses the module name, not helpers.py as a dotted filename in the import statement. Keep the file suffix and the import name distinct.", 'f1 f2 f3', 'f1',reason='A multi-file editor and execution demonstration can connect the helper file, importing script and shared call result.')
add(86,"As helpers grow, the program groups them in a regular package directory. The package structure and the import path need to agree.",
'''An illustrative layout is an orders directory containing an empty __init__.py and a costs.py module with the cost helper. From a context where that package is importable, import orders.costs and call orders.costs.cost(3, 4). Alternatively, from orders.costs import cost binds the helper directly for cost(3, 4). The regular package's __init__.py may be empty; it still belongs in this regular-package layout. Trace directory, module and helper as separate parts of the dotted access.''',
    "The package and its module are not the same name. Use package.module.helper after the module-import form, or import the member explicitly.", 'f1 f2', 'f1 f2',reason='A directory-tree and multi-file execution demonstration makes the package/module/helper relationships concrete.')
add(87,"A command program needs progress messages and diagnostics with different importance. Logging names the source and assigns a level to each event.",
'''Configure an application and emit events:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.debug("Detailed quantity calculation")
logger.info("Report complete")
```
INFO and higher events are included under this configuration, while DEBUG is below the threshold. Without that changed root threshold, the default is WARNING. Use WARNING for an unexpected condition while continuing, ERROR for inability to perform a function and CRITICAL for serious failure. Normally configure a handler at one suitable ancestor rather than both a logger and its ancestors, because propagation can otherwise duplicate output.''',
    "A missing DEBUG message need not mean its line was never reached. The configured level controls inclusion. Duplicated output can also result from handlers at multiple levels of a propagating logger hierarchy.", 'f1 f2 f3 f4 f5', 'f4 f5')
add(88,"A module should offer a reusable helper without running its command report whenever another module imports it. Guard the command-interface actions.",
'''Keep definitions outside the guarded body:
```python
def cost(quantity, price):
    return quantity * price

if __name__ == "__main__":
    print(cost(3, 4))
```
Executing this file as the main script displays 12. Importing it under its module name makes cost available without executing that guarded print. Main-script execution gives __name__ the value "__main__"; an imported module has its module name. The guard applies only to the actions placed inside it, so identify those boundaries when separating reusable code from the command interface.''',
    "Putting reusable helper definitions inside the guard would not preserve the intended unguarded import interface. Keep them outside and guard the command actions.", 'f1 f2 f3', 'f2 f3')
add(89,"An order-report script takes an input path and an optional verbosity switch. Define the command interface rather than guessing how supplied words should bind.",
'''Declare the arguments and inspect the parsed attributes:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_path")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
print(args.input_path, args.verbose)
```
With orders.csv --verbose as the supplied arguments, the values are orders.csv and True. Without --verbose, the flag is False. Input_path is required because it is declared as a positional argument. Missing required or otherwise invalid arguments produce an error message and exit status 2 by default.''',
    "A store_true flag is selected by its presence. It is not a request to supply the following word as a text value for verbose.", 'f1 f2 f3 f4 f5', 'f3')
add(90,"An import appears to load an unexpected implementation. Inspect the search locations and the file actually imported before assuming the module name proves its source.",
'''For a diagnostic run:
```python
import sys
import json
print(sys.path)
print(json.__file__)
```
The exact paths depend on the executing environment. Ordinary imports check built-in modules and then search sys.path; the script directory normally precedes standard-library directories. A conflicting local file can consequently shadow a standard-library module. Inspect a file-backed module's __file__ to locate the imported file, and rename a conflicting local file to remove the ambiguity.''',
    "A familiar import name is not sufficient evidence that the expected standard-library file was loaded. Local shadowing is possible; check actual search paths and the imported location.", 'f1 f2 f3 f4', 'f1 f2 f4')
add(91,"An order program receives configuration through process environment settings. The setting arrives as text, and absence needs an explicit policy.",
'''Choose a fallback only for an optional setting:
```python
import os
label = os.environ.get("ORDER_LABEL", "notebook")
required = os.environ.get("ORDER_SOURCE")
print(label)
if required is None:
    print("Missing ORDER_SOURCE configuration")
```
The mapping stores string values. With no ORDER_LABEL, the example uses notebook; with no ORDER_SOURCE, the absence test reports missing configuration. Bracket lookup for a required missing key would raise KeyError. Do not silently proceed with an unintended value when the requirement says the setting must be present.''',
    "An absent setting and a configured empty string are not identical. Check absence explicitly when enforcing required configuration, rather than relying on a broad truth test.", 'f1 f2 f3', 'f2 f3')
add(92,"A simulation and a security-sensitive token have different randomness requirements. Choose the module from the use case, not from the convenience of a familiar function.",
'''For a simulation, import random, call random.seed(7), then obtain values with random.random(). Each such value is in the interval starting at 0.0 and excluding 1.0. Reusing a seed reproduces a sequence under the documented reproducibility conditions. For a security-sensitive token, import secrets and use secrets.token_hex(16) to request a random hexadecimal token from 16 bytes. The illustrative seed is not a recipe for security. Keep reproducible modelling behavior separate from the cryptographically strong randomness supplied by secrets.''',
    "Do not substitute seeded random output for security-sensitive randomness. Also, do not upgrade conditional documented reproducibility into a promise that every sequence is identical across every environment.", 'f1 f2 f3 f4', 'f1 f2',level='MEDIUM')
add(93,"A program accepts labels consisting of uppercase letters. The pattern describes the allowed text, and fullmatch expresses a whole-text check.",
'''Check complete labels:
```python
import re
pattern = r"[A-Z][A-Z]*"
for label in ["BLUE", "Blue", "BLUE!"]:
    accepted = re.fullmatch(pattern, label) is not None
    print(label, accepted)
```
The results are True, False and False. The first element requires an uppercase letter, and the following [A-Z]* permits zero or more additional uppercase letters. Fullmatch checks the entire text. Match checks at the beginning and search can find a match anywhere, so neither has the same whole-text requirement. Raw literals avoid Python string-escape processing of pattern backslashes.''',
    "Finding a matching prefix or substring does not establish whole-text validity. Use fullmatch and an explicit is not None success test for this validation requirement.", 'f1 f2 f3 f4', 'f3 f4')
add(94,"A run should identify which interpreter is actually executing the program. Print runtime information instead of relying only on a tool label.",
'''Inspect the selected process:
```python
import sys
print(sys.executable)
print(sys.version)
```
The first value gives the executable path when Python can retrieve it. The second includes interpreter version, build and compiler information. These are runtime observations, so compare them with the interpreter you intended to use. The executable field may be an empty string or None when Python cannot retrieve it; do not fabricate a path in that case.''',
    "Sys.executable is not guaranteed to supply a nonempty path in every circumstance. Preserve that availability limit when recording runtime identity.", 'f1 f2 f3', 'f1',level='LOW')
add(95,"A project needs an environment separate from the base interpreter's packages. Create it with the selected Python and verify the environment through its own executable.",
'''Run the chosen executable with -m venv .venv. The created interpreter is .venv/bin/python on POSIX or .venv/Scripts/python.exe on Windows. Invoke that executable with -m pip list to inspect the project's packages. Inside a run, compare sys.prefix and sys.base_prefix: inequality identifies a virtual environment. Activation changes command lookup, but a full-path invocation does not require activation. The environment is isolated from base-environment packages by default, so inspect it rather than assuming the base package list applies.''',
    "Activation is not a prerequisite for explicit environment-executable invocation. Nor does a virtual environment share all base-environment packages by default.", 'f1 f2 f3 f4 f5', 'f2 f5',reason='A terminal demonstration can show environment creation, explicit interpreter invocation and package-list inspection.')
add(96,"A tool says a project environment is selected, but the program may be running another interpreter. Verify the executed process, then configure an explicit executable if needed.",
'''In the executed program, inspect sys.executable and compare sys.prefix with sys.base_prefix after importing sys. If the path is not the intended venv interpreter, configure the execution tool to use its bin/python on POSIX or Scripts/python.exe on Windows. Run again and inspect both the executable path and the prefix comparison. An environment label is not the evidence used in this check; the actual process values are. Explicit executable invocation does not depend on activation.''',
    "Do not stop after changing a displayed environment label. Recheck the executable and prefix relationship in the program that actually runs.", 'f1 f2 f3 f4', 'f1 f4',reason='A tool configuration and rerun demonstration can contrast intended environment labels with the actual interpreter path.')
add(97,"A project needs a documented third-party distribution. Installation, inspection and import verification should all use the interpreter that will run the project.",
'''Using the intended environment executable, invoke -m pip install package_name, replacing package_name with the verified distribution name. Through that same executable, use -m pip show package_name or -m pip list to inspect installation. Then run an import of the project's documented import name under the same interpreter. Keep these as separate checks: the distribution installed by pip and the import package used by Python need not have identical names. Do not guess an import name solely from the installation spelling.''',
    "Installing with one interpreter does not verify usability in a different interpreter. Match the executable across install, inspection and the documented import check.", 'f1 f2 f3 f4', 'f1 f3 f4',reason='A terminal demonstration can show installation and verification through one explicitly selected environment interpreter.')
add(98,"A project environment should be recreated from recorded dependencies. A requirements file records package specifications, while the recreated runtime still needs verification.",
'''An illustrative requirement package_name==version represents a pinned distribution version; replace both placeholders with verified project information. In a fresh environment, invoke its Python with -m pip install -r requirements.txt. Use the same interpreter with -m pip list to inspect installed versions, then check the required documented imports there. The file records dependencies, but the installation report alone is not the final evidence that every required module is importable in the recreated runtime.''',
    "Do not invent dependency names or versions to fill a requirements file. Nor should a successful installation report replace import checks in the recreated interpreter.", 'f1 f2 f3 f4', 'f4',reason='A recreation demonstration can connect the requirements file, fresh environment installation and runtime import checks.')
add(99,"A debugging check is not a production input policy. Assert can check a condition during normal debugging execution, but optimization can remove it.",
'''For a supplied expected total, assert total == 10, "unexpected total" raises AssertionError when false in normal debugging execution. If nonnegative quantity is a required runtime contract, use an explicit if quantity < 0: branch followed by raise ValueError(...) instead.''',
    "With -O, assert statements can be omitted. Do not use a removable assertion as the required production input check.", 'f1 f2 f3', 'f2 f3',level='NONE')
add(100,"A list stores reusable items, while an iterator records progress through a traversal. Keeping those roles separate explains why a fresh iterator and the same iterator behave differently.",
'''Advance one traversal without changing another:
```python
values = [3, 2]
first = iter(values)
second = iter(values)
print(next(first))
print(next(first))
print(next(first, None))
print(next(second))
print(iter(first) is first)
```
The results are 3, 2, None, 3 and True. Separate list iterators have separate traversal state. First is exhausted after two items, so next with a default returns None. Without the default, exhaustion signals StopIteration. Calling iter(first) returns that same iterator rather than resetting its progress.''',
    "An iterable source and its iterator are not interchangeable traversal states. Calling iter on an iterator does not create an independent restarted pass.", 'f1 f2 f3 f4', 'f2 f3')
add(101,"A helper should supply accepted quantities one at a time. Yield gives a value and suspends the function rather than completing an ordinary return-style calculation.",
'''Advance a generator function:
```python
def positive_quantities(values):
    for value in values:
        if value > 0:
            yield value

quantities = positive_quantities([3, -1, 2])
print(next(quantities))
print(next(quantities))
```
The outputs are 3 and 2. Calling the function creates a generator iterator. Advancing it runs to the next accepted yield, suspends there and retains local state for the next advance. The rejected minus one contributes no item. A later advance reaches the function's end and terminates iteration.''',
    "Yield does not finish the whole generator the way an ordinary return expression ends a call. It supplies an item while retaining state for a later advance.", 'f1 f2 f3', 'f1 f2')
add(102,"A one-pass calculation needs transformed positive quantities but not an intermediate list. A generator expression describes the transformation to perform during consumption.",
'''Total the accepted transformations:
```python
values = [3, -1, 2]
total = sum(value * 2 for value in values if value > 0)
print(total)
```
The result is 10 from transformed values 6 and 4. As the consumer requests items, filtering and transformation occur. The leftmost iterable expression is evaluated immediately when the generator expression is created; the item processing is deferred to iteration. As a sole argument to sum, this expression totals values without constructing an intermediate transformed list.''',
    "Do not say every part of a generator expression is deferred. The leftmost iterable expression is evaluated immediately, while filtering and transformation happen during iteration.", 'f1 f2 f3', 'f2')
add(103,"A diagnostic has already consumed one item from a traversal. The following consumer sees only what remains, and iter on that iterator will not rewind it.",
'''Observe consumption and a fresh pass:
```python
values = [3, 2]
traversal = iter(values)
print(next(traversal))
print(list(traversal))
print(list(iter(traversal)))
print(list(iter(values)))
```
The outputs are 3, [2], [], and [3, 2]. The exhausted traversal stays exhausted. Iter(traversal) returns that same iterator, whereas iter(values) supplies a fresh traversal of the reusable list. For a second complete pass, obtain that fresh iterator rather than reusing the consumed one.''',
    "Inspecting an iterator with next changes what later consumers can see. Calling iter on it does not reset it after inspection or exhaustion.", 'f1 f2 f3 f4', 'f1 f3',level='MEDIUM')
add(104,"A report may need one total or several passes over transformed values. Choose between lazy consumption and materialization based on which reuse the example requires.",
'''Compare a consumed generator with a stored result:
```python
values = [3, 2]
lazy = (value * 2 for value in values)
print(sum(lazy))
print(list(lazy))
stored = list(value * 2 for value in values)
print(sum(stored))
print(sum(stored))
```
The outputs are 10, [], 10 and 10. List materializes remaining items into a reusable collection. Generator expressions compute as consumed and tend to use less memory than equivalent list comprehensions. For a single total, sum(value * 2 for value in values) avoids the intermediate list.''',
    "Lazy does not mean automatically reusable. An iterator remains exhausted after completion; repeated work may need a stored collection or a new source traversal.", 'f1 f2 f3 f4', 'f4')
add(105,"Two batches of quantities need one combined total. Chain traverses the first batch and then the second without first joining them into a list.",
'''Use the combined traversal directly:
```python
from itertools import chain
first = [3, 2]
second = [5, 4]
print(list(chain(first, second)))
print(sum(chain(first, second)))
```
The displayed sequence is [3, 2, 5, 4], and the total is 14. Each call here creates a combined traversal for its consumer. Chain exhausts the first input before moving to the second; it does not alternate items from the two batches. The total does not require constructing that displayed list first.''',
    "Chain is sequential concatenation of traversal, not pairwise zip. Interpret the inputs in order: first is exhausted before second is visited.", 'f1 f2', 'f1')
add(106,"A transformation pipeline should select positive quantities and double them. Map, filter and comprehension forms can express this work with different materialization choices.",
'''Name the callable and predicate:
```python
def positive(value):
    return value > 0

def double(value):
    return value * 2

values = [3, -1, 2]
lazy = map(double, filter(positive, values))
print(list(lazy))
print([double(value) for value in values if positive(value)])
```
Both displayed lists are [6, 4]. Map and filter are lazy; the list call consumes the pipeline. The comprehension directly materializes its transform-and-filter result. Filter(positive, values) corresponds to (value for value in values if positive(value)); filter(None, values) instead selects truthy items.''',
    "Replacing a lazy pipeline with a list comprehension changes materialization. Use a parenthesized generator expression instead when preserving lazy traversal is required.", 'f1 f2 f3 f4 f5', 'f4 f5')
add(107,"Supplied checks describe how an order helper should behave. Express those checks in unittest methods so equality, truth and expected exceptions have explicit assertions.",
'''Wrap the supplied behaviors in a TestCase:
```python
import unittest

def cost(quantity):
    if quantity < 0:
        raise ValueError("negative quantity")
    return quantity * 4

class CostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(cost(3), 12)
        self.assertTrue(cost(3) > 0)
    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            cost(-1)
```
The test_* methods express individual checks. Equality compares actual and expected values, assertTrue checks a required truth condition, and assertRaises surrounds the operation expected to fail. These methods implement supplied checks rather than inventing a general testing foundation.''',
    "An expected exception check needs the failing operation inside the assertRaises body. Merely naming an exception type does not execute or check the operation.", 'f1 f2 f3', 'f3')
add(108,"A test runner report is evidence only for the tests it actually executed. Read the count and distinguish unsuccessful assertions from unexpected exceptions.",
'''For an illustrative test_cost.py module, python -m unittest test_cost runs the named module. Python -m unittest discover uses discovery, with the current directory and test*.py names as defaults. The -s option selects another starting directory and -p selects a filename pattern. In the report, a failure identifies an unsuccessful assertion and its traceback; an error identifies an unexpected exception during a test. A reported count of zero means no helper checks ran, even if you intended to discover several.''',
    "A zero test count is not evidence of correct helper behavior. Also, failures and errors are different report categories, not two interchangeable descriptions of a failed assertion.", 'f1 f2 f3 f4 f5', 'f3 f4 f5',reason='A runner demonstration can show selected tests, discovery options and distinct failure/error/count reports.')
add(109,"Each test needs fresh mutable data, and a supplied resource needs cleanup even on setup failure. Arrange per-test state and registered release actions explicitly.",
'''For list state, define setUp(self) and assign self.quantities = [3, 2] there. Every test receives fresh per-test setup rather than mutating a shared class list. TearDown runs after a test whenever setUp succeeded, even if the test failed. For a supplied acquired resource, register its release callable with self.addCleanup(release) after acquisition. Registered cleanups run after tearDown, or after failed setUp, in reverse registration order. Trace acquisition and registration as separate steps when reasoning about a failing setup.''',
    "TearDown does not run when setUp fails. Registered cleanup covers that case; also, setUp failure prevents the test method from running.", 'f1 f2 f3 f4', 'f1 f2 f3',reason='An execution-order diagram can contrast successful setup, failing tests, failed setup and reverse-order registered cleanup.')
add(110,"A generated helper looks plausible, but its actual branches must meet the supplied requirement. Trace specific inputs rather than treating generated form as proof.",
'''Consider this deliberately incomplete helper:
```python
def cost(quantity):
    if quantity > 0:
        return quantity * 4

print(cost(3))
print(cost(0))
```
The results are 12 and None. For three, the condition selects the return. For zero, the branch is not selected and the function reaches its end without return. If the supplied requirement expects zero cost for zero quantity, that traced None is a mismatch. Track each assignment, condition and actual return for valid and invalid inputs before deciding how the code should be corrected.''',
    "Plausible generated code is not correctness evidence. A missing return path produces None, not the value suggested by a comment or the user's intended calculation.", 'f1 f2 f3', 'f1 f3')
add(111,"A generated report helper may overwrite or move a file somewhere unintended. Review the modes and resolved paths before allowing the operation to run.",
'''In a supplied helper, with open(output, "w") truncates an existing output. If that contradicts the requirement, do not execute it unchanged. A path.unlink() removes the file or symbolic link at that path; remove an unintended unlink call instead of trying it. For source.rename(target), inspect both source and destination, including the Unix possibility of replacing an existing file. Trace absolute child operands, which replace a preceding base, and relative rename targets, which resolve against the working directory. Write down the actual destination before execution.''',
    "A reassuring variable name such as safe_output does not establish a safe destination. Actual modes and path-resolution rules determine the operation being proposed.", 'f1 f2 f3 f4', 'f1 f4',reason='An annotated, non-executing review can diagram proposed source/destination paths and identify destructive operations before they run.')
add(112,"A generated parser must not execute untrusted text. Review execution mechanisms and choose a parser matching the data the requirement actually expects.",
'''If the quantity arrives as untrusted text, replace a proposed eval(text) calculation with int(text) or float(text) as appropriate, followed by explicit value validation and malformed-input handling. For expected JSON, json.loads is the matching parser, but impose input-size limits because malicious input can consume substantial CPU and memory. Reject exec on untrusted instructions. Inspect shell=True and untrusted command construction for injection risk: a shell makes quoting and metacharacters a security responsibility. Review these calls as text; do not demonstrate them by running untrusted input.''',
    "Non-executing parsing does not imply unlimited resource safety. JSON needs input-size limits for untrusted input, and eval or exec must not be used to process untrusted text or instructions.", 'f1 f2 f3 f4 f5', 'f1 f2 f5',reason='Annotated code and data-flow diagrams can expose execution boundaries and unsafe input routes without executing hazardous examples.')
add(113,"A generated API call may sound authoritative while using nonexistent or mismatched arguments. Verify the actual interface in the selected runtime.",
'''For a proposed sorted(records, key=quantity_key, reverse=True), compare the official sorted entry with the claimed name, signature, keyword-only options and returned value. In the available runtime, help(sorted) displays documentation for the object and supports inspection of its interface. Check the executing interpreter's version before comparing version-specific documentation. Record what the documented interface supports rather than filling a gap with the assistant's confident wording.''',
    "A plausible assistant claim is not an API specification. Verify the actual object and version, including arguments and expected result, before accepting the generated call.", 'f1 f2 f3 f4', 'f2 f4',level='MEDIUM')
add(114,"A generated solution proposes a dependency install. Verify the named distribution and its source before allowing installation into the project.",
'''For a proposed package, browse the Python Package Index, which pip uses by default, and compare the actual distribution with the project's installation documentation. Confirm its documented import name separately because distribution and import packages need not share a name. Inspect --index-url in the command: it changes the package index used for installation. Before adding the dependency, check whether a documented standard-library module already meets the requirement. Withhold installation when the suggestion's identity and documented use cannot be verified.''',
    "Do not install first and investigate the name later. Assistant output can be mistaken, and both the distribution identity and the proposed installation source need verification.", 'f1 f2 f3 f4 f5', 'f3 f5',level='MEDIUM')
add(115,"A generated implementation needs an evidence-based decision: accept supported behavior, correct a mismatch or refuse unsafe execution. Keep the requirement, traces and supplied tests together.",
'''Suppose the supplied expectation is cost(0) == 0, but the traced helper reaches its end and returns None. That mismatch supports correction, not unchanged acceptance. A failed assertion or unexpected test exception likewise identifies behavior needing correction. Record acceptance only for behavior supported by traced returns and supplied expectations. If the proposal evaluates untrusted input or truncates a file contrary to requirements, reject its execution until those operations are removed or corrected. Testing is necessary because assistant-generated code can be wrong.''',
    "Generated origin is not acceptance evidence. Neither failed tests nor identified unsafe operations support accepting the implementation unchanged.", 'f1 f2 f3 f4', 'f1 f2 f4',level='MEDIUM')

# Self-review adjustments: factual introductions cite what they actually teach;
# visual preferences distinguish non-executing reviews from running demonstrations.
intro_facts = {
8:'f1 f2 f4', 9:'f1', 16:'f1 f2', 19:'f1 f2', 21:'f1 f2',
28:'f1', 40:'f1', 48:'f1 f2', 55:'f1 f2', 60:'f1', 62:'f1 f2',
68:'f1 f2', 69:'f1', 70:'f1 f2 f3', 71:'f1 f2', 72:'f1 f2 f3',
75:'f1 f2', 79:'f1 f2', 81:'f1 f2 f3 f4', 82:'f1 f2', 93:'f1 f3',
95:'f1 f5', 97:'f1 f2 f3', 98:'f1 f4', 99:'f2 f3', 100:'f1',
101:'f1 f2', 102:'f1 f3', 103:'f1 f3', 104:'f1 f2', 105:'f1',
107:'f1 f2 f3', 108:'f3 f4 f5', 110:'f1 f2 f3', 111:'f1 f3 f4',
112:'f1 f2 f4', 113:'f1 f4', 114:'f1 f3 f5', 115:'f1 f2 f3 f4'}
for i,ids in intro_facts.items(): entries[i]['teaching_blocks'][0]['fact_ids']=ids.split()
for i in [35,59,67,78,85,86,87,89,90,95,96,97,98,108]:
    entries[i]['video_need']['preferred_visual_modes']=['screen_demo','annotated_code']
for i in [51,56,109]:
    entries[i]['video_need']['preferred_visual_modes']=['diagram_animation','annotated_code']
for i in [111,112]:
    entries[i]['video_need']['preferred_visual_modes']=['annotated_code','diagram_animation']
# The path scope supplies staged prerequisites absent from the internal graph.
for i in [25,35,56,67,78,80,81,82,83,85,86,95,96,97,98,111]:
    entries[i]['teaching_notes'].append('Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.')
for i in [95,96,97,98]:
    entries[i]['teaching_notes'].append('Require linux.shell_pipes_and_redirection before shell-dependent environment work; commands here teach Python invocation, not shell fundamentals.')
entries[111]['teaching_notes'].append('Require linux.permissions_ownership_and_users and security.access_control_identities_and_permissions before reviewing generated file operations.')
entries[112]['teaching_notes'].append('Require security.access_control_identities_and_permissions before reviewing untrusted-input execution.')
for i in [87,91,92]:
    entries[i]['teaching_notes'].append('Require security.secrets_handling_basics before this consuming unit; do not introduce a general secrets-handling curriculum here.')
entries[76]['teaching_notes'].append('Require web.json_serialization_basics before this unit; teach the Python json API rather than the generic format foundation.')
for i in [107,108,109,115]:
    entries[i]['teaching_notes'].append('Require testing.write_unit_tests_with_assertions and testing.test_edge_cases_and_failures before applying the supplied checks. This unit does not supply the external testing foundations.')
entries[109]['teaching_notes'].append('Require testing.fixtures_and_test_data before fixture/isolation work.')

assert len(entries)==len(cs)==116
metadata=dict(briefs['metadata'])
metadata.update(artifact_type='glossary_pass_a',prompt_version='05_glossary_pass_a@v1',model='none',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), parent_artifact_hashes={name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in inputs})
artifact={'metadata':metadata,'batch_id':'glossary_batch_learn_python','entries':entries}
(B/'glossary_pass_a.part.all.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
(B/'pass_a_examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n')
# Free mechanical checklist: row identity, exact brief fact references, complete coverage,
# standalone prose, unique local block IDs, and visual-mode policy.
for e in entries:
    key=(e['concept_id'],e['path_id']); valid={f['id'] for f in bs[key]['evidence']['required_facts']}
    used={f for b in e['teaching_blocks'] for f in b['fact_ids']}
    assert used==valid,(key,used,valid)
    assert len({b['id'] for b in e['teaching_blocks']})==len(e['teaching_blocks'])
    assert not re.search(r'\b(video|clip|watch)\b', ' '.join(b['content'] for b in e['teaching_blocks']), re.I),key
    assert e['video_need']['level']!='NONE' or e['video_need']['preferred_visual_modes']==[]
assert {(e['concept_id'],e['path_id']) for e in entries}==set(bs)==set(ds)
assert len({(e['concept_id'],e['path_id']) for e in entries})==len(entries)
for i,code in examples: ast.parse(code)
print('Entries:',len(entries),'Teaching blocks:',sum(len(e['teaching_blocks']) for e in entries),'Python examples:',len(examples))
print('Tiers:', {t:sum(ds[(e['concept_id'],e['path_id'])]['depth_tier']==t for e in entries) for t in ['core','standard','reference']})
