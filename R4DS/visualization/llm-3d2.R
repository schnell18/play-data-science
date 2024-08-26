# Load required libraries
library(plotly)
library(reshape2)

# Example data (replace this with your actual data)
set.seed(123)
data_matrix <- matrix(runif(256), nrow = 16, ncol = 16)

# Convert data to long format for easier plotting
data_long <- melt(data_matrix)
colnames(data_long) <- c("Channel", "Token", "Activation")

# 3D Surface Plot using Plotly
plot_ly(data_long, x = ~Channel, y = ~Token, z = ~Activation, type = 'surface') %>%
  layout(scene = list(
    xaxis = list(title = 'Channel'),
    yaxis = list(title = 'Token'),
    zaxis = list(title = 'Activation')
  ))
