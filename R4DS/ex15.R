# Q1


# manufacturer <chr> "audi", "audi", "audi", "audi", "audi", "audi", "audi", "audi", "audi", "audi", "audi", "audi"…
# model        <chr> "a4", "a4", "a4", "a4", "a4", "a4", "a4", "a4 quattro", "a4 quattro", "a4 quattro", "a4 quattr…
# displ        <dbl> 1.8, 1.8, 2.0, 2.0, 2.8, 2.8, 3.1, 1.8, 1.8, 2.0, 2.0, 2.8, 2.8, 3.1, 3.1, 2.8, 3.1, 4.2, 5.3,…
# year         <int> 1999, 1999, 2008, 2008, 1999, 1999, 2008, 1999, 1999, 2008, 2008, 1999, 1999, 2008, 2008, 1999…
# cyl          <int> 4, 4, 4, 4, 6, 6, 6, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8…
# trans        <chr> "auto(l5)", "manual(m5)", "manual(m6)", "auto(av)", "auto(l5)", "manual(m5)", "auto(av)", "man…
# drv          <chr> "f", "f", "f", "f", "f", "f", "f", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "r",…
# cty          <int> 18, 21, 20, 21, 16, 18, 18, 18, 16, 20, 19, 15, 17, 17, 15, 15, 17, 16, 14, 11, 14, 13, 12, 16…
# hwy          <int> 29, 29, 31, 30, 26, 26, 27, 26, 25, 28, 27, 25, 25, 25, 25, 24, 25, 23, 20, 15, 20, 17, 17, 26…
# fl           <chr> "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "p", "r",…
# class        <chr> "compact", "compact", "compact", "compact", "compact", "compact", "compact", "compact", "compa…

# categorical: manufacturer, model, trans, drv, fl, class

# Q2
ggplot(mpg, aes(x = hwy, y = displ)) +
  geom_point(aes(color=cty))

ggplot(mpg, aes(x = hwy, y = displ)) +
  geom_point(aes(size=cty))

ggplot(mpg, aes(x = hwy, y = displ)) +
  geom_point(aes(color=cyl, size=cty))

ggplot(mpg, aes(x = hwy, y = displ)) +
  geom_point(aes(shape=trans, color=cyl, size=cty))

# Q3
ggplot(mpg, aes(x = hwy, y = displ, linewidth=cyl)) +
  geom_point(aes(color=manufacturer, size=cty))

# Q5
ggplot(penguins, aes(x = bill_depth_mm, y = bill_length_mm)) +
  geom_point(aes(color=species))

ggplot(penguins, aes(x = bill_depth_mm, y = bill_length_mm)) +
  geom_point() +
  facet_wrap(~species)

# Q6
ggplot(penguins, aes(x = bill_length_mm, y = bill_depth_mm, color = species)) +
  geom_point() +
  labs(color = "Species")

# Q7
# 1: percentage of species on each island
# 2: the percentage of penguins on each island for a given species
