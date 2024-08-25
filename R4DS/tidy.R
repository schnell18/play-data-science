library(tidyverse)

table1 |>
  mutate(rate = cases / population * 10000)

table1 |>
  group_by(year) |>
  summarise(total_cases = sum(cases))

ggplot(table1, aes(x = year, y = cases)) +
  geom_line(aes(group = country), color = "grey50") +
  geom_point(aes(color = country, shape = country)) +
  scale_x_continuous(breaks = c(1999, 2000))
  