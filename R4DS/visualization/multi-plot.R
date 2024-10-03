library(ggplot2)
library(patchwork)

# Sample data
set.seed(123)
data <- data.frame(
  x = 1:10,
  y = sample(1:100, 10),
  category = rep(1:3, each = 10)
)

# Create a single plot for one grid element
create_combined_plot <- function() {
  # Line plot (on top)
  line_plot <- ggplot(data, aes(x, y)) +
    geom_line(color = "blue") +
    theme_minimal() +
    theme(axis.title.x = element_blank())  # Remove x-axis title for a clean look
  
  # Bar plot (on bottom)
  bar_plot <- ggplot(data, aes(x, y)) +
    geom_bar(stat = "identity", fill = "orange") +
    theme_minimal()
  
  # Combine the line and bar plot vertically
  combined_plot <- line_plot / bar_plot + plot_layout(heights = c(1, 3))
  return(combined_plot)
}

# Create a 3x3 grid of combined plots
final_plot <- (create_combined_plot() | create_combined_plot() | create_combined_plot()) /
  (create_combined_plot() | create_combined_plot() | create_combined_plot()) /
  (create_combined_plot() | create_combined_plot() | create_combined_plot())

# Display the plot
final_plot
