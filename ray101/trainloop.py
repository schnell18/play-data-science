import csv
import os
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import ray
import torch
import torchmetrics
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.models import resnet18
from torchvision.transforms import Compose, Normalize, ToTensor


def train_loop_torch(
    num_epochs: int = 2,
    batch_size: int = 128,
    local_path: str = "./checkpoints",
):
    loss_func = CrossEntropyLoss()
    model = load_model_torch()
    optimizer = Adam(model.parameters(), lr=1e-5)

    # acc = torchmetrics.Accuracy(task="multiclass", num_classes=10).to("cuda")
    acc = torchmetrics.Accuracy(task="multiclass", num_classes=10)

    data_loader = build_data_loader_torch(batch_size=batch_size)

    for epoch in range(num_epochs):
        for images, labels in data_loader:
            # images, labels = images.to("cuda"), labels.to("cuda")
            outputs = model(images)
            loss = loss_func(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            acc(outputs, labels)
        metrics = report_metrics_torch(
            loss=loss,
            accuracy=acc.compute(),
            epoch=epoch,
        )
        acc.reset()
        Path(local_path).mkdir(parents=True, exist_ok=True)
        save_checkpoint_and_metrics_torch(
            metrics=metrics, model=model, local_path=local_path
        )


def train_loop_ray_train(config: dict):  # pass in hyperparameters in config
    criterion = CrossEntropyLoss()
    # Use Ray Train to wrap the model with DistributedDataParallel
    model = load_model_ray_train()
    optimizer = Adam(model.parameters(), lr=1e-5)

    # Calculate the batch size for each worker
    global_batch_size = config["global_batch_size"]
    batch_size = global_batch_size // ray.train.get_context().get_world_size()
    # Use Ray Train to wrap the data loader as a DistributedSampler
    data_loader = build_data_loader_ray_train(batch_size=batch_size)

    acc = torchmetrics.Accuracy(task="multiclass", num_classes=10).to(model.device)
    # Add AUROC metric
    auroc = torchmetrics.AUROC(task="multiclass", num_classes=10).to(model.device)

    for epoch in range(config["num_epochs"]):
        # Ensure data is on the correct device
        data_loader.sampler.set_epoch(epoch)

        for (
            images,
            labels,
        ) in data_loader:  # images, labels are now sharded across the workers
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()  # gradients are now accumulated across the workers
            optimizer.step()
            acc(outputs, labels)
            auroc(outputs, labels)

        # Use Ray Train to report metrics
        metrics = print_metrics_ray_train(loss, acc.compute(), auroc.compute())

        # Use Ray Train to save checkpoint and metrics
        save_checkpoint_and_metrics_ray_train(model, metrics)
        acc.reset()


def build_resnet18():
    model = resnet18(num_classes=10)
    model.conv1 = torch.nn.Conv2d(
        in_channels=1,
        out_channels=64,
        kernel_size=(7, 7),
        stride=(2, 2),
        padding=(3, 3),
        bias=False,
    )
    return model


def load_model_ray_train() -> torch.nn.Module:
    model = build_resnet18()
    return ray.train.torch.prepare_model(model)


def load_model_torch() -> torch.nn.Module:
    model = build_resnet18()
    return model
    # return model.to("cuda")


def build_data_loader_torch(batch_size: int) -> DataLoader:
    transform = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    dataset = MNIST(
        root="/tmp/ray_data",
        train=True,
        download=True,
        transform=transform,
    )
    train_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        drop_last=True,
    )
    return train_loader


def build_data_loader_ray_train(batch_size: int) -> DataLoader:
    transform = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    dataset = MNIST(
        root="/tmp/ray_data",
        train=True,
        download=True,
        transform=transform,
    )
    train_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        drop_last=True,
    )
    return ray.train.torch.prepare_data_loader(train_loader)


def report_metrics_torch(
    loss: torch.Tensor, accuracy: torch.Tensor, epoch: int
) -> None:
    metrics = {
        "loss": loss.item(),
        "epoch": epoch,
        "accuracy": accuracy.item(),
    }
    print(metrics)
    return metrics


def print_metrics_ray_train(
    loss: torch.Tensor, accuracy: torch.Tensor, auroc: torch.Tensor
) -> None:
    metrics = {
        "loss": loss.item(),
        "accuracy": accuracy.item(),
        "auroc": auroc.item(),
    }
    if ray.train.get_context().get_world_rank() == 0:
        print(metrics)
    return metrics


def report_metrics_ray_train(
    loss: torch.Tensor, accuracy: torch.Tensor, epoch: int
) -> None:
    metrics = {
        "loss": loss.item(),
        "epoch": epoch,
        "accuracy": accuracy.item(),
    }
    if ray.train.get_context().get_world_rank() == 0:
        print(metrics)
    return metrics


def save_checkpoint_and_metrics_torch(
    metrics: dict[str, float], model: torch.nn.Module, local_path: str
) -> None:
    with open(os.path.join(local_path, "metrics.csv"), "a") as f:
        writer = csv.writer(f)
        writer.writerow(metrics.values())

    checkpoint_path = os.path.join(local_path, "model.pt")
    torch.save(model.state_dict(), checkpoint_path)


def save_checkpoint_and_metrics_ray_train(
    model: torch.nn.Module,
    metrics: dict[str, float],
) -> None:
    with tempfile.TemporaryDirectory() as tcpd:
        checkpoint = None
        if ray.train.get_context().get_world_rank() == 0:
            checkpoint_path = os.path.join(tcpd, "model.pt")
            torch.save(model.module.state_dict(), checkpoint_path)
            checkpoint = ray.train.Checkpoint.from_directory(tcpd)

        ray.train.report(metrics, checkpoint=checkpoint)


def main():
    dataset = MNIST(root="./data", train=True, download=True)

    fig, axes = plt.subplots(1, 10, figsize=(20, 2))
    for i in range(10):
        axes[i].imshow(dataset.train_data[i], cmap="gray")
        axes[i].axis("off")
        axes[i].set_title(dataset.train_labels[i].item())
