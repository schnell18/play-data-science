# Introduction

This document is the reading notes of [R for Data Science(2e)][1]. The book's
cover is a near-extinct parrot species named kakapo which is native to New
Zealand. Besides this book, the [Hands-On Programming with R][2] by the rstudio
team is also worth reading. The [ggplot2: Elegant Graphics for Data Analysis
(3e)][4] focus on visualization. The [Tidy Modeling with R][5] elaborates how
to create statistical and machine learning models. The [Big Book of R][3] a
comprehensive catalog of R books, book clubs, interview skills and online
learning materials.


## Preparation

### Install R IDE
Download and install [R-Studio][6].

### Install tidyverse and dependencies

    install.packages(
      c(
        "arrow", "babynames", "curl", "duckdb", "gapminder",
        "ggrepel", "ggridges", "ggthemes", "hexbin", "janitor", "Lahman",
        "leaflet", "maps", "nycflights13", "openxlsx", "palmerpenguins",
        "repurrrsive", "tidymodels", "writexl"
      )
    )


## Data science process


                                => Visualize

    Import => Tidy => Transform               => Communicate

                                => Model

The data science process is iterative by nature.
The process starts with importing external data into R as dataframe.
Then followed by tidy and transform, aka data wrangling, to ensure
clean data and useful aggregation and derived data are prepared.
Then visualization and modeling are performed to genenate insight
and knowledge from data. The last step is communicate the knowledge
and insight gained from the science process to stakeholders.

The morden R data science process usually employs the so-called `tidyverse` and
`ggplot` to tidy, transform and visualize data. In the tidyverse, the
conventional dataframe is enhanced to be tipples.


## Visualize

Load the dependencies:

~~~~R
library(tidyverse)
library(palmerpenguins)
library(ggthemes)
~~~~

The `palmerpenguins` is a small dataset on penguins.

With ggplot2, we create a plot using the `ggplot()` function.
The first argument to this function is the dataset.
A plot contains a number of layers.

Plot penguins flipper length vs body mass:

~~~~R
ggplot(
  data = penguins,
  mapping = aes(x=flipper_length_mm, y=body_mass_g)
) + 
  geom_point(mapping = aes(shape=species, color=species)) +
  geom_smooth(method="lm") +
  labs(
    title="Body mass and flipper length",
    subtitle="Dimensions for Adelie, Chinstrap and Gentoo Penguins",
    x="Filpper length(mm)",
    y="Body mass(g)",
  ) +
  scale_color_colorblind()
~~~~

We can use modern expression to simply above code snippet as:

~~~~R
penguins |>
ggplot(
  aes(x=flipper_length_mm, y=body_mass_g)
) + 
  geom_point(mapping = aes(shape=species, color=species)) +
  geom_smooth(method="lm") +
  labs(
    title="Body mass and flipper length",
    subtitle="Dimensions for Adelie, Chinstrap and Gentoo Penguins",
    x="Filpper length(mm)",
    y="Body mass(g)",
  ) +
  scale_color_colorblind()
~~~~

The `|>` is the pipe operator similar to `|` in Linux/Unix shell. It sends the
argument to the left to the first argument of the function to the right.
In this case, the `penguins` data frame is plotted using `ggplot()` function.

### Categorical data

Tyically we use bar to display categorical data. For example, we display penguins
count by species as follows:

~~~~R
ggplot(penguins, aes(x=species)) + 
  geom_bar()
~~~~

Display in descreasing order:

~~~~R
ggplot(penguins, aes(x=fct_infreq(species))) + 
  geom_bar()
~~~~

### Numerical data

Typically we use histogram to display numeric data. For example, we display
penguins body mass as follows:

~~~~R
ggplot(penguins, aes(x=body_mass_g)) + 
  geom_histogram(binwidth=200)
~~~~

To show the distribution, we offen pair the histogram with density plot:

~~~~R
ggplot(penguins, aes(x=body_mass_g)) + 
  geom_density() +
  geom_histogram(binwidth=200)
~~~~

## Visualize relationships

### A numerical and a categorical variable

We use side-by-side box plots to display the relationship between a numerical
and categorical varialb. A box plot show the percentiles to outline the data
distribution. And it is also used to identify potential outliers. Specifically,
it displays a box with height equal the IQR, the top indicating the 75th
percentile, the bottom indicating the 25th percentile. A solid line inside the
box denotes the 50th percentile. The points outside the 1.5 times the IRQ are
outliers. The whisker shows the farest non-outlier data points.

