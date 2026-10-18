#!/usr/bin/env python3
"""
Build clusters.json for stage 12_cluster_pass.
Groups adjacent concepts within tiles that are presentation-compatible.
"""
import json
import hashlib
import datetime
from collections import defaultdict

# Load input artifacts
with open("batches/glossary_batch_001_data_analyst_pilot/extracted_concepts.json") as f:
    extracted = json.load(f)

with open("batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.json") as f:
    bundles_data = json.load(f)

# Build concept lookup by concept_id
concepts_by_id = {c["concept_id"]: c for c in extracted["concepts"]}

# Build bundles lookup
bundles_by_id = {b["context"]["concept_id"]: b for b in bundles_data["bundles"]}

# Group concepts by tile, sorted by toc_sequence_position
tiles = defaultdict(list)
for c in sorted(extracted["concepts"], key=lambda x: x["toc_sequence_position"]):
    tile_id = c["toc_location"]["tile_id"]
    tiles[tile_id].append(c)

# Compute parent artifact hashes
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

extracted_hash = sha256_file("batches/glossary_batch_001_data_analyst_pilot/extracted_concepts.json")
bundles_hash = sha256_file("batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.json")

# -----------------------------------------------------------------------
# Cluster decision logic
# 
# Rules from GENERATOR.md + playbook §24:
# 1. Concepts must be adjacent in TOC order within a tile
# 2. Learner has all prerequisites at tile start (no concept in the cluster
#    requires another concept in the cluster as a prerequisite — they're
#    all available at the tile's entry point)
# 3. Showing them together doesn't hide an important boundary
# 4. They read as parts of one idea — steps of a workflow, variants of one operation
# 5. Never cross tiles
# 6. At least 2 concepts
#
# Key exclusion: concepts that learners must learn to tell apart (e.g., 
# join types) are better as separate steps.
# -----------------------------------------------------------------------

# Each entry: (tile_id, cluster_title, concept_ids, reasoning)
# We decide per tile whether to cluster, and which sub-groups if any.

cluster_decisions = []

# Helper: check if concepts within a group have cross-prerequisites
# (i.e., one concept in the group is a prerequisite of another in the group)
def has_internal_prereqs(concept_ids):
    """Returns True if any concept in the list is a prerequisite of another in the list."""
    id_set = set(concept_ids)
    for cid in concept_ids:
        c = concepts_by_id[cid]
        for prereq in c.get("direct_prerequisite_ids", []):
            if prereq in id_set:
                return True
    return False

# -----------------------------------------------------------------------
# TILE-BY-TILE DECISIONS
# -----------------------------------------------------------------------

# tile_data_shape_and_types: 2 concepts
# data.dataset_rows_columns, data.categorical_numeric_types
# These are two aspects of the same foundational idea: what data looks like.
# Rows/columns define structure; variable types describe what's in each column.
# They're taught together in every intro data course. No internal prereqs.
# CLUSTER: yes — parts of one idea (data shape and types)
cluster_decisions.append({
    "tile_id": "tile_data_shape_and_types",
    "title": "Datasets and Variable Types",
    "concept_ids": ["data.dataset_rows_columns", "data.categorical_numeric_types"],
    "reasoning": "Rows/columns and variable types are two facets of the same foundational idea — what a dataset looks like and what kind of values it holds. A learner encounters both simultaneously when first opening a dataset. Neither requires the other as a prerequisite; they read as complementary parts of one orientation."
})

# tile_data_quality_and_workflow: 3 concepts
# data.data_quality_basics, data.analysis_workflow, data.ethics_privacy_basics
# data_quality_basics and analysis_workflow are tightly linked — quality is a
# step in the workflow. ethics_privacy_basics is a separate concern (legal/ethical
# framing) that learners must distinguish from the technical workflow.
# CLUSTER: data_quality_basics + analysis_workflow only; ethics stands alone.
cluster_decisions.append({
    "tile_id": "tile_data_quality_and_workflow",
    "title": "Data Quality and the Analysis Workflow",
    "concept_ids": ["data.data_quality_basics", "data.analysis_workflow"],
    "reasoning": "Data quality is a prerequisite concern that feeds directly into the analysis workflow — understanding what makes data trustworthy is part of understanding the workflow itself. These two concepts read as steps of one process. Ethics/privacy is a distinct conceptual domain (legal and ethical obligations) that learners must learn to separate from the technical workflow, so it is not clustered here."
})

# tile_python_variables_types: 2 concepts
# python.variables_assignment, python.core_data_types
# Variables and types are inseparable in Python — you can't assign a variable
# without a type being inferred. They're always taught together.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_python_variables_types",
    "title": "Variables and Core Data Types",
    "concept_ids": ["python.variables_assignment", "python.core_data_types"],
    "reasoning": "Variable assignment and core data types are inseparable in Python: every assignment creates a typed value. Learners encounter both in the same first code cell. They read as two aspects of one idea — naming and typing values."
})

# tile_python_operators_conversion: 4 concepts
# python.arithmetic_operators, python.comparison_operators, 
# python.logical_operators, python.type_conversion
# Arithmetic, comparison, and logical operators are three distinct operator
# families that learners must learn to tell apart (they have different
# return types and precedence rules). type_conversion is a separate operation.
# However, comparison + logical operators are often used together in conditions.
# CLUSTER: arithmetic_operators alone; comparison + logical together; type_conversion alone.
# But the tile has 4 concepts — we can make two sub-clusters or one full cluster.
# The key question: do learners need to distinguish arithmetic from comparison?
# Yes — they have different return types (numbers vs booleans). 
# But comparison + logical are always used together in if/filter conditions.
# CLUSTER: comparison_operators + logical_operators (they compose naturally in conditions)
# arithmetic_operators and type_conversion are standalone.
cluster_decisions.append({
    "tile_id": "tile_python_operators_conversion",
    "title": "Comparison and Logical Operators",
    "concept_ids": ["python.comparison_operators", "python.logical_operators"],
    "reasoning": "Comparison and logical operators are always used together to build compound conditions (e.g., x > 0 and x < 10). They form one idea: constructing boolean tests. Arithmetic operators produce numbers rather than booleans and are a distinct concept; type_conversion is a separate operation. Clustering only comparison and logical keeps the important boundary between numeric and boolean operations visible."
})

# tile_python_lists_dicts_tuples: 3 concepts
# python.lists, python.dictionaries, python.tuples
# These are three distinct collection types that learners must learn to tell apart
# (different mutability, access patterns, use cases). Important boundary to preserve.
# However, lists and tuples are both ordered sequences — they share structure.
# Dicts are fundamentally different (key-value, unordered).
# CLUSTER: lists + tuples (ordered sequences, variants of one idea)
# dicts stand alone.
cluster_decisions.append({
    "tile_id": "tile_python_lists_dicts_tuples",
    "title": "Lists and Tuples",
    "concept_ids": ["python.lists", "python.tuples"],
    "reasoning": "Lists and tuples are both ordered sequences that support indexing and iteration; the key distinction is mutability. Showing them side by side makes that single difference immediately clear. Dictionaries are a fundamentally different structure (key-value mapping, unordered) that learners must learn to distinguish from sequences, so they are not clustered here."
})

