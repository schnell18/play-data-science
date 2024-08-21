# Introduction

Notes on basic R programming tutorial based on [R Programming Tutorial -
Learn the Basics of Statistical Computing][1].

## useful R packages

Some useful third-party R packages:
- dplyr
- tidyr
- stringr
- lubridate
- httr
- ggvis
- ggplot2
- shiny
- rio
- rmarkdown
- pacman

## date types

R supports a few built-in data types such as:
- vector: a one-dimension array with same data type
- scalar: a special case of one element vector
- matrix: two dimension same data type
- array: any dimension same data type
- data frame: consists of vectors of various data types
- list: ordered collection of elements, can be nested like Russian nesting dolls

primitive types:
- double(default)
- integer
- character(string and char)
- logical(boolean)

constructors:
- concat with comma separated literals: c(1, 2, 3), c(T, T, F), c("a", "b", "c")
- concat with sequence expression: c(1:24)
- combine: cbind(vNumeric, vCharacter, vLogical), coerce to most general data type
- as.data.frame: generate data frame
- cbind.data.frame: bind and convert to dataframe
- list: generate list
- factor: generate factors
- colon operator: 0:10
- sequence: seq

Misc:
- assignment operator: '<-' is preferred(shortcut option+dash in RStudio), '='
  and '->' also works
- place assignment expression inside parenthesis to evaluate the varialbe's
  value and display on console)

Define factors:

    x3 <- c(1:3)
    df3 <- cbind.data.frame(x3, y)
    (df3$x3 <- factor(df3$x3, levels = c(1, 2, 3), labels= c("MacOS", "Windows", "Linux")))


coerce rules:
- automatic coercion: convert to "least restrictive" data type
- manual coercion: as.numeric(), as.integer(), as.data.frame()

### importing data
R supports common data formats like csv, excel, txt, json.
rio is the convenient third-party library to import data.

[1]: https://www.youtube.com/watch?v=_V8eKsto3Ug

