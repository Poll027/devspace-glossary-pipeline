# Human Spot-Check List

**Batch:** glossary_batch_001_data_analyst_pilot  
**Path:** data_analyst  
**Generated:** Cross-artifact review stage

This file lists segments for manual review. Lowest-scoring segments appear first within each tier.

---

## Core Concepts (10 of 28 segments)

| Concept | Label | Time (review link) | Summary |
|---------|-------|-------------------|---------|
| python.lists | Index into a list with positive and negative positions, and see why a slice's end index is excluded | [0:00–2:57](https://www.youtube.com/watch?v=ajrtAuDg3yw&t=0s) (2:57) | Takes a list holding the numbers 0 to 9 and reads single items by position, from... |
| python.lists | Building a list with square brackets, indexing elements by position, and replacing an element in place | [0:19–3:28](https://www.youtube.com/watch?v=SfX8IIxoJwQ&t=19s) (3:09) | Introduces a list as a way to store several items under one name, using a food e... |
| python.dictionaries | Live demo: creating a dictionary, reading by key, KeyError, get() with a default, and adding or updating an entry | [0:00–5:00](https://www.youtube.com/watch?v=daefaLgNkw0&t=0s) (5:00) | Explains a dictionary as linked key and value pairs, where the key is a unique i... |
| python.for_loops | How Python for loops work: syntax, loop variable, and iteration over a list | [0:00–3:27](https://www.youtube.com/watch?v=zmIdC0_0BgY&t=0s) (3:27) | Opens with a flow diagram of a for loop over a list of five numbers: take the fi... |
| python.return_values | Getting a value back from a function to reuse, instead of just printing | [0:00–5:00](https://www.youtube.com/watch?v=AetGXMcNU3M&t=0s) (5:00) | Starts with an area function that prints length times width, so the result appea... |
| python.return_values | Return sends a value back to the caller; a function without return gives None | [0:00–6:37](https://www.youtube.com/watch?v=DZ2yBGzvlXk&t=0s) (6:37) | Contrasts printing with returning: programs need a function to hand a value back... |
| stats.measures_of_spread | Variance and standard deviation worked from squared deviations, for a whole population and then for a sample | [3:56–10:12](https://www.youtube.com/watch?v=SzZ6GpcfoQY&t=236s) (6:16) | Works through variance and standard deviation on a small set of measurements. Fo... |
| pandas.dataframe_series_model | A Series built from a Python list: one labelled column of any data type | [0:00–2:41](https://www.youtube.com/watch?v=W6WFX_H-AA4&t=0s) (2:41) | Introduces a Series as a one-dimensional labelled array, like a single column in... |
| pandas.dataframe_series_model | From a dict of lists to a DataFrame: rows, columns, and a simple index | [3:09–11:08](https://www.youtube.com/watch?v=zmdjNSmRXF4&t=189s) (7:59) | Builds the DataFrame idea in plain Python first: a dict whose keys play the role... |
| pandas.reading_data | Reading a CSV into a DataFrame with pd.read_csv | [0:58–2:52](https://www.youtube.com/watch?v=dUpyC40cF6Q&t=58s) (1:54) | Calls pd.read_csv on a countries CSV: the file's path is copied, pasted as the a... |

---

## Standard Concepts (10 of 69 segments)

| Concept | Label | Time (review link) | Summary |
|---------|-------|-------------------|---------|
| data.data_quality_basics | Data-quality dimensions explained one at a time: accuracy, completeness, consistency, validity, uniqueness | [1:51–5:26](https://www.youtube.com/watch?v=f7bAohSl_fo&t=111s) (3:35) | Presents data quality dimensions as separate factors, each measuring one aspect ... |
| data.data_quality_basics | Data quality as fitness for purpose, shown on one phone-and-email marketing list | [0:00–2:24](https://www.youtube.com/watch?v=pncfeOvxamg&t=0s) (2:24) | Describes data quality as keeping data useful for its intended business purpose,... |
| data.analysis_workflow | One analysis walked through in order: ask, prepare, clean, analyze, share | [0:04–4:36](https://www.youtube.com/watch?v=Jye81eSts2c&t=4s) (4:32) | Follows one real analysis, an employee engagement survey, through its stages. Fi... |
| python.sets | What a set is, two ways to create one, and how duplicates are dropped | [0:26–2:38](https://www.youtube.com/watch?v=r3R3h5ly_8g&t=26s) (2:12) | Describes a set as like a list that removes duplicate values; intersection and d... |
| python.sets | Sets in Python: unordered unique collections, set() constructor, membership testing, and union/intersection operations | [0:02–4:03](https://www.youtube.com/watch?v=t9j8lCUGZXo&t=2s) (4:01) | Starts from a list of numbers with duplicates and converts it with set() so only... |
| python.while_loops | Visually explained: building a while-loop counter, including the infinite-loop trap and the fix | [2:58–7:01](https://www.youtube.com/watch?v=gD8ePxAhjUM&t=178s) (4:03) | Builds a counter with a while loop: write while, a condition such as i smaller t... |
| python.variable_scope | The LEGB resolution order, then live demos of a local variable shadowing a global | [0:34–6:15](https://www.youtube.com/watch?v=QVdf0LgmICw&t=34s) (5:41) | Starts with the lookup order Python uses: local names first, then names from an ... |
| python.file_io | open()'s r/w/a/r+ modes and its default-to-read behavior, matched to file-handle methods | [0:18–6:26](https://www.youtube.com/watch?v=Uh2ebFW8OYM&t=18s) (6:08) | Opens a text file with open(), explaining that the second argument picks the mod... |
| python.file_io | Opening a file with open()+mode, reading it with a context manager, and writing with w mode | [0:38–9:06](https://www.youtube.com/watch?v=Jsnw6HLASZA&t=38s) (8:28) | Reads a text file by calling open() in r mode, read() to get the whole contents ... |
| stats.distribution_shape | Symmetric, left-skewed and right-skewed distributions told apart by where the tail stretches | [0:00–2:29](https://www.youtube.com/watch?v=Y53_8WRrPzg&t=0s) (2:29) | Shows three of six example charts and names each shape. Housefly lengths form a ... |

---

## Reference Concepts (10 of 18 segments)

| Concept | Label | Time (review link) | Summary |
|---------|-------|-------------------|---------|
| python.function_default_keyword_args | Live demo: adding default values to function parameters with = in the def line | [0:00–3:15](https://www.youtube.com/watch?v=m2uURZxex3c&t=0s) (3:15) | Explains a default argument as a value a parameter uses when that argument is le... |
| python.function_default_keyword_args | Calling a function with named arguments instead of position | [0:00–3:21](https://www.youtube.com/watch?v=7QCHpAtlSMo&t=0s) (3:21) | Explains a keyword argument as an argument written with its parameter's name and... |
| pandas.concat_stacking | pd.concat to stack monthly tables, then axis=1 to place tables side by side | [0:06–3:14](https://www.youtube.com/watch?v=bIiXKpZaJ3U&t=6s) (3:08) | Combines three monthly sales DataFrames into a quarter table by passing them as ... |
| pandas.melt_reshaping | pd.melt with id_vars, then renaming the new columns with var_name and value_name | [0:00–3:22](https://www.youtube.com/watch?v=ldpDNtPC_mU&t=0s) (3:22) | Starts with wide sales data, one row per store with a separate column for each m... |
| datamodel.er_diagram_reading | Entity type, instance and set, and the rectangle used to draw an entity | [70:52–72:48](https://www.youtube.com/watch?v=NdeeSEknp58&t=4252s) (1:56) | Names the building blocks of an ER model as entities, attributes and relationshi... |
| spreadsheet.sorting | Single-column sort and multi-level Sort dialog walkthrough | [0:45–5:52](https://www.youtube.com/watch?v=Aw4ZHT3SYzc&t=45s) (5:07) | The presenter sorts a dataset's revenue column largest to smallest and its divis... |
| spreadsheet.filtering | Applying AutoFilter: turning filters on, filtering by value, and clearing filters | [1:17–4:47](https://www.youtube.com/watch?v=cB5koQvGwsA&t=77s) (3:30) | The presenter starts with a data range that already has filter drop-down arrows ... |
| spreadsheet.conditional_formatting | Navigating to Highlight Cells Rules and applying a rule to a date column | [7:47–8:40](https://www.youtube.com/watch?v=_eZRkmRfVTM&t=467s) (0:53) | The presenter selects a date column, opens Conditional Formatting > Highlight Ce... |
| spreadsheet.data_validation | Input messages, error alerts, and numeric/date/text-length validation rules | [8:14–14:09](https://www.youtube.com/watch?v=FRiFfKb_B_A&t=494s) (5:55) | The instructor selects a cell that already has a dropdown rule and opens Data Va... |
| spreadsheet.remove_duplicates_cleaning | Copy data first, then remove duplicates by all columns or a subset | [0:34–3:09](https://www.youtube.com/watch?v=ADArCWLz55Y&t=34s) (2:35) | The presenter works with a sales table (Sales Agent, Region, Sales Value) and ex... |

---

## Segments with mean_score < 3.5

None found. All segments either have no score or score ≥ 3.5.