# tile_python_sets_strings: 2 concepts
# python.sets, python.string_basics_formatting
# Sets and strings are quite different — sets are unordered collections for
# membership testing; strings are text sequences with formatting operations.
# These don't read as parts of one idea. No cluster.
# SKIP

# tile_python_conditionals_for_loops: 2 concepts
# python.conditional_statements, python.for_loops
# Conditionals and for loops are both control flow, but they're distinct
# structures that learners must learn to tell apart. However, they're often
# combined (for loop with if inside). They read as the two main control flow tools.
# CLUSTER: yes — both are control flow structures, often used together
cluster_decisions.append({
    "tile_id": "tile_python_conditionals_for_loops",
    "title": "Conditionals and For Loops",
    "concept_ids": ["python.conditional_statements", "python.for_loops"],
    "reasoning": "Conditionals and for loops are the two foundational control flow structures in Python, and they are routinely combined (a for loop containing an if statement). They read as complementary parts of one idea: directing program flow. Neither requires the other as a prerequisite at the tile's start."
})

# tile_python_while_loop_control: 2 concepts
# python.while_loops, python.loop_control
# While loops and loop control (break/continue) are tightly coupled —
# loop control statements are most meaningful in the context of a loop.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_python_while_loop_control",
    "title": "While Loops and Loop Control",
    "concept_ids": ["python.while_loops", "python.loop_control"],
    "reasoning": "Loop control statements (break, continue, pass) are only meaningful inside a loop. While loops and loop control read as one idea: how to run and exit a loop conditionally. They are always taught together."
})

# tile_python_comprehensions_iterating: 2 concepts
# python.comprehensions, python.iterating_collections
# Comprehensions are a compact form of iteration — they're closely related.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_python_comprehensions_iterating",
    "title": "Comprehensions and Iterating Collections",
    "concept_ids": ["python.comprehensions", "python.iterating_collections"],
    "reasoning": "List comprehensions are a compact syntax for iterating over a collection and transforming it — they are the same idea expressed differently. Showing them together lets learners see the equivalence between a for-loop iteration and a comprehension, which is the core insight of this tile."
})

# tile_python_functions_scope: 5 concepts
# python.defining_calling_functions, python.parameters_arguments,
# python.return_values, python.function_default_keyword_args, python.variable_scope
# These are all aspects of functions. However, there are important distinctions:
# - defining/calling is the basic concept
# - parameters/arguments is how you pass data in
# - return values is how you get data out
# - default/keyword args is a variant of parameters
# - variable scope is a separate concept about name resolution
# 
# Cluster 1: defining_calling + parameters_arguments + return_values
#   (the three parts of a function's interface — define, input, output)
# Cluster 2: function_default_keyword_args alone (variant of parameters)
# variable_scope stands alone (different concept: name resolution)
# 
# Actually, parameters_arguments and function_default_keyword_args are
# variants of the same idea (how to pass arguments). Cluster those.
# defining_calling + return_values are the basic function structure.
# 
# Best split: 
# - defining_calling_functions + parameters_arguments + return_values
#   (the complete basic function: define, input, output)
# - function_default_keyword_args stands alone (advanced parameter variant)
# - variable_scope stands alone (separate concept)
cluster_decisions.append({
    "tile_id": "tile_python_functions_scope",
    "title": "Defining Functions, Parameters, and Return Values",
    "concept_ids": ["python.defining_calling_functions", "python.parameters_arguments", "python.return_values"],
    "reasoning": "Defining a function, passing parameters, and returning values are the three inseparable parts of a function's basic interface. A learner cannot understand any one of them without the other two — they form a single mental model: 'a function takes inputs and produces an output.' Default/keyword arguments are a parameter variant that builds on this foundation and is better shown separately. Variable scope is a distinct concept about name resolution."
})

# tile_python_errors_imports: 2 concepts
# python.error_handling, python.import_statements
# Error handling and imports are both practical Python mechanics, but they're
# conceptually distinct — one is about catching exceptions, the other about
# loading modules. No strong "parts of one idea" relationship.
# SKIP

# tile_python_file_io: 1 concept — skip (need ≥2)
# tile_python_pep8_style: 1 concept — skip

# tile_stats_center_spread: 2 concepts
# stats.descriptive_measures_of_center, stats.measures_of_spread
# Mean/median/mode and variance/std dev are the two halves of descriptive stats.
# They're always taught as a pair: where is the center, how spread out is it?
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stats_center_spread",
    "title": "Measures of Center and Spread",
    "concept_ids": ["stats.descriptive_measures_of_center", "stats.measures_of_spread"],
    "reasoning": "Measures of center (mean, median, mode) and measures of spread (variance, standard deviation, IQR) are the two complementary halves of descriptive statistics — they answer 'where is the data?' and 'how spread out is it?' respectively. They are always interpreted together and form one idea: summarizing a distribution numerically."
})

# tile_stats_shape_outliers: 3 concepts
# stats.distribution_shape, stats.outlier_reasoning, stats.frequency_distribution_reading
# Distribution shape and outlier reasoning are tightly linked — skewness and
# outliers are related phenomena. Frequency distribution reading is how you
# see the shape. All three are about reading a distribution visually.
# CLUSTER: distribution_shape + outlier_reasoning (shape informs outlier detection)
# frequency_distribution_reading stands alone (it's the tool/skill, not the concept)
# Actually, frequency distribution reading is how you observe shape — they're
# parts of one workflow: read the distribution, identify shape, reason about outliers.
# CLUSTER: all three — they're steps of one analytical act
cluster_decisions.append({
    "tile_id": "tile_stats_shape_outliers",
    "title": "Distribution Shape, Outliers, and Frequency Distributions",
    "concept_ids": ["stats.distribution_shape", "stats.outlier_reasoning", "stats.frequency_distribution_reading"],
    "reasoning": "Reading a frequency distribution, identifying its shape (symmetric, skewed, bimodal), and reasoning about outliers are three steps of one analytical act: understanding how a variable is distributed. A learner cannot reason about outliers without first understanding shape, and shape is read from a frequency distribution. They form a single workflow and are always taught together."
})

