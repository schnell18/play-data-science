library(plotly)
library(safetensors)
library(jsonlite)
   
create_3d_plot2 <- function(i, j, weight, scen, title, block_size=1024) {
  rs <- (i - 1) * block_size
  re <- i * block_size
  cs <- (j - 1) * block_size
  ce <- j * block_size
  z <- weight[rs:re,cs:ce]
  x <- rs:re
  y <- cs:ce
  
  plot_ly(
    x = x, y = y, z = z,
    type = "surface", alpha = 0.6,
    colorscale = 'coloraxis',
    scene = scen
  )
  # colorscale = list(c(-1, 0, 1), c("blue", "white", "green"))
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


get_tensor2 <- function(matrix_name, base_dir, st_file) {
  st_file_fp <- file.path(base_dir, st_file)
  tensors <- safe_load_file(st_file_fp)
  return(tensors[[matrix_name]])
}

matrix <- "31.self_attn.o_proj"

orig_matrix <- paste0("model.layers.", matrix, ".weight")
quant_matrix <- paste0("model.layers.", matrix, ".qweight")
base_dir <- "~/work/hqq/examples/llama2_benchmark/snapshots/cmp"
base_dir <- path.expand(base_dir)
st_file <- "Llama-2-7b-hf-cmp.safetensors"
wo <- get_tensor2(orig_matrix, base_dir, st_file)
wo <- as.matrix(wo)
wq <- get_tensor2(quant_matrix, base_dir, st_file)
wq <- as.matrix(wq)

p1 <- create_3d_plot2(1, 1, wo, "scene1", matrix, block_size = 2048)
p2 <- create_3d_plot2(1, 1, wq, "scene1", matrix, block_size = 2048)

fig1 <- subplot(p1) |> 
  layout(
    title = "Llama-2-7B Original Weight",
    scene1 = list(
      domain = list(row = 1, column = 1),
      zaxis = list(title = "Weight", range = c(-1.7, 1.7)),
      camera = list(eye = list(x = 1.5, y = 1.5, z = 0.3))
    )
  )
fig2 <- subplot(p2) |> 
  layout(
    title = "Llama-2-7B Quantized Weight",
    scene1 = list(
      domain = list(row = 1, column = 1),
      zaxis = list(title = "Weight", range = c(-1.7, 1.7)),
      camera = list(eye = list(x = 1.5, y = 1.5, z = 0.3))
    )
  )
save_image(fig1, "llama2-7B-orig.pdf")
save_image(fig2, "llama2-7B-quant.pdf")
