library(plotly)
library(safetensors)
library(jsonlite)
   
create_3d_plot <- function(x, y, z, title, zlim) {
  plot_ly(
    x = x, y = y, z = z,
    type = "surface", alpha = 0.6,
    colorscale = 'coloraxis'
    # colorscale = list(c(-1, 0, 1), c("blue", "white", "green"))
  ) |> 
    layout(scene = list(
      xaxis = list(title = "Row"),
      yaxis = list(title = "Column"),
      zaxis = list(title = "Weight")
      #zaxis = list(title = "", range = zlim)
    ),
    title = title)
}

get_tensor <- function(matrix_name, base_dir, index_json='model.safetensors.index.json') {
  index_file <- file.path(base_dir, index_json)
  model_index <- fromJSON(index_file)
  
  if (exists(matrix_name, model_index$weight_map)) {
    st_file = model_index$weight_map[[matrix_name]]
    st_file_fp <- file.path(base_dir, st_file)
    tensors <- safe_load_file(st_file_fp)
    return(tensors[[matrix_name]])
  }
}

i <- 2
j <- 2
b <- 2048
rs <- (i - 1) * b
re <- i * b
cs <- (j - 1) * b
ce <- j * b
matrix_name <- "model.layers.31.self_attn.o_proj.weight"
base_dir <- "~/.cache/huggingface/hub/models--meta-llama--Llama-2-7b-hf/snapshots/01c7f73d771dfac7d292323805ebc428287df4f9/"
base_dir <- path.expand(base_dir)
weight <- get_tensor(matrix_name, base_dir)
z <- as.matrix(weight[rs:re,cs:ce])
x <- rs:re
y <- cs:ce

p1 <- create_3d_plot(x, y, z, "block_0.self_attn.q_proj", c(0, 3))
# p2 <- create_3d_plot(x, y, z, "block_0.self_attn.o_proj", c(0, 0.3))
# p3 <- create_3d_plot(x, y, z, "block_0.mlp.gate_proj", c(0, 1))
# p4 <- create_3d_plot(x, y, z, "block_0.mlp.down_proj", c(0, 0.7))

# Combine plots in a 2x2 grid
subplot(p1, titleX = TRUE, titleY = TRUE) |> 
  layout(title = "Llama-3.1-8B Weight Visualization")