# tile_stats_correlation: 3 concepts
# stats.correlation, stats.correlation_interpretation, stats.correlation_vs_causation_caveat
# These three are explicitly about the same topic: correlation.
# correlation = what it is; interpretation = how to read r; causation caveat = the limit.
# They're parts of one idea. However, the causation caveat is a critical boundary
# that learners must internalize separately — it's the most important thing to
# distinguish. But it's still part of the same concept cluster.
# CLUSTER: all three — they're the complete picture of correlation
cluster_decisions.append({
    "tile_id": "tile_stats_correlation",
    "title": "Correlation and Its Limits",
    "concept_ids": ["stats.correlation", "stats.correlation_interpretation", "stats.correlation_vs_causation_caveat"],
    "reasoning": "Correlation, how to interpret the correlation coefficient, and the correlation-vs-causation caveat are three aspects of one concept. A learner who knows what correlation is but not how to interpret r, or who doesn't know the causation caveat, has an incomplete and potentially dangerous understanding. Showing them together as a cluster makes the complete picture visible while keeping each sub-concept individually addressable."
})

# tile_pandas_dataframe_reading: 2 concepts
# pandas.dataframe_series_model, pandas.reading_data
# The DataFrame/Series model is the conceptual foundation; reading data is
# the first operation. They're tightly coupled — you need the model to
# understand what read_csv returns.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_pandas_dataframe_reading",
    "title": "DataFrames, Series, and Reading Data",
    "concept_ids": ["pandas.dataframe_series_model", "pandas.reading_data"],
    "reasoning": "The DataFrame/Series model is the conceptual foundation for all pandas work, and reading data (pd.read_csv) is the first operation that produces a DataFrame. A learner needs the model to understand what read_csv returns. These two concepts are the entry point to pandas and read as one idea: what a DataFrame is and how to get one."
})

# tile_pandas_creating_inspecting: 2 concepts
# pandas.creating_dataframes, pandas.inspecting_dataframes
# Creating and inspecting are two sides of the same coin — you create a
# DataFrame and immediately inspect it. They're workflow steps.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_pandas_creating_inspecting",
    "title": "Creating and Inspecting DataFrames",
    "concept_ids": ["pandas.creating_dataframes", "pandas.inspecting_dataframes"],
    "reasoning": "Creating a DataFrame and inspecting it (head, info, describe, shape) are the first two steps of every pandas workflow — you create or load data, then immediately examine it. They read as a single orientation step: 'make a DataFrame and look at it.'"
})

# tile_pandas_descriptive_stats: 1 concept — skip

# tile_pandas_selection_filtering: 2 concepts
# pandas.loc_iloc_selection, pandas.boolean_filtering
# loc/iloc and boolean filtering are two different selection mechanisms.
# Learners must learn to tell them apart (label-based vs condition-based).
# However, they're both about selecting subsets of data — variants of one operation.
# CLUSTER: yes — both are data selection tools, and they're often compared
cluster_decisions.append({
    "tile_id": "tile_pandas_selection_filtering",
    "title": "Selecting and Filtering Data",
    "concept_ids": ["pandas.loc_iloc_selection", "pandas.boolean_filtering"],
    "reasoning": "loc/iloc (label/position-based selection) and boolean filtering (condition-based selection) are the two primary ways to select subsets of a DataFrame. Showing them together makes the contrast clear: one selects by address, the other by condition. They are variants of one operation — subsetting data — and learners need both to work effectively."
})

# tile_pandas_sort_rename: 2 concepts
# pandas.sort_values, pandas.rename_columns_index
# Sorting and renaming are both basic DataFrame manipulation operations,
# but they're quite different in purpose. They don't read as parts of one idea.
# SKIP

# tile_pandas_dtype_datetime: 2 concepts
# pandas.dtype_conversion, pandas.datetime_handling
# Type conversion and datetime handling are related — datetime is a specific
# type conversion case. They're both about getting column types right.
# CLUSTER: yes — both are about column type management
cluster_decisions.append({
    "tile_id": "tile_pandas_dtype_datetime",
    "title": "Type Conversion and Datetime Handling",
    "concept_ids": ["pandas.dtype_conversion", "pandas.datetime_handling"],
    "reasoning": "dtype conversion (astype, pd.to_numeric) and datetime handling (pd.to_datetime, dt accessor) are both about correcting column types in a DataFrame. Datetime conversion is the most common and complex type conversion case. They read as two aspects of one task: making sure columns have the right type before analysis."
})

# tile_pandas_text_dupes_missing: 3 concepts
# pandas.str_accessor_cleaning, pandas.drop_duplicates, pandas.missing_data_handling
# These are three distinct data cleaning operations. They're all cleaning steps
# but address different problems (text format, duplicate rows, missing values).
# They're steps of one workflow: cleaning a DataFrame.
# CLUSTER: all three — they're the main cleaning operations
cluster_decisions.append({
    "tile_id": "tile_pandas_text_dupes_missing",
    "title": "Text Cleaning, Duplicates, and Missing Data",
    "concept_ids": ["pandas.str_accessor_cleaning", "pandas.drop_duplicates", "pandas.missing_data_handling"],
    "reasoning": "String cleaning, removing duplicates, and handling missing values are the three main data cleaning operations in pandas. They address different problems but are always applied in the same cleaning phase of an analysis workflow. Showing them as a cluster lets learners see the full cleaning toolkit at once, with each operation individually addressable."
})

# tile_pandas_map_apply: 2 concepts
# pandas.map_substitution, pandas.apply_transform
# map and apply are both element-wise transformation operations — variants
# of one idea (transforming values in a column/DataFrame).
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_pandas_map_apply",
    "title": "Mapping and Applying Transformations",
    "concept_ids": ["pandas.map_substitution", "pandas.apply_transform"],
    "reasoning": "map (for substituting values via a dictionary or function on a Series) and apply (for applying a function element-wise or row/column-wise) are two variants of the same idea: transforming values in a DataFrame. Showing them together makes the distinction clear — map is for simple substitution, apply is for custom logic."
})

# tile_pandas_concat_merge: 2 concepts
# pandas.concat_stacking, pandas.merge_join
# Concatenating (stacking) and merging (joining) are two ways to combine
# DataFrames. Learners must learn to tell them apart (stack vs join on key).
# But they're variants of one operation: combining DataFrames.
# CLUSTER: yes — both combine DataFrames, important to contrast
cluster_decisions.append({
    "tile_id": "tile_pandas_concat_merge",
    "title": "Concatenating and Merging DataFrames",
    "concept_ids": ["pandas.concat_stacking", "pandas.merge_join"],
    "reasoning": "concat (stacking DataFrames by rows or columns) and merge (joining DataFrames on a key) are the two ways to combine DataFrames in pandas. Showing them together makes the fundamental distinction clear: concat stacks, merge joins. They are variants of one operation — combining DataFrames — and learners need to choose between them in practice."
})

# tile_pandas_groupby_melt: 2 concepts
# pandas.groupby_aggregation, pandas.melt_reshaping
# groupby and melt are both reshaping operations but quite different:
# groupby aggregates (reduces rows), melt unpivots (increases rows).
# They don't read as parts of one idea — they're opposite operations.
# SKIP

