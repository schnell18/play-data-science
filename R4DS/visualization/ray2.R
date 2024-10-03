library(rayshader)
library(ggplot2)
library(tidyverse)

gg <- ggplot(diamonds, aes(x, depth)) +
  stat_density_2d(aes(fill = stat(nlevel)),
    geom = "polygon",
    n = 100, bins = 10, contour = TRUE
  ) +
  facet_wrap(clarity ~ .) +
  scale_fill_viridis_c(option = "A")

plot_gg(gg, width = 10, height = 8, raytrace = TRUE, preview = TRUE)
plot_gg(gg,
  width = 10, height = 8, multicore = TRUE, scale = 250,
  zoom = 0.7, theta = 10, phi = 30, windowsize = c(800, 800)
)
Sys.sleep(0.2)
render_snapshot(clear = TRUE)
render_highquality(
  lightdirection = c(-45, 45), lightaltitude = 30, clamp_value = 10,
  samples = 256, camera_lookat = c(0, -50, 0),
  ground_material = diffuse(
    color = "grey50", checkercolor = "grey20", checkerperiod = 100
  ),
  clear = TRUE
)
