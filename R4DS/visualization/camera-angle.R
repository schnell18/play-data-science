library(plotly)

# Sample data
x <- c(1, 2, 3, 4)
y <- c(5, 6, 7, 8)
z <- outer(x, y)

# Create 3D scatter plot
plot <- plot_ly(x = ~x, y = ~y, z = ~z, type = "scatter3d", mode = "markers")

# Adjust the camera angle
plot <- plot %>% layout(
  scene = list(
    camera = list(
      eye = list(x = 1.5, y = 1.5, z = 1.0) # Adjust these values to set the viewing angle
    )
  )
)

# Display the plot
plot