# tile_pandas_pivot_export: 2 concepts
# pandas.pivot_table_reshaping, pandas.export_to_csv
# Pivot tables and exporting are both end-of-workflow operations but
# conceptually unrelated. No cluster.
# SKIP

# tile_sql_fund_relational_select: 2 concepts
# sql.relational_model, sql.select_fundamentals
# The relational model is the conceptual foundation; SELECT is the first query.
# They're tightly coupled — you need the model to understand what SELECT does.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_sql_fund_relational_select",
    "title": "The Relational Model and SELECT Basics",
    "concept_ids": ["sql.relational_model", "sql.select_fundamentals"],
    "reasoning": "The relational model (tables, rows, columns, relationships) is the conceptual foundation for SQL, and SELECT is the first query that retrieves from it. A learner needs the model to understand what SELECT returns. These two concepts are the entry point to SQL and read as one idea: what a relational database is and how to query it."
})

# tile_sql_fund_alias_distinct: 2 concepts
# sql.aliasing, sql.distinct
# Aliasing and DISTINCT are both SELECT clause modifiers, but they serve
# different purposes (renaming vs deduplicating). They don't read as one idea.
# SKIP

# tile_sql_fund_filtering_rows: 3 concepts
# sql.where_filtering, sql.logical_operators, sql.null_handling
# WHERE and logical operators are inseparable — you use AND/OR/NOT inside WHERE.
# NULL handling is a special case of filtering (IS NULL / IS NOT NULL).
# CLUSTER: where_filtering + logical_operators (they compose naturally)
# null_handling stands alone — it's a distinct concept about NULL semantics
# that learners must understand separately (three-valued logic).
cluster_decisions.append({
    "tile_id": "tile_sql_fund_filtering_rows",
    "title": "Filtering Rows with WHERE and Logical Operators",
    "concept_ids": ["sql.where_filtering", "sql.logical_operators"],
    "reasoning": "WHERE and logical operators (AND, OR, NOT) are inseparable in practice — every non-trivial WHERE clause uses logical operators to combine conditions. They read as one idea: constructing a row filter. NULL handling involves three-valued logic (TRUE/FALSE/UNKNOWN) which is a distinct and often surprising concept that learners must understand on its own terms, so it is not clustered here."
})

# tile_sql_fund_sorting_limiting: 2 concepts
# sql.order_by, sql.limit_offset
# ORDER BY and LIMIT/OFFSET are both result-set modifiers that are always
# used together (sort then limit). They're parts of one idea: controlling output.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_sql_fund_sorting_limiting",
    "title": "Sorting and Limiting Results",
    "concept_ids": ["sql.order_by", "sql.limit_offset"],
    "reasoning": "ORDER BY and LIMIT/OFFSET are always used together to sort a result set and then take a slice of it (e.g., 'top 10 by revenue'). They read as two parts of one idea: controlling which rows appear in the output and in what order."
})

# tile_sql_fund_aggregating_data: 3 concepts
# sql.aggregate_functions, sql.group_by, sql.having
# These three are the complete aggregation pattern in SQL:
# aggregate functions compute summaries, GROUP BY groups rows, HAVING filters groups.
# They're always used together and form one idea.
# CLUSTER: all three
cluster_decisions.append({
    "tile_id": "tile_sql_fund_aggregating_data",
    "title": "Aggregating Data with GROUP BY",
    "concept_ids": ["sql.aggregate_functions", "sql.group_by", "sql.having"],
    "reasoning": "Aggregate functions (COUNT, SUM, AVG), GROUP BY, and HAVING are the three components of the SQL aggregation pattern. GROUP BY groups rows, aggregate functions summarize each group, and HAVING filters the groups. A learner cannot use any one of them effectively without understanding the others — they form a single mental model: 'group rows and summarize each group, optionally filtering groups.'"
})

# tile_sql_case_expressions: 1 concept — skip
# tile_sql_style_conventions: 1 concept — skip

# tile_sql_text_dates_casts: 3 concepts
# sql.string_functions, sql.date_time_functions, sql.type_casting
# These are three categories of scalar functions. String and date functions
# are both about transforming column values; type casting is about converting types.
# They're all "scalar function" operations but address different data types.
# CLUSTER: string_functions + date_time_functions (both transform text/date values)
# type_casting stands alone (it's about type conversion, not string/date manipulation)
cluster_decisions.append({
    "tile_id": "tile_sql_text_dates_casts",
    "title": "Text and Date Functions",
    "concept_ids": ["sql.string_functions", "sql.date_time_functions"],
    "reasoning": "String functions (UPPER, LOWER, TRIM, SUBSTRING, CONCAT) and date/time functions (DATE_TRUNC, EXTRACT, DATEDIFF) are both categories of scalar functions that transform column values in SELECT. They are often used together in data cleaning and reporting queries. Type casting (CAST, ::) is a distinct operation about converting between data types and is better shown separately."
})

# tile_sql_null_fallback_and_union: 2 concepts
# sql.coalesce, sql.union
# COALESCE (null fallback) and UNION (combining result sets) are quite different
# operations. They don't read as parts of one idea.
# SKIP

# tile_datamodel_entities_keys: 2 concepts
# datamodel.entities_tables, datamodel.primary_keys
# Entities/tables and primary keys are inseparable — a primary key is what
# makes a table an entity. They're two aspects of one idea.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_datamodel_entities_keys",
    "title": "Entities, Tables, and Primary Keys",
    "concept_ids": ["datamodel.entities_tables", "datamodel.primary_keys"],
    "reasoning": "Entities/tables and primary keys are inseparable in the relational model — a primary key is what uniquely identifies each row in a table and makes it a proper entity. A learner cannot understand what a table represents without understanding primary keys. They read as two aspects of one idea: what a table is and how rows are identified."
})

# tile_datamodel_foreign_keys_one_to_many: 2 concepts
# datamodel.foreign_keys_referential_integrity, datamodel.one_to_many
# Foreign keys implement one-to-many relationships — they're two aspects of
# the same concept: how tables relate to each other.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_datamodel_foreign_keys_one_to_many",
    "title": "Foreign Keys and One-to-Many Relationships",
    "concept_ids": ["datamodel.foreign_keys_referential_integrity", "datamodel.one_to_many"],
    "reasoning": "Foreign keys are the mechanism that implements one-to-many relationships — a foreign key in the 'many' table points to the primary key in the 'one' table. These two concepts are two sides of the same coin: the relationship pattern and the column that enforces it. They are always taught together in data modeling."
})

