library(tidyverse)

ggplot(diamonds, aes(x = carat, y = price)) +
  geom_hex()
ggsave("figs/diamonds.png")
write_csv(diamonds, "data/diamonds.csv")