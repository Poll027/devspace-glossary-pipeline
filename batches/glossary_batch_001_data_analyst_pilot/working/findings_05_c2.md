## Stage 05 evaluation of chunk c2 (`glossary_pass_a.part.c2.json`, 30 concepts)

The chunk fails on 7 blocking defects. Four are overclaims, two are code examples that don't do what the text says, and one uses Python the learner was never taught. All 30 entries are otherwise structurally clean, and every worked number checks out.

File evaluated: `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK/batches/glossary_batch_001_data_analyst_pilot/glossary_pass_a.part.c2.json` (not edited).

### Scripted checks (all pass)
- **Schema:** `schema_check.py glossary_pass_a.schema.json` reports VALID. I ran it on a scratch copy.
- **Coverage tags:** every required fact and misconception across the 30 briefs is tagged by some block. No fact_id is unknown, no optional fact is tagged, and block ids are unique.
- **video_need consistency:** every NONE has an empty `preferred_visual_modes` list (4 entries). Every LOW has one mode (2 entries). Every MEDIUM and HIGH has at least one mode.
- **Video words:** "video", "clip" and "watch" never appear in teaching-block text. They only appear in `video_need.reason`, which is not shown to learners.

### Worked numbers
- **Delivery-time batch 18, 20, 22, 22, 26, 28, 80:**
  - sum 216, mean 30.857 (text says ~30.9)
  - median 22, mode 22, range 62
  - sum of squared deviations 2886.857 (~2886.9)
  - sample variance 481.14 (~481.1), sample standard deviation 21.935 (~21.9)
  - All correct, and pandas' `mean()`, `median()` and `std()` give 30.9, 22 and 21.9 as `stats.pandas_descriptive_stats` says.
- **Frequency table:** 4 + 9 + 5 + 2 + 1 = 21, and the 20–30 bin is the peak. Correct.
- **Correlation comparisons:** 0.82 is strongest and 0.38 weakest. Correct.

### pandas traces (pandas 3.0.6 in a scratch venv)
These all behave as the text says:
- **Series and DataFrame basics:**
  - `pd.Series([...])` gets index 0..6; the dict version uses its keys as the index.
  - `df[col]` returns a Series.
- **Selection and filtering:**
  - `loc[2:4]` returns 3 rows (labels 2, 3, 4); `loc[3]` equals `loc[3, :]`.
  - `iloc[0:3]` returns positions 0–2; `iloc[0:3, 0:2]` has shape (3, 2).
  - The boolean filter keeps [26, 28, 80], and leaving out the parentheses raises TypeError.
- **Sorting and relabelling:**
  - `sort_values` with `ascending=[True, False]` gives cities A→Z and slowest time first within each city.
  - `rename` with both `columns=` and `index=` works.
- **Type and text cleaning:**
  - `astype` with a dict works; `astype(float)` on "unknown" raises ValueError.
  - `.dt.month` works.
  - `.str.strip().str.lower()` turns all three Lagos variants into "lagos".
- **Duplicates and missing values:**
  - `drop_duplicates(keep="last")` keeps the second #1042 row.
  - `fillna(median)` works.
- **map, apply and concat:**
  - `map` with a dict works.
  - `apply(label_speed, axis=1)` works.
  - `concat` stacks rows by default and puts tables side by side with `axis=1`.
- **merge and groupby:**
  - An inner `merge` keeps only matched keys; `how="left"` fills unmatched rows with NaN.
  - `groupby(...).mean()` and `.agg(["mean", "sum"])` work.
- **Reshaping:**
  - `melt` produces the columns variable and value, which `var_name` and `value_name` rename.
  - `pivot_table` averages by default and sums with `aggfunc="sum"`.

Two traces fail:
- **`describe()`:** its output rows are count, mean, std, min, 25%, 50%, 75% and max. There is no "range" row, but `pandas.inspecting_dataframes` tb6 says there is.
- **`pivot_table`:** `city_deliveries.pivot_table(index="city", columns="month", values="deliveries")` raises KeyError. That's because `city_deliveries` is the wide table in `pandas.melt_reshaping`, and that entry never saves the long result under that name.

### Boundary
- Known TOC conflicts are handled correctly and are advisory under `orchestrator_notes.md`: the "skewed" wording in measures of center, the histogram practice in distribution shape, shape checks in reading/creating DataFrames, and SQL mirroring in merge.
- `lambda` is used in `pandas.map_substitution`. No concept in `extracted_concepts.json` or the coverage briefs teaches lambda (checked by grep), so the example depends on knowledge the learner never gets. This is blocking.

VERDICT: FAIL

BLOCKING stats.correlation@data_analyst: tb4 → "farther deliveries reliably take noticeably longer" upgrades f2's "tend to" to "reliably", and "noticeably longer" claims correlation shows how big the effect is, which no fact supports (correlation measures strength of a linear relationship, not slope) → replace the sentence after the f3 statement with: "Suppose the correlation between distance and delivery time in this dataset comes out to 0.82 -- close to +1, so distance and delivery time have a strong positive linear relationship: farther deliveries tend to take longer."

BLOCKING pandas.inspecting_dataframes@data_analyst: tb6 → says `describe()` reports "range", but the brief's f2 in `stats.pandas_descriptive_stats` and real pandas output list count, mean, std, min, quartiles and max, with no range → replace with: "`orders.describe()` would summarize delivery_time_minutes with statistics like its count, mean, minimum, and maximum, without you writing each calculation separately."

BLOCKING pandas.reading_data@data_analyst: tb1 → "Delivery records usually start life outside Python ... reading them into pandas is the first step of any analysis" adds an unsupported "usually" and an absolute ordering claim ("first step of any analysis") that no fact supports → replace tb1 with: "Suppose your delivery records arrive as a CSV export or an Excel workbook. Before pandas can work with them, you read the file into a DataFrame."