# tile_datamodel_normalization_many_to_many: 2 concepts
# datamodel.normalization_basics, datamodel.many_to_many_junction_tables
# Normalization and many-to-many relationships (junction tables) are related:
# junction tables are a normalization technique for many-to-many relationships.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_datamodel_normalization_many_to_many",
    "title": "Normalization and Many-to-Many Relationships",
    "concept_ids": ["datamodel.normalization_basics", "datamodel.many_to_many_junction_tables"],
    "reasoning": "Normalization (reducing redundancy by splitting data into related tables) and many-to-many junction tables (the normalization technique for many-to-many relationships) are tightly linked. A junction table is the canonical example of normalization in action. They read as two aspects of one idea: how to structure data to avoid redundancy."
})

# tile_datamodel_dimensional_er: 1 concept — skip

# tile_sql_adv_joining_tables: 3 concepts
# sql.inner_join, sql.composite_join_conditions, sql.outer_joins
# These are three join concepts. Inner join and outer joins are variants that
# learners MUST learn to tell apart (they produce different result sets).
# Composite join conditions are an extension of any join type.
# CLUSTER: inner_join + composite_join_conditions (composite conditions extend inner join)
# outer_joins stands alone — learners must distinguish INNER from OUTER clearly.
# 
# Actually, the GENERATOR.md explicitly says "two join types that learners must
# learn to tell apart may be better as separate steps." Inner vs outer joins
# is exactly this case. So no cluster for this tile.
# SKIP

# tile_sql_adv_execution_order_subquery_where: 2 concepts
# sql.clause_execution_order, sql.subquery_in_where
# Execution order explains why subqueries work where they do.
# They're related but execution order is a meta-concept about SQL processing,
# while subquery_in_where is a specific technique.
# CLUSTER: yes — execution order explains subquery placement
cluster_decisions.append({
    "tile_id": "tile_sql_adv_execution_order_subquery_where",
    "title": "Query Execution Order and Subqueries in WHERE",
    "concept_ids": ["sql.clause_execution_order", "sql.subquery_in_where"],
    "reasoning": "SQL clause execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) directly explains why subqueries can appear in WHERE: the subquery runs first, producing a value that WHERE can filter on. Understanding execution order is the prerequisite mental model for understanding subquery placement. These two concepts read as one idea: how SQL processes a query and how that enables subqueries."
})

# tile_sql_adv_subquery_from_cte: 2 concepts
# sql.subquery_in_from, sql.cte
# Subqueries in FROM and CTEs are two ways to create a named intermediate
# result set. They're variants of one idea: building a query in layers.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_sql_adv_subquery_from_cte",
    "title": "Subqueries in FROM and Common Table Expressions",
    "concept_ids": ["sql.subquery_in_from", "sql.cte"],
    "reasoning": "Subqueries in FROM (derived tables) and CTEs (WITH clause) are two syntactic approaches to the same idea: creating a named intermediate result set that the outer query can reference. CTEs are the modern, more readable alternative to subqueries in FROM. Showing them together makes the equivalence and the trade-offs immediately clear."
})

# tile_spreadsheet_grid_references: 2 concepts
# spreadsheet.grid_model, spreadsheet.cell_references_ranges
# The grid model and cell references are inseparable — cell references are
# how you address locations in the grid.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_grid_references",
    "title": "The Spreadsheet Grid and Cell References",
    "concept_ids": ["spreadsheet.grid_model", "spreadsheet.cell_references_ranges"],
    "reasoning": "The spreadsheet grid model (rows, columns, cells) and cell references/ranges (A1, B2:D5) are inseparable — cell references are the addressing system for the grid. A learner cannot write a formula without understanding both. They read as two aspects of one foundational idea: how a spreadsheet is structured and how to point to locations in it."
})

# tile_spreadsheet_tables_named_ranges: 2 concepts
# spreadsheet.structured_tables, spreadsheet.named_ranges
# Structured tables and named ranges are both ways to give a data range a name
# and reference it by name. They're variants of one idea: named data regions.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_tables_named_ranges",
    "title": "Structured Tables and Named Ranges",
    "concept_ids": ["spreadsheet.structured_tables", "spreadsheet.named_ranges"],
    "reasoning": "Structured tables (Excel Tables / Google Sheets tables with auto-expanding references) and named ranges are both mechanisms for giving a data region a meaningful name that can be referenced in formulas. They read as two variants of one idea: naming data regions to make formulas more readable and maintainable."
})

# tile_spreadsheet_sorting_filtering: 2 concepts
# spreadsheet.sorting, spreadsheet.filtering
# Sorting and filtering are the two basic data exploration operations in a spreadsheet.
# They're always taught together and complement each other.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_sorting_filtering",
    "title": "Sorting and Filtering Data",
    "concept_ids": ["spreadsheet.sorting", "spreadsheet.filtering"],
    "reasoning": "Sorting (reordering rows by a column) and filtering (showing only rows that match a condition) are the two basic data exploration operations in a spreadsheet. They are always taught together and are often used in sequence: filter to a subset, then sort within it. They read as two parts of one idea: navigating and exploring tabular data."
})

# tile_spreadsheet_formatting_validation: 2 concepts
# spreadsheet.conditional_formatting, spreadsheet.data_validation
# Conditional formatting (visual rules) and data validation (input rules) are
# both about applying rules to cells, but they serve different purposes
# (display vs input control). They don't read as parts of one idea.
# SKIP

# tile_spreadsheet_cleaning_cross_sheet: 3 concepts
# spreadsheet.remove_duplicates_cleaning, spreadsheet.text_to_columns_split,
# spreadsheet.cross_sheet_references
# Remove duplicates and text-to-columns are both data cleaning operations.
# Cross-sheet references are a navigation/formula concept.
# CLUSTER: remove_duplicates + text_to_columns (both are cleaning operations)
# cross_sheet_references stands alone (different concept: formula navigation)
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_cleaning_cross_sheet",
    "title": "Removing Duplicates and Splitting Text",
    "concept_ids": ["spreadsheet.remove_duplicates_cleaning", "spreadsheet.text_to_columns_split"],
    "reasoning": "Removing duplicates and splitting text (Text to Columns / SPLIT) are both data cleaning operations applied to raw imported data. They are often used in sequence when cleaning a dataset: split combined fields, then remove duplicate rows. Cross-sheet references are a formula navigation concept and belong to a different idea."
})

# tile_spreadsheet_formula_syntax_refs: 2 concepts
# spreadsheet.formula_syntax, spreadsheet.relative_absolute_references
# Formula syntax and relative/absolute references are inseparable — you can't
# write a formula without understanding reference types.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_formula_syntax_refs",
    "title": "Writing Formulas and Reference Types",
    "concept_ids": ["spreadsheet.formula_syntax", "spreadsheet.relative_absolute_references"],
    "reasoning": "Formula syntax (= sign, operators, function calls) and relative/absolute references ($A$1 vs A1) are inseparable — every formula uses references, and whether those references are relative or absolute determines how the formula behaves when copied. They read as two aspects of one idea: how to write a formula correctly."
})