Sample boxplot for penguins body mass:

~~~~R
ggplot(penguins, aes(x = species, y = body_mass_g)) +
  geom_boxplot()
~~~~

An alternative is the density plot:

~~~~R
ggplot(penguins, aes(x = body_mass_g, color=species, fill=species)) +
  geom_density(alpha=0.5)
~~~~

### Two categorical variables

We can use stacked bar plots show the relationship between two categorical
variables.

Example(Y-axis is the count):

~~~~R
ggplot(penguins, aes(x = island, fill=species)) +
  geom_bar()
~~~~

Example(Y-axis is the percentage):

~~~~R
ggplot(penguins, aes(x = island, fill = species)) +
  geom_bar(position = "fill")
~~~~

### Two numerical variables

Scatterplot is commonly used to show the relationship of two numerical
variables.

Example:

~~~~R
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point()
~~~~

To plot more variables using scatter plot, we can use shape and color.

~~~~R
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(aes(color=species, shape=island))
~~~~

The downside of this approach is the plot is usually difficulty to read as lots
of elements are presented. So ggplot offers a better method to present multiple
variables involving categorical variable, the facet.

Example:

~~~~R
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(aes(color=species, shape=species)) +
  facet_wrap()
~~~~

### Save plot

We can use the `ggsave()` function to save the plot on disk for publication.
To save as pdf, specify `device=pdf`.

## Transform data

The dplyr package is main tool to transform data in the tidyverse. However,
this package overwrite some built-in function the base package. To use the
built-in functions, you have to use prefix the function name with package. For
example, to use the `filter()` in the base R, you need type `stats::filter()`
instead.

In tidyverse, the dataframe is called tibble, which is designed for large
dataset in mind. To view a tibble, we can use `glimpse` or `view` in R-Studio.
The glimpse() show column name, type and sample data on one screen.
The data type is abbreviated with common varieties such as:

- int: integer
- dbl: double, real number
- chr: string
- dttm: date-time

The dplyr connects operations on tipple with pipe, represented as `|>`. The
operations are functions that expect a tipple object as its first argument. So
the expression `x |> f(y)` is same as `f(x, y)`, and `x |> f(y) !> g(z)` is
equivalent to `g(f(x, y), z)`. The pipe symbol is similar to `then`.

Here is more complex example to express the data processing pipeline using dplyr.

~~~~R
flights |>
  filter(dest == "IAH") |> 
  group_by(year, month, day) |> 
  summarize(
    arr_delay = mean(arr_delay, na.rm = TRUE)
  )
~~~~

Without the pipe expresion, we have to write deeply nested function calls for
pipeline with a few steps.

### Row-wise operations

#### filter

`filter()` is used to match specific rows according to the values of columns.
The first argument of this function is the tipple. The rest arguments are the
predicates to select rows.

To select flights with late departure more than 120 minutes, we have:

~~~~R
flights |>
  filter(dep_delay > 120)
~~~~

We can express different relationship operators as follows:
- greater than: `>`
- greater than or equal to: `>=`
- less than: `<`
- less than or equal to: `<=`
- equal to: `==`
- not equal: `!=`
- or: `|`
- and: `&`
- multiple equal to: `%in%`

For example, to find flights with late departure more than 120 minutes in May,
we have:

~~~~R
flights |>
  filter(dep_delay > 120 & month == 5)
~~~~

Find flights with late departure more than 120 minutes in May and June,
we have:

~~~~R
flights |>
  filter(dep_delay > 120 & month %in% c(5, 6))
~~~~

#### arrange

`arrange()` order the tipple by selected columns in ascending or descending
order. It is equivalent to SQL's `order by`. By default, this function orders
rows ascendingly. To order in the opposite direction, you use the `desc()` to
wrap the column you wish order in descending order.

List flights with biggest departure delay first:

~~~~R
flights |>
  arrange(desc(dep_delay))
~~~~

#### distinct

`distinct()` selects unique combinations of given columns.

List all unique origin and destination pairs:

~~~~R
flights |>
  distinct(origin, dest)
~~~~

To count the occurrences instead, we can use the `count()` function:

Count flights between origin and destination:

~~~~R
flights |>
  count(origin, dest, sort=T)
