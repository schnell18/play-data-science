library(palmerpenguins)
library(ggthemes)
# Plot penguins bill length vs bill depth:

ggplot(
  data = penguins,
  mapping = aes(x=bill_length_mm, y=bill_depth_mm)
) + 
  geom_point(mapping = aes(shape=sex, color=species)) +
  geom_smooth() +
  labs(
    title="Bill length and bill depth",
    x="Bill Length(mm)",
    y="Bill Depth(mm)",
  ) +
  scale_color_colorblind()
ggsave("penguins.pdf", device="pdf")


# Plot penguins species length vs bill depth:

ggplot(
  data = penguins,
  mapping = aes(x=species, y=bill_depth_mm)
) + 
  geom_violin(mapping = aes(shape=species, color=species)) +
  labs(
    title="Species vs Bill length",
    x="Species",
    y="Bill Depth(mm)",
  ) +
  scale_color_colorblind()



ggplot(
  data = penguins,
  mapping = aes(x=flipper_length_mm, y=body_mass_g)
) + 
  geom_point(mapping = aes(color=bill_depth_mm), na.rm=T) +
  geom_smooth() +
  labs(
    x="Flipper length(mm)",
    y="Body mass(g)",
  )