# tile_spreadsheet_aggregation_logical: 2 concepts
# spreadsheet.aggregation_functions, spreadsheet.logical_functions
# SUM/COUNT/AVERAGE and IF/AND/OR are both formula categories but serve
# different purposes (summarizing vs decision-making). They don't read as one idea.
# SKIP

# tile_spreadsheet_text_date_conditional_agg: 4 concepts
# spreadsheet.text_combining, spreadsheet.text_extraction,
# spreadsheet.date_functions, spreadsheet.conditional_aggregation
# Text combining and text extraction are two text manipulation operations —
# variants of one idea (working with text in formulas).
# Date functions are a separate category.
# Conditional aggregation (SUMIF, COUNTIF) is a separate category.
# CLUSTER: text_combining + text_extraction (both are text manipulation)
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_text_date_conditional_agg",
    "title": "Text Combining and Text Extraction",
    "concept_ids": ["spreadsheet.text_combining", "spreadsheet.text_extraction"],
    "reasoning": "Text combining (CONCAT, TEXTJOIN, &) and text extraction (LEFT, RIGHT, MID, FIND) are two complementary text manipulation operations — one builds strings from parts, the other pulls parts from strings. They are variants of one idea: working with text values in formulas, and are often used together when cleaning or reformatting text data."
})

# tile_spreadsheet_lookups_troubleshooting: 3 concepts
# spreadsheet.vlookup_xlookup, spreadsheet.index_match, spreadsheet.formula_error_troubleshooting
# VLOOKUP/XLOOKUP and INDEX/MATCH are two lookup approaches — learners must
# learn to tell them apart (different syntax, different flexibility).
# Formula error troubleshooting is a separate skill.
# CLUSTER: vlookup_xlookup + index_match (both are lookup functions, important to contrast)
# formula_error_troubleshooting stands alone (different skill: debugging)
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_lookups_troubleshooting",
    "title": "VLOOKUP/XLOOKUP and INDEX/MATCH",
    "concept_ids": ["spreadsheet.vlookup_xlookup", "spreadsheet.index_match"],
    "reasoning": "VLOOKUP/XLOOKUP and INDEX/MATCH are the two main lookup approaches in spreadsheets. Showing them together makes the trade-offs immediately clear: VLOOKUP/XLOOKUP is simpler but limited to left-to-right lookups; INDEX/MATCH is more flexible. Learners need to choose between them in practice. Formula error troubleshooting is a debugging skill that applies to all formulas and is better shown separately."
})

# tile_spreadsheet_pivot_tables: 2 concepts
# spreadsheet.pivot_tables, spreadsheet.pivot_summarization
# Building a pivot table and summarizing with it are two steps of one workflow.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_spreadsheet_pivot_tables",
    "title": "Building and Summarizing Pivot Tables",
    "concept_ids": ["spreadsheet.pivot_tables", "spreadsheet.pivot_summarization"],
    "reasoning": "Building a pivot table (inserting, configuring rows/columns/values) and summarizing with it (choosing aggregation functions, filtering, grouping) are two steps of one workflow. A learner cannot summarize with a pivot table without first building one. They read as the setup and the use of the same tool."
})

# tile_spreadsheet_chart_types: 3 concepts
# spreadsheet.bar_chart_creation, spreadsheet.line_chart_creation, spreadsheet.pie_chart_creation
# These are three chart types that learners must learn to tell apart
# (different use cases: comparison vs trend vs proportion).
# GENERATOR.md says concepts that learners must learn to tell apart may be
# better as separate steps. These are exactly that case.
# SKIP

# tile_viz_figures_layout_plotting: 3 concepts
# viz.matplotlib_figure_axes, viz.figure_size_layout, viz.pyplot_basic_plotting
# Figure/axes model, figure size/layout, and basic plotting are three aspects
# of setting up a matplotlib figure. They're all part of one idea: creating a plot.
# CLUSTER: all three — they're the setup steps for any matplotlib plot
cluster_decisions.append({
    "tile_id": "tile_viz_figures_layout_plotting",
    "title": "Figures, Layout, and Basic Plotting",
    "concept_ids": ["viz.matplotlib_figure_axes", "viz.figure_size_layout", "viz.pyplot_basic_plotting"],
    "reasoning": "The Figure/Axes model, figure size and layout configuration, and basic pyplot plotting are three aspects of the same setup: creating a matplotlib figure. A learner needs all three to produce their first plot. They read as the initialization steps of any matplotlib visualization and are always taught together."
})

# tile_viz_bar_histograms: 2 concepts
# viz.bar_charts, viz.histograms
# Bar charts and histograms look similar but serve different purposes
# (categorical comparison vs continuous distribution). Learners must learn
# to tell them apart. However, they're both basic chart types and the
# distinction is the key learning — showing them together makes the
# contrast visible.
# CLUSTER: yes — the contrast is the lesson
cluster_decisions.append({
    "tile_id": "tile_viz_bar_histograms",
    "title": "Bar Charts and Histograms",
    "concept_ids": ["viz.bar_charts", "viz.histograms"],
    "reasoning": "Bar charts (categorical comparison) and histograms (continuous distribution) are often confused because they look similar. Showing them together makes the critical distinction immediately visible: bar charts have gaps between bars and compare categories; histograms have no gaps and show distribution. The contrast is the core learning, making them ideal for a cluster."
})

# tile_viz_line_scatter_box: 3 concepts
# viz.line_plots, viz.scatter_plots, viz.box_plots
# These are three chart types for different analytical purposes:
# line = trend over time, scatter = relationship between variables, box = distribution.
# Learners must learn to tell them apart (different use cases).
# CLUSTER: line_plots + scatter_plots (both show relationships between two variables)
# box_plots stands alone (shows distribution, different purpose)
cluster_decisions.append({
    "tile_id": "tile_viz_line_scatter_box",
    "title": "Line Plots and Scatter Plots",
    "concept_ids": ["viz.line_plots", "viz.scatter_plots"],
    "reasoning": "Line plots (trends over an ordered axis, typically time) and scatter plots (relationship between two continuous variables) are both two-variable charts that learners often conflate. Showing them together makes the distinction clear: line plots connect ordered points to show trend; scatter plots show correlation between unordered pairs. Box plots show distribution rather than relationships and are better shown separately."
})

# tile_viz_labeling_chart_selection: 2 concepts
# viz.labeling_annotation, viz.chart_type_selection
# Labeling/annotation and chart type selection are both about making a chart
# communicate clearly, but they're different skills (visual polish vs chart choice).
# SKIP

