# Q1:
# The second

# Q1:

ggplot(mpg, aes(x = cty, y = hwy)) +
  geom_point()
ggsave("mpg-plot.pdf", device="pdf")
