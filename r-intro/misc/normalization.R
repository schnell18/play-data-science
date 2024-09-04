library(ggplot2)
library(tidyverse)

# Min-Max Normalization function
min_max_normalize <- function(x) {
  return((x - min(x)) / (max(x) - min(x)))
}

# Z-Score Normalization function
z_score_normalize <- function(x) {
  return((x - mean(x)) / sd(x))
}

features <- mtcars |>
  select(mpg_original = mpg, disp_original = disp) |>
  mutate(
    mpg_zscore = z_score_normalize(mpg_original),
    disp_zscore = z_score_normalize(disp_original),
    mpg_minmax = min_max_normalize(mpg_original),
    disp_minmax = min_max_normalize(disp_original),
  ) |>
  # select(mpg_zscore, disp_zscore, mpg_minmax, disp_minmax) |>
  pivot_longer(
    cols = where(is.numeric),
    names_to = c(".value", "metric"),
    names_sep = "_",
  ) |>
  mutate(
    metric = factor(
      metric,
      levels=c("original", "zscore", "minmax"),
      labels=c("Original", "Z-Score", "Min-Max"),
    )
  )


# Create the ggplot
ggplot(features, aes(x = mpg, y = disp, color = metric)) +
  geom_point() +
  geom_smooth() +
  facet_wrap(~ metric, scales = "free") +
  labs(title = "MPG vs Displacement in original measurement and normalized forms of Min-Max and Z-Score",
       x = "MPG",
       y = "Displacement",
       color = "metric")
