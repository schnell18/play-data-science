library(tidyverse)
library(ggthemes)
library(readr)

# wdist <- read_csv("~/study/aut-study/master-thesis/kube-sft/data/wdist-Meta-Llama-3.1-405B-Instruct.csv")
wdist <- read_csv("~/study/aut-study/master-thesis/kube-sft/data/wdist-Llama-2-7b-hf.csv")
percentiles <- c("0", "99", "99.9", "99.99", "100")
all_cols <- c("module", "layer", percentiles) 
wdist <- wdist |>
  mutate(
    `0` = percentile_0,
    `99` = percentile_99 - percentile_0,
    `99.9` = percentile_999 - percentile_99,
    `99.99` = percentile_9999 - percentile_999,
    `100` = percentile_100 - percentile_9999,
  ) |>
  select(all_of(all_cols)) |>
  pivot_longer(
    cols = percentiles,
    names_to = "nth_percentile",
    names_transform = list(nth_percentile = as.numeric),
    values_to = "abs_val"
  ) |> 
  mutate(
    nth_percentile = factor(nth_percentile, levels = rev(percentiles))
  )

ggplot(wdist, aes(x = layer, y = abs_val, fill = nth_percentile)) +
  geom_bar(stat = "identity", color = "gray50") +
  facet_wrap(~module) +
  scale_color_tableau()

wdist |> 
  filter(nth_percentile == 0 & abs_val > 0.0001)
