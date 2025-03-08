#!/usr/bin/env python3

import torch
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
from ray.tune import RunConfig

from trainloop import train_loop_ray_train

if __name__ == "__main__":
    n_workers = 2 if not torch.cuda.is_available() else torch.cuda.device_count()
    storage_path = "/tmp/ray_train"
    run_config = RunConfig(storage_path=storage_path, name="distributed-mnist-resnet18")
    scaling_config = ScalingConfig(num_workers=1, use_gpu=True)

    trainer = TorchTrainer(
        train_loop_ray_train,
        scaling_config=scaling_config,
        run_config=run_config,
        train_loop_config={"num_epochs": 2, "global_batch_size": 128},
    )

    result = trainer.fit()
