# Load required libraries
library(plotly)

# Function to compute the l_p norm for given p
lp_norm_surface <- function(p, x, y) {
  return((abs(x)^p + abs(y)^p)^(1/p))
}

lp_norm_surface_14 <- function(x, y) {
  return(lp_norm_surface(1/4, x, y))
}

lp_norm_surface_13 <- function(x, y) {
  return(lp_norm_surface(1/3, x, y))
}

lp_norm_surface_12 <- function(x, y) {
  return(lp_norm_surface(2, x, y))
}

# Generate a grid of points in 2D space
x <- seq(-10, 10, length.out = 100)
y <- seq(-10, 10, length.out = 100)


# Plotting the surface for p = 1/4
p1 <- plot_ly(x = x, y = y, z = outer(x, y, lp_norm_surface_14), type = 'surface') %>%
  layout(title = 'l_{1/4} Norm Surface',
         scene = list(xaxis = list(title = 'x'),
                      yaxis = list(title = 'y'),
                      zaxis = list(title = 'z', range=c(0,200))))

# Plotting the surface for p = 1/3
p2 <- plot_ly(x = x, y = y, z = outer(x, y, lp_norm_surface_13), type = 'surface') %>%
  layout(title = 'l_{1/2} Norm Surface',
         scene = list(xaxis = list(title = 'x'),
                      yaxis = list(title = 'y'),
                      zaxis = list(title = 'z')))

# Plotting the surface for p = 1/2
p3 <- plot_ly(x = x, y = y, z = outer(x, y, lp_norm_surface_12), type = 'surface') %>%
  layout(title = 'l_{1/2} Norm Surface',
         scene = list(xaxis = list(title = 'x'),
                      yaxis = list(title = 'y'),
                      zaxis = list(title = 'z')))

# Display the plots side by side
subplot(p3) %>% layout(title = 'l_p Norm Surfaces for p=1/4, p=1/3 and p=1/2')
