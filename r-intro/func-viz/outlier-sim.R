# Load the necessary library
library(stats)

# Define parameters for the Laplace distribution
set.seed(123) # Setting seed for reproducibility
n <- 128
mu <- 0       # Mean (location parameter)
b <- 1        # Scale parameter

# Function to generate Laplacian distributed data
rlaplace <- function(n, location = 0, scale = 1) {
  u <- runif(n, min = -0.5, max = 0.5)
  location - scale * sign(u) * log(1 - 2 * abs(u))
}

# Generate 128 x 128 matrix with Laplacian distribution
laplace_matrix <- matrix(rlaplace(n * n, location = mu, scale = b), nrow = n, ncol = n)

# Print out the first few values to check
print(head(laplace_matrix))