~~~~


### Column-wise operations

#### mutate

`mutate()` is used to add calculated fields. The new fields can be inserted a
given location by using `.before` and `.after`. Or to keep related fields only
with `.keep="used"`.

~~~~R

flights |> 
  mutate(
  gain = dep_delay - arr_delay,
  speed = distance / air_time * 60,
  .after = day
  )
~~~~

~~~~R
flights |> 
  mutate(
  gain = dep_delay - arr_delay,
  speed = distance / air_time * 60,
  .keep = "used"
  )
~~~~

#### select

`select()` is used to pick a subset of columns.

select columns by name:

~~~~R
flights |> 
  select(year, month, day)
~~~~

select columns by range(inclusive):

~~~~R
flights |> 
  select(year:day)
~~~~

select columns not in a range(inclusive):

~~~~R
flights |> 
  select(!year:day)
~~~~

select by data type:

~~~~R
flights |> 
  select(where(is.character))
~~~~

select by name prefix:

~~~~R
flights |> 
  select(starts_with("abc"))
~~~~

select by name postfix:

~~~~R
flights |> 
  select(ends_with("abc"))
~~~~

select by substring:

~~~~R
flights |> 
  select(contains("abc"))
~~~~

select by numeric postfix:

~~~~R
flights |> 
  select(num_range("x", 1:3))
~~~~

select and rename:

~~~~R
flights |> 
  select(tail_num = tailnum)
~~~~

#### rename
This function only rename specified column and keep other column intact.

#### relocate
This function move the column to desired position.

### Pipe example
By combining the functions we learnt so far we solve complex problem
such as finding fastest flights to Houston's IAH airport:

~~~~R

flights |> 
  filter(dest == "IAH") |>
  mutate(speed = distance / air_time * 60) |>
  select(year:day, dep_time, carrier, flight, speed) |>
  arrange(desc(speed))
~~~~

The native pipe symbol is `|>`, the alternative is `%>%`. To insert pipe symbol
in R-Studio, press Ctrl/Cmd + Shift + M.

## Groups

We can aggregate data using groups. We create groups using the `group_by()`
function. Then we apply aggregation functions in the `summarize()`. In recent
version of dplyr, the `.by` parameter can be used in place of `group_by()`.

~~~~R
flights |> 
  group_by(month) |>
  summarize(avg_delay = mean(dep_delay))
~~~~

The `summarize()` function is sensitive to missing data. You need either clean
the missing data up front or ignore them in the aggregation function.

~~~~R
flights |> 
  group_by(month) |>
  summarize(
    avg_delay = mean(dep_delay, na.rm = TRUE),
    n = n()
  )
~~~~

### slice_ functions

The `slice_` functions are convenient window functions:
- `slice_head(n = 1)`: takes the first row from each group
- `slice_tail(n = 1)`: takes the last row from each group
- `slice_sample(n = 1)`: takes one random row from each group
- `slice_max(x, n = 1)`: takes one row with largest x from each group
- `slice_min(x, n = 1)`: takes one row with smallest x from each group

You can specify percent of rows to take with the `prop=0.n` parameter instead
of `n=xx`. The `slice_max()` and `slice_min()` functions keeps ties by default.
If you don't want ties, you can pass `with_ties = FALSE` in these functions.

# Tidy data

The rules for a tidy dataset include:
- Each variable is a column and each column is a variable
- Each observation is a row and each row is an observation
- Each value is a cell, each cell is a single value

Tidy dataset is easier to work with in the tidyverse. Most built-in functions
in R works well with vector variable.

## Pivot data

### Make table longer

The `pivot_longer()` function turns columns into rows. It selects a list of
columns by prefix/surfix, a new column to store the selected column names
is created using the name specified by parameter `names_to`. The values
are stored in the other column specified by parameter `values_to`.

Here is an example to convert a extremely wide table `billboard` into long
table.

~~~~R
billboard_longer <- billboard |>
  pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    values_to = "rank",
    values_drop_na = TRUE
  ) |> 
  mutate(
    week = parse_number(week)
  )
~~~~

~~~~R
billboard_longer |> 
  ggplot(aes(x = week, y = rank, group = track)) + 
  geom_line(alpha = 0.25) + 
  scale_y_reverse()
~~~~