# tile_viz_seaborn_stats_themes: 3 concepts
# viz.seaborn_dataframe_plotting, viz.seaborn_statistical_functions, viz.seaborn_themes_palettes
# These are three aspects of seaborn: basic plotting, statistical functions, themes.
# seaborn_dataframe_plotting and seaborn_statistical_functions are both about
# creating seaborn plots — they're parts of one idea.
# seaborn_themes_palettes is about styling — a separate concern.
# CLUSTER: seaborn_dataframe_plotting + seaborn_statistical_functions
cluster_decisions.append({
    "tile_id": "tile_viz_seaborn_stats_themes",
    "title": "Seaborn DataFrame Plotting and Statistical Functions",
    "concept_ids": ["viz.seaborn_dataframe_plotting", "viz.seaborn_statistical_functions"],
    "reasoning": "Seaborn's DataFrame-aware plotting (sns.barplot, sns.scatterplot) and its statistical functions (sns.histplot with kde, sns.regplot, sns.boxplot) are two levels of the same library: basic chart creation and statistically-enhanced chart creation. They read as two aspects of one idea: using seaborn to visualize data. Themes and palettes are a styling concern that applies after the chart is created."
})

# tile_viz_custom_multi_panel: 2 concepts
# viz.custom_styling_theming, viz.multi_panel_figures
# Custom styling and multi-panel figures are both advanced matplotlib topics
# but serve different purposes (aesthetics vs layout). They don't read as one idea.
# SKIP

# tile_stats_ab_test_lift: 2 concepts
# stats.ab_test_structure, stats.lift_interpretation
# A/B test structure and lift interpretation are two aspects of the same
# experiment: how to set it up and how to read the result.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stats_ab_test_lift",
    "title": "A/B Test Structure and Lift",
    "concept_ids": ["stats.ab_test_structure", "stats.lift_interpretation"],
    "reasoning": "A/B test structure (control vs treatment, random assignment, metric selection) and lift interpretation (the relative improvement of treatment over control) are two aspects of the same experiment: how to design it and how to read its primary result. A learner cannot interpret lift without understanding the test structure that produced it."
})

# tile_stats_sample_size_significance: 3 concepts
# stats.sample_size_effect_concept, stats.significance_confidence_concept,
# stats.business_conclusion_from_experiment
# These three are the complete picture of experiment interpretation:
# sample size/effect size, statistical significance/confidence, and business conclusions.
# They're all about reading experiment results correctly.
# CLUSTER: sample_size_effect_concept + significance_confidence_concept
# (both are statistical concepts about experiment validity)
# business_conclusion_from_experiment stands alone (it's the application/translation step)
cluster_decisions.append({
    "tile_id": "tile_stats_sample_size_significance",
    "title": "Sample Size, Effect Size, and Statistical Significance",
    "concept_ids": ["stats.sample_size_effect_concept", "stats.significance_confidence_concept"],
    "reasoning": "Sample size/effect size and statistical significance/confidence intervals are two interconnected statistical concepts for evaluating experiment validity. Sample size determines whether an effect can be detected; significance tells you whether the detected effect is likely real. They are always interpreted together and form one idea: 'is this result trustworthy?' Business conclusions from experiments are the translation step that applies these concepts to a decision, and are better shown separately."
})

# tile_stakeholder_framing_requirements: 4 concepts
# stakeholder.identifying_decision_need, stakeholder.precise_finding_statement,
# stakeholder.framing_analytical_question, stakeholder.identifying_requirements
# These four are all about the front-end of stakeholder work: understanding
# what the stakeholder needs before doing analysis.
# identifying_decision_need + framing_analytical_question are tightly linked
# (identify the decision, then frame the question).
# precise_finding_statement + identifying_requirements are about outputs.
# CLUSTER: identifying_decision_need + framing_analytical_question
# (two steps of one process: understand the need, frame the question)
cluster_decisions.append({
    "tile_id": "tile_stakeholder_framing_requirements",
    "title": "Identifying Decisions and Framing Analytical Questions",
    "concept_ids": ["stakeholder.identifying_decision_need", "stakeholder.framing_analytical_question"],
    "reasoning": "Identifying the decision a stakeholder needs to make and framing the analytical question that will inform that decision are two sequential steps of one process: translating a business need into an analysis brief. They read as cause and effect — the decision need motivates the analytical question. Precise finding statements and requirements identification are output-oriented concepts that build on this foundation."
})

# tile_stakeholder_recommendation_translation: 2 concepts
# stakeholder.data_driven_recommendation, stakeholder.plain_language_translation
# Data-driven recommendations and plain-language translation are two aspects
# of communicating findings: what to recommend and how to say it.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stakeholder_recommendation_translation",
    "title": "Recommendations and Plain-Language Translation",
    "concept_ids": ["stakeholder.data_driven_recommendation", "stakeholder.plain_language_translation"],
    "reasoning": "Forming a data-driven recommendation and translating it into plain language are two steps of the same communication act: deciding what to say and then saying it in terms the stakeholder understands. A recommendation that cannot be translated into plain language is not yet complete. They read as two parts of one idea: communicating a finding as an actionable recommendation."
})

# tile_stakeholder_prioritizing_framing_context: 3 concepts
# stakeholder.prioritizing_findings_by_relevance, stakeholder.actionable_recommendation_framing,
# stakeholder.narrative_context_setup
# Prioritizing findings and framing recommendations are both about selecting
# and shaping what to communicate. Narrative context setup is about how to
# open a presentation.
# CLUSTER: prioritizing_findings + actionable_recommendation_framing
# (both are about selecting and shaping the message)
cluster_decisions.append({
    "tile_id": "tile_stakeholder_prioritizing_framing_context",
    "title": "Prioritizing Findings and Framing Recommendations",
    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance", "stakeholder.actionable_recommendation_framing"],
    "reasoning": "Prioritizing findings by relevance (selecting which results matter most to the stakeholder) and framing recommendations as actionable (stating what to do, not just what was found) are two aspects of the same editorial decision: what to lead with and how to say it. Narrative context setup is about structuring the opening of a presentation, which is a distinct communication skill."
})

# tile_stakeholder_tailoring_anticipating: 2 concepts
# stakeholder.tailoring_detail_to_audience, stakeholder.anticipating_questions_objections
# Tailoring detail and anticipating questions are both about audience awareness.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stakeholder_tailoring_anticipating",
    "title": "Tailoring Detail and Anticipating Questions",
    "concept_ids": ["stakeholder.tailoring_detail_to_audience", "stakeholder.anticipating_questions_objections"],
    "reasoning": "Tailoring the level of detail to the audience and anticipating their questions and objections are two aspects of audience-aware communication. Both require the analyst to model the stakeholder's perspective: what do they need to know, and what will they push back on? They read as two parts of one idea: preparing a presentation for a specific audience."
})

