# Load required libraries
library(tidyverse)
library(ggplot2)

# Define the GELU function
gelu <- function(x) {
  x * pnorm(x)
}

relu <- function(x) {
  sapply(x, function(e) {
    max(e, 0)
  })
}

silu <- function(x) {
  x / (1 + exp(-x))
}

leaky_relu <- function(x) {
  sapply(x, function(e) {
    if (e <= 0) 0.01 * e else e
  })
}


# Create a data frame with x values and corresponding GELU values
data <- data.frame(x = seq(-10, 10, length.out = 1000)) |>
  mutate(
    ReLU = relu(x),
    LeakyReLU = leaky_relu(x),
    GeLU = gelu(x),
    SiLU = silu(x),
  ) |>
  pivot_longer(
    cols = !c("x"),
    names_to = "func",
    values_to = "y",
  ) |>
  mutate(
    func = factor(func, levels = c("ReLU", "LeakyReLU", "GeLU", "SiLU"))
  )

# Create the plot
ggplot(data, aes(x = x, y = y)) +
  geom_line(color = "blue", linewidth = 1) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray") +
  facet_wrap(~func) +
  labs(
    title = "Common Neural Network Activation Functions",
    x = "x",
    y = "y"
  ) +
  coord_cartesian(xlim = c(-10, 10), ylim = c(-8, 8))