The `pivot_longer()` function is very powerful to deal with complex pivoting
problem where the number of columns is large and the column name bears multiple
information. For the `who2` dataset contains 56 columns in form like 
`<diag method>_<gender>_<age group>`. We split these columns into three parts
as follows:

~~~~R
who2 |> 
  pivot_longer(
    cols = !(country:year),
    names_to = c("diagnosis", "gender", "age"),
    names_sep = "_",
    values_to = "count",
  )
~~~~

One more complex example, which pivot the paired columns indicated by numeric
suffix.

~~~~R
household |> 
  pivot_longer(
    cols = !family, 
    names_to = c(".value", "child"), 
    names_sep = "_", 
    values_drop_na = TRUE
  )
~~~~

The position of new column to store the captured identifier is the same as it
appears in the column name. In the previous example the identifier `child` is
the second position, so we set the new field `child` as the second element
in the list passed to `names_to` parameter of `pivot_longer()` function.

~~~~R
household1 <- household |> 
  rename(
    child1_dob = dob_child1,
    child2_dob = dob_child2,
    child1_name = name_child1,
    child2_name = name_child2
  )
household1 |> 
  pivot_longer(
    cols = !family, 
    names_to = c("child", ".value"), 
    names_sep = "_", 
    values_drop_na = TRUE
  )
~~~~


### Widen table
The `pivot_wider()` function can turn the row into columns. It is useful to
show column with low cardinality in column format.
To use this function, we need specify:
- id_cols: the list of identifying fields
- names_from: the column contains values as new columns
- values_from: the column contains values as values

~~~~R
cms_patient_experience |> 
  pivot_wider(
    id_cols = starts_with("org"),
    names_from = measure_cd,
    values_from = prf_rate
  )
~~~~

# Data file I/O
## Import data

R supports numerous data formats. To read text file such as CSV, we can use
the `readr` package, which offers the `read_csv()` function.
The `read_csv()` function can read local file and remote file using HTTP.

~~~~R
students <- read_csv("data/students.csv", na = c("N/A", ""))
~~~~

To normalize field naming, we can apply the `janitor::clean_names()` to the
dataframe. The default behavior of the function is to apply snake case to the
names and remove spaces in the name.

~~~~R
students <- read_csv("data/students.csv", na = c("N/A", ""))
students <- students |>
  janitor::clean_names() |> 
  mutate(
    meal_plan = factor(meal_plan),
    age = parse_number(if_else(age == "five", "5", age))
  )
~~~~

Read multiple csv files:


~~~~R
sales_files <- c(
  "https://pos.it/r4ds-01-sales",
  "https://pos.it/r4ds-02-sales",
  "https://pos.it/r4ds-03-sales"
)
sales <- read_csv(sales_files, id = "file")
~~~~

Summary of importing a csv file:
- normalize NA values by specifying alternative NA representations
- use factor data type to represent categorical data
- extract number from text
- convert column name to snake case

## Export data
We can export data by:
- export textual: format write_csv()/write_tsv() of readr package
- export binary RDS: write_rds() of readr package
- export binary parquet: write_parquet() of arrow package

The binary RDS is a R native format, it can restore the data type precisely. The
binary parquet is a fast cross-language binary data format, it requires the
`arrow` package.

~~~~R
library(arrow)
write_parquet(students, "students.parquet")
read_parquet("students.parquet")
~~~~

## Enter small test data

The `tribble()` function(transposed tibble) helps us to enter tabular data in an
intuitive way. Column head is prefixed with tilde, columns are separated by
comma.

~~~~R
tribble(
  ~X,  ~Y,  ~Z, 
  1, "H", 0.08,
  2, "M", 0.89,
  3, "G", 0.71,
  4, "B", 0.81
)
~~~~

# Trouble shooting

## create reproducible example
We can use the the reprex::reprex package to format the R code to reproduce
a problem. To include data, we can use the `dput()` function to serialize
a dataframe as code to reconstruct it.

## continuous learning
Read [tidyverse blog][7] and [R Weekly][8].

[1]: https://r4ds.hadley.nz/
[2]: https://rstudio-education.github.io/hopr/
[3]: https://www.bigbookofr.com/
[4]: https://ggplot2-book.org/
[5]: https://www.tmwr.org/
[6]: https://posit.co/download/rstudio-desktop/
[7]: https://www.tidyverse.org/blog/
[8]: https://rweekly.org/