# tile_stakeholder_chart_matching_simplifying: 2 concepts
# stakeholder.chart_type_to_point_matching, stakeholder.simplifying_charts_for_audience
# Matching chart type to the point and simplifying charts are both about
# making charts communicate clearly to a non-technical audience.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stakeholder_chart_matching_simplifying",
    "title": "Matching and Simplifying Charts for an Audience",
    "concept_ids": ["stakeholder.chart_type_to_point_matching", "stakeholder.simplifying_charts_for_audience"],
    "reasoning": "Choosing the right chart type for the point being made and simplifying charts for a non-technical audience are two aspects of the same skill: making a visualization communicate clearly. They read as two parts of one idea: chart design for stakeholder communication."
})

# tile_stakeholder_presentation_structure: 2 concepts
# stakeholder.presentation_structure_basics, stakeholder.executive_summary_writing
# Presentation structure and executive summary writing are both about
# organizing a communication for a stakeholder. They're parts of one idea.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_stakeholder_presentation_structure",
    "title": "Structuring Presentations and Writing Executive Summaries",
    "concept_ids": ["stakeholder.presentation_structure_basics", "stakeholder.executive_summary_writing"],
    "reasoning": "Presentation structure (opening, findings, recommendation, appendix) and executive summary writing (one-page distillation of the key finding and recommendation) are two formats for the same communication goal: delivering analytical results to a stakeholder. They read as two variants of one idea: how to organize and present findings."
})

# tile_capstone_question_workflow: 3 concepts
# capstone.defining_business_question, capstone.data_retrieval_method_selection,
# capstone.end_to_end_workflow_structure
# These three are the planning phase of the capstone:
# define the question, choose how to get the data, plan the workflow.
# They're sequential steps of one planning process.
# CLUSTER: all three
cluster_decisions.append({
    "tile_id": "tile_capstone_question_workflow",
    "title": "Defining the Question and Planning the Workflow",
    "concept_ids": ["capstone.defining_business_question", "capstone.data_retrieval_method_selection", "capstone.end_to_end_workflow_structure"],
    "reasoning": "Defining the business question, selecting the data retrieval method, and structuring the end-to-end workflow are three sequential planning steps for a capstone project. They form one idea: scoping and planning an analysis before executing it. A learner cannot choose a retrieval method without a defined question, and cannot structure the workflow without knowing both."
})

# tile_capstone_integrate_tools_model: 4 concepts
# capstone.integrate_sql, capstone.integrate_spreadsheet,
# capstone.integrate_python_pandas, capstone.building_data_model
# These four are about integrating tools in the capstone.
# integrate_sql, integrate_spreadsheet, integrate_python_pandas are three
# tool integration steps — variants of one idea (applying each tool).
# building_data_model is a separate structural task.
# CLUSTER: integrate_sql + integrate_spreadsheet + integrate_python_pandas
# (three tool integration steps in one workflow)
cluster_decisions.append({
    "tile_id": "tile_capstone_integrate_tools_model",
    "title": "Integrating SQL, Spreadsheets, and pandas",
    "concept_ids": ["capstone.integrate_sql", "capstone.integrate_spreadsheet", "capstone.integrate_python_pandas"],
    "reasoning": "Integrating SQL, spreadsheets, and pandas are three parallel tool-application steps in the capstone workflow — each applies one of the path's core tools to the project dataset. They read as variants of one idea: using each tool for what it does best in a real analysis. Building the data model is a structural design task that precedes or accompanies tool integration and is better shown separately."
})

# tile_capstone_stats_dashboard: 2 concepts
# capstone.applying_descriptive_statistics, capstone.building_dashboard_or_viz
# Applying stats and building the visualization are two steps of the
# analysis and presentation phase.
# CLUSTER: yes
cluster_decisions.append({
    "tile_id": "tile_capstone_stats_dashboard",
    "title": "Applying Statistics and Building the Visualization",
    "concept_ids": ["capstone.applying_descriptive_statistics", "capstone.building_dashboard_or_viz"],
    "reasoning": "Applying descriptive statistics and building the dashboard or visualization set are two sequential steps of the capstone's analysis and presentation phase: compute the summaries, then visualize them. The statistics inform what to show; the visualization makes it communicable. They read as two parts of one idea: turning data into insight."
})

# tile_capstone_execution_narration_delivery: 3 concepts
# capstone.independent_execution, capstone.narrated_stakeholder_summary,
# capstone.documenting_presenting_deliverable
# These three are the delivery phase of the capstone:
# execute independently, narrate the summary, document and present.
# They're sequential steps of one delivery process.
# CLUSTER: narrated_stakeholder_summary + documenting_presenting_deliverable
# (both are about the final deliverable)
# independent_execution stands alone (it's about the execution process, not the output)
cluster_decisions.append({
    "tile_id": "tile_capstone_execution_narration_delivery",
    "title": "Narrating and Delivering the Capstone",
    "concept_ids": ["capstone.narrated_stakeholder_summary", "capstone.documenting_presenting_deliverable"],
    "reasoning": "The narrated stakeholder summary and the documented/presented deliverable are two forms of the same final output: communicating the capstone results. The narration is the verbal presentation; the documentation is the written artifact. They read as two aspects of one idea: delivering the completed analysis to a stakeholder. Independent execution is the process of doing the work, which is a distinct concept."
})

# -----------------------------------------------------------------------
# Build the clusters array
# -----------------------------------------------------------------------
clusters = []
cluster_counter = 1

for decision in cluster_decisions:
    tile_id = decision["tile_id"]
    # Get path_id from first concept in the cluster
    first_concept = concepts_by_id[decision["concept_ids"][0]]
    path_id = first_concept["path_id"]
    
    cluster_id = f"cluster_{cluster_counter:03d}"
    cluster_counter += 1
    
    clusters.append({
        "cluster_id": cluster_id,
        "path_id": path_id,
        "tile_id": tile_id,
        "title": decision["title"],
        "concept_ids": decision["concept_ids"],
        "reasoning": decision["reasoning"]
    })

# -----------------------------------------------------------------------
# Build the output artifact
# -----------------------------------------------------------------------
now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

output = {
    "metadata": {
        "batch_id": "glossary_batch_001_data_analyst_pilot",
        "stage_id": "12_cluster_pass",
        "model": "us.anthropic.claude-sonnet-4-6",
        "prompt_version": "12_cluster_pass@v1",
        "generated_at": now_utc,
        "parent_artifact_hashes": {
            "extracted_concepts.json": extracted_hash,
            "glossary_bundles_draft.json": bundles_hash
        }
    },
    "batch_id": "glossary_batch_001_data_analyst_pilot",
    "clusters": clusters
}

output_path = "batches/glossary_batch_001_data_analyst_pilot/clusters.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written {output_path}")
print(f"Total clusters: {len(clusters)}")
for c in clusters:
    print(f"  {c['cluster_id']}: {c['tile_id']} -> {c['concept_ids']}")
