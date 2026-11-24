import json
from pathlib import Path
p=Path('batches/glossary_batch_flutter_mobile_developer/glossary_pass_a.part.all.json')
d=json.loads(p.read_text()); before=json.loads(p.read_text()); rows={e['concept_id']:e for e in d['entries']}
def text(cid,bid,content):
    b=next(b for b in rows[cid]['teaching_blocks'] if b['id']==bid)
    b['content']=content
text('dart.expressions','tb4', 'Take an illustrative eligibility rule: the amount is at least 20 and delivery is enabled. With `amount = 24` and `deliveryEnabled = true`, `amount >= 20 && deliveryEnabled` gives true; with amount 18 it gives false. For arithmetic, trace the same inputs through three different operations: `5 / 2 = 2.5` is division, retaining the fractional part; `5 ~/ 2 = 2` is integer division, giving the whole-number quotient; `5 % 2 = 1` is remainder, because two groups of 2 use 4 of the 5, leaving 1. The remainder is not the quotient or its fractional part. These are separate illustrative expressions. When an eligibility rule combines alternatives and requirements, parentheses record the intended grouping.')
text('dart.classes','tb4', '''Here is a small model with typed final fields and initializing formal parameters:
```dart
class Order {
  final int id;
  final String label;
  Order(this.id, this.label);
}
final order = Order(7, 'Ready');
```
`this.id` and `this.label` in the parameter list are initializing formals: the supplied arguments initialize the corresponding instance fields. Here id receives 7 and label receives 'Ready'. The fields are initialized before the constructor body runs, not by later assignments in that body. `order.label` reads 'Ready', and the final field cannot subsequently be reassigned.

An alternative definition of the same class uses ordinary parameters and an initializer list:
```dart
class Order {
  final int id;
  final String label;
  Order(int idValue, String labelValue)
      : id = idValue, label = labelValue {}
}
```
The list after `:` initializes id from idValue and label from labelValue before the empty `{}` body runs. This is an alternative to the first class definition, not code to paste beside it. The named initializing-formal alternative `Order({required this.id, required this.label});` makes the inputs explicit by name. Final fields may also be initialized at declaration; each route establishes their value once.''')
text('flutter.bundled_assets','tb2', '''Declare bundled asset paths in pubspec.yaml under the `flutter` section's `assets` list. For an illustrative resource at `assets/order.png` relative to pubspec.yaml, use:
```yaml
flutter:
  assets:
    - assets/order.png
```
`assets:` is indented two spaces beneath `flutter:`, and the asset entry is indented beneath `assets:`. The relative path supplies the logical asset-bundle key. Load the matching resource with `Image.asset('assets/order.png')`; the key must match the declaration.''')
text('flutter.bundled_assets','tb3', "Use the indented declaration above for the illustrative `assets/order.png` resource. The path relative to pubspec.yaml is its logical bundle key, so `Image.asset('assets/order.png')` refers to that same key. Compare the strings directly when the image is not the expected one. This example concerns a bundled resource, not a network image source.")
text('dart.variable_declarations','tb4', "For a changing count, `var orderCount = 2;` infers a type from the integer initializer. At this point orderCount is 2. After `orderCount = 3;`, it is 3: the reassignment stays within its inferred type. `int orderCount = 2;` is the explicit-type alternative, not a second declaration to place beside the first. Contrast `final deliveryLabel = 'Ready';`: this example assigns the label once and does not reassign it; a later replacement is not permitted. A compile-time value can instead be declared with `const`. Choose the modifier according to whether this variable will receive another assignment.")
text('dart.functions','tb4', '''For an order amount and a required named delivery amount, write:
```dart
int orderTotal(int amount, {required int delivery}) {
  return amount + delivery;
}
```
`orderTotal(20, delivery: 4)` binds 20 to amount and 4 to delivery, returning 24. The amount is required positional; the delivery argument is required by name and cannot be omitted.

Use a separate function to illustrate optional positional parameters:
```dart
int totalWithDefault(int amount, [int delivery = 4]) {
  return amount + delivery;
}
```
`totalWithDefault(20)` omits the optional argument, so delivery uses its constant default 4 and the result is 24. `totalWithDefault(20, 2)` supplies delivery positionally and returns 22. The first argument binds to amount and the second to delivery. These separate declarations show different parameter forms rather than mixing them in one parameter list.''')
text('dart.conditionals','tb4', '''Trace this short chain for an order action:
```dart
var action = 'Wait';
if (eligible) {
  action = 'Proceed';
} else if (canRetry) {
  action = 'Retry';
} else {
  action = 'Wait';
}
```
The inputs eligible and canRetry must be bool values. With eligible true, action becomes 'Proceed'; the later branches are not taken. With eligible false and canRetry true, the first test fails, the second succeeds, and action becomes 'Retry'. With both false, the else branch selects 'Wait'. The else-if test belongs to the same chain: it is reached only when the preceding condition was false, not as an independent action after an earlier match.''')
text('dart.iteration','tb4', '''For quantities 2, 3, and 1, a total declared as 0 before a for-in loop becomes 2, then 5, then 6 as each quantity is added. Resetting it in the body would discard earlier accumulation. To trace a bounded conventional loop and a skipped iteration, use:
```dart
var total = 0;
for (var i = 0; i < 3; i = i + 1) {
  if (i == 1) {
    continue;
  }
  total = total + i;
}
```
Initialization sets i to 0 once. The condition `0 < 3` is true, so the body adds 0 and total remains 0; the update makes i equal 1. The condition `1 < 3` is true, but continue skips the addition for this iteration. The update makes i equal 2. The condition is again true, the body adds 2, and total becomes 2. The update makes i equal 3; `3 < 3` is false, so repetition ends. Continue skips the rest of one body; break would stop the loop altogether.''')
text('dart.callbacks','tb4', '''Compare passing `onPressed: handler` with evaluating `handler()`. The first supplies the function value as the callback: its body runs when the receiving control invokes it. The second calls handler immediately where the expression is evaluated; it does not pass handler itself for later invocation. In the supplied order-label example, an anonymous callback can use the label from its surrounding lexical scope:
```dart
final orderLabel = 'Ready';
final handler = () {
  suppliedAction(orderLabel);
};
```
Here suppliedAction is the supplied action accepting the label. Creating handler defines the closure; passing handler hands over that function; invoking it executes the body with access to orderLabel. Adding call parentheses changes passing into immediate invocation. An arrow callback is an alternative to the block form, not a different promise about timing or copied values.''')
text('flutter.change_notifier_updates','tb4', '''In a supplied model extending ChangeNotifier, this mutation method makes the update-before-notification order visible:
```dart
int orderCount = 2;

void setOrderCount(int value) {
  orderCount = value;
  notifyListeners();
}
```
These are members inside that model. Calling `setOrderCount(3)` first changes the exposed orderCount field from 2 to 3, then notifies listeners. A notified consumer reading that field therefore sees 3, not the old 2. Reading the field alone is not this mutation and does not by itself call for notification. Notify when a model change might affect its consumers' UI, not merely because a value was read.''')
text('flutter.widget_find_assert','tb4', '''After creating the supplied widget tree, assert the illustrative Saved label with:
```dart
expect(find.text('Saved'), findsOneWidget);
```
`find.text('Saved')` targets Text widgets displaying Saved; findsOneWidget requires exactly one match. The assertion passes with one matching widget and fails with zero or more than one. To assert absence instead, use findsNothing. If the requirement identifies a keyed control, use find.byKey(key); if it identifies a widget type, use find.byType(Type). Choose the finder and expected count from the acceptance target, not whichever query happens to return something.''')
# Terminology repair only: use the source guide's existing layer names.
for b in rows['flutter.app_responsibility_boundaries']['teaching_blocks']:
    b['content']=b['content'].replace('application layer', 'UI layer')
