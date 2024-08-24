# Introduction

This document is the reading notes of [R for Data Science(2e)][1]. The book's
cover is a near-extinct parrot species named kakapo which is native to New
Zealand. Besides this book, the [Hands-On Programming with R][2] by the rstudio
team is also worth reading. The [ggplot2: Elegant Graphics for Data Analysis
(3e)][4] focus on visualization. The [Tidy Modeling with R][5] elaborates how
to create statistical and machine learning models. The [Big Book of R][3] a
comprehensive catalog of R books, book clubs, interview skills and online
learning materials.


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

We can use morden expression to simply above code snippet as:


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

Tyically we use histogram to display numeric data. For example, we display penguins
body mass as follows:

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
Example:
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


[1]: https://r4ds.hadley.nz/
[2]: https://rstudio-education.github.io/hopr/
[3]: https://www.bigbookofr.com/
[4]: https://ggplot2-book.org/
[5]: https://www.tmwr.org/

