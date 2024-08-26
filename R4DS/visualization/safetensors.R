library(safetensors)
library(jsonlite)
   
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

matrix_name = "model.layers.1.mlp.down_proj.weight"
base_dir <- "~/.cache/huggingface/hub/models--meta-llama--Llama-2-7b-hf/snapshots/01c7f73d771dfac7d292323805ebc428287df4f9/"
base_dir <- path.expand(base_dir)
     
weight <- get_tensor(matrix_name, base_dir)
weight