# Concretize the existing schema example consistently; no change to schema rules.
for b in rows['flutter.local_database_schema']['teaching_blocks']:
    b['content']=b['content'].replace('tableName', 'orders').replace('fieldName', 'label')
text('flutter.local_database_schema','tb3', "A schema-to-model comparison has names, types, and identity. In the orders table above, id is the integer row identity with INTEGER PRIMARY KEY and label is the TEXT column matching the model's label field. The model's values must use storage representations sqflite supports; encode a boolean as 0/1 rather than treating a Dart bool as directly supported. The creation callback creates the initial tables at the supplied database path. Keep these concrete names aligned with the model rather than copying names from a different schema.")
text('flutter.local_database_schema','tb4', "Use the initialization pattern above with the supplied database path and initial version. In the illustrative orders table, id uses INTEGER PRIMARY KEY and label uses TEXT. Map the model's id and label fields to those matching column names. For a different supplied schema, substitute its prescribed table and column names consistently. If the model includes a boolean, encode it as 0 or 1 for sqflite rather than storing a Dart bool directly.")
# Check that only named rows and their teaching content changed.
allowed=set('dart.expressions dart.classes flutter.bundled_assets dart.variable_declarations dart.functions dart.conditionals dart.iteration dart.callbacks flutter.change_notifier_updates flutter.widget_find_assert flutter.app_responsibility_boundaries flutter.local_database_schema'.split())
for old,new in zip(before['entries'],d['entries']):
    if old!=new:
        assert old['concept_id'] in allowed
        for k in old:
            if k!='teaching_blocks': assert old[k]==new[k]
        for ob,nb in zip(old['teaching_blocks'],new['teaching_blocks']):
            assert {k:v for k,v in ob.items() if k!='content'}=={k:v for k,v in nb.items() if k!='content'}
assert before['metadata']==d['metadata']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Rows:',len(d['entries']),'Changed rows:',sum(a!=b for a,b in zip(before['entries'],d['entries'])), 'Blocks:',sum(len(e['teaching_blocks']) for e in d['entries']))
