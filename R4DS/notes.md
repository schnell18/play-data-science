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
~~~~{R}
library(tidyverse)
library(palmerpenguins)
library(ggthemes)
~~~~

The `palmerpenguins` is a small dataset on penguins.

With ggplot2, we create a plot using the `ggplot()` function.
The first argument to this function is the dataset.
A plot contains a number of layers.

Plot penguins flipper length vs body mass:
~~~~{R}
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


~~~~{R}
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

~~~~{R}
ggplot(penguins, aes(x=species)) + 
  geom_bar()
~~~~

Display in descreasing order:
~~~~{R}
ggplot(penguins, aes(x=fct_infreq(species))) + 
  geom_bar()
~~~~

### Numerical data

Tyically we use histogram to display numeric data. For example, we display penguins
body mass as follows:

~~~~{R}
ggplot(penguins, aes(x=body_mass_g)) + 
  geom_histogram(binwidth=200)
~~~~
To show the distribution, we offen pair the histogram with density plot:
~~~~{R}
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
~~~~{R}
ggplot(penguins, aes(x = species, y = body_mass_g)) +
  geom_boxplot()
~~~~

An alternative is the density plot:
~~~~{R}
ggplot(penguins, aes(x = body_mass_g, color=species, fill=species)) +
  geom_density(alpha=0.5)
~~~~

### Two categorical variables

We can use stacked bar plots show the relationship between two categorical
variables.

Example(Y-axis is the count):
~~~~{R}
ggplot(penguins, aes(x = island, fill=species)) +
  geom_bar()
~~~~

Example(Y-axis is the percentage):
~~~~{R}
ggplot(penguins, aes(x = island, fill = species)) +
  geom_bar(position = "fill")
~~~~

### Two numerical variables

Scatterplot is commonly used to show the relationship of two numerical
variables.

Example:
~~~~{R}
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point()
~~~~

To plot more variables using scatter plot, we can use shape and color.
Example:
~~~~{R}
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(aes(color=species, shape=island))
~~~~

The downside of this approach is the plot is usually difficulty to read as lots
of elements are presented. So ggplot offers a better method to present multiple
variables involving categorical variable, the facet.

Example:
~~~~{R}
ggplot(penguins, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(aes(color=species, shape=species)) +
  facet_wrap()
~~~~

## Save plot

We can use the `ggsave()` function to save the plot on disk for publication.




[1]: https://r4ds.hadley.nz/
[2]: https://rstudio-education.github.io/hopr/
[3]: https://www.bigbookofr.com/
[4]: https://ggplot2-book.org/
[5]: https://www.tmwr.org/