BLOCKING pandas.merge_join@data_analyst: tb6 → "merge() always starts from a shared key" adds an absolute not in f1–f4 (f1 only says a shared key "can be specified with the on parameter") → replace tb6 with: "merge() matches rows on a shared key; setting the how parameter decides whether unmatched rows on either side get dropped or kept with NA gaps."

BLOCKING pandas.pivot_table_reshaping@data_analyst: tb1/tb3 → "the long-format city_deliveries table from before" refers back to melt, where `city_deliveries` is the wide table; the traced tb3 call raises KeyError 'deliveries', so the code doesn't do what the text says → tb1: "Suppose the long table that melt produced earlier is saved as long_deliveries, with one row per city-month and the columns city, month, and deliveries -- and it needs to go back to a wide table: cities as rows, months as columns."; in tb3 replace `city_deliveries.pivot_table(index="city", columns="month", values="deliveries")` with `long_deliveries.pivot_table(index="city", columns="month", values="deliveries")`, and leave the rest of tb3 unchanged.

BLOCKING pandas.map_substitution@data_analyst: tb1 → the example needs `lambda`, which is never taught anywhere in the TOC (only `python.defining_calling_functions` is allowed), so the learner must understand untaught syntax to follow the f1 example → replace everything after the f1 statement with: "with `def to_upper(code): return code.upper()` defined first, `orders["city_code"].map(to_upper)` uppercases every city code in the column."

BLOCKING pandas.apply_transform@data_analyst: tb1 → "logic specific enough that no single built-in method already does it" is a new claim about what pandas can do, and it's contestable (`pd.cut` with labels does this in one call) → replace tb1 with: "Suppose you want to label every order "fast" or "slow" based on its delivery time, using a rule you write yourself as a small function."

ADVISORY stats.measures_of_spread@data_analyst: tb6 → "standard deviation being the one expressed in the original units" can be read as "the only one of the three", but the range (62 minutes) is also in original units → reword to "with standard deviation, unlike variance, expressed in the original units".

ADVISORY stats.descriptive_measures_of_center@data_analyst: tb6 → "they ... react differently to a batch that includes one unusually large value" extends f4 (mean vs median only) to the mode → say "the mean and median react differently".

ADVISORY stats.distribution_shape@data_analyst: tb2/tb4 → the single 80-minute value is used as the whole "long tail", which blurs shape with outlier-spotting, the exact distinction the central mental model draws (and `stats.outlier_reasoning` reuses the same value as its outlier) → illustrate right skew with a gradual tail, e.g. 18, 20, 22, 22, 26, 28, 34, 41, 52.

ADVISORY stats.frequency_distribution_reading@data_analyst: tb3 → the frequency table skips the empty 50–80 bins → list "50-80 minutes, 0 orders" so the gap before the far-out delivery is visible.

ADVISORY stats.correlation@data_analyst: tb3/tb4 → there's no worked negative example, though the practice objective uses -0.72 → add one line, e.g. drivers on shift vs delivery time at -0.65 meaning more drivers tend to go with shorter times.

ADVISORY stats.correlation_interpretation@data_analyst: tb1/tb2 → all three r values are positive, so f1's "regardless of sign" is stated but never shown → make one pair negative (e.g. -0.55) and compare by absolute value. Separately, tb3's "directly cause" leans on the next concept (causation), so prefer f2's "directly linked".

ADVISORY stats.pandas_descriptive_stats@data_analyst: tb2 → assumes `orders` holds exactly the seven-value batch, but other entries show 3 or 250 rows → add "if delivery_time_minutes holds that seven-order batch". Also nothing interprets mean or std, which the practice objective asks for → add one sentence of interpretation.

ADVISORY pandas.dataframe_series_model@data_analyst: tb4/tb5 → tb4 never assigns `orders =`, yet tb5 uses `orders` → prefix `orders = `. tb5's `orders['delivery_time_minutes'] < 25` uses element-wise comparison, which `pandas.boolean_filtering` teaches later (a passing use, since the sentence only says "adds a new column") → swap in `orders['courier'] = ['Ada', 'Bayo', 'Chidi']`.

ADVISORY pandas.apply_transform@data_analyst: tb2 → `label_speed` is described with a `... if ... else ...` conditional expression, which is untaught (`python.conditional_statements` covers if/else statements) → show the body as an if/else statement. tb3's "when built-in vectorized methods don't already do what you need" is framing beyond f1; soften it.

ADVISORY pandas.inspecting_dataframes@data_analyst: tb7 → "running through all of them is the standard first step" goes beyond the facts (the central mental model partly supports it) → soften to "a common first step". Also tb2/tb3 have awkward double colons (fact sentence, colon, code).

ADVISORY pandas.missing_data_handling@data_analyst: tb5 → the drop-vs-fill decision rule is not in the facts → frame it as an example judgment, not a rule.

ADVISORY pandas.reading_data@data_analyst and pandas.groupby_aggregation@data_analyst: Core entries at 172 and 199 words (guide is 400–700), with no misconception block → add one grounded misconception each, e.g. `sep` for semicolon files, or the group key becoming the index.

ADVISORY chunk-wide: many blocks paste the fact sentence verbatim and then append code after a colon, which reads stiffer than the §8 benchmark → work the fact into the example-led prose.

ADVISORY video_need: `pandas.datetime_handling` HIGH suits MEDIUM better (two short calls). `pandas.drop_duplicates` MEDIUM could be LOW for a Reference concept. The `annotated_ui` mode on code-only concepts (`loc_iloc_selection`, `missing_data_handling`, `merge_join`) fits poorly → use `data_table_demo` or `live_code`.