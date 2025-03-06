import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
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


def load_model_torch() -> torch.nn.Module:
    model = build_resnet18()
    return model
    # return model.to("cuda")


def build_data_loader_torch(batch_size: int) -> DataLoader:
    transform = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    dataset = MNIST(
        root="./data",
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


def save_checkpoint_and_metrics_torch(
    metrics: dict[str, float], model: torch.nn.Module, local_path: str
) -> None:
    with open(os.path.join(local_path, "metrics.csv"), "a") as f:
        writer = csv.writer(f)
        writer.writerow(metrics.values())

    checkpoint_path = os.path.join(local_path, "model.pt")
    torch.save(model.state_dict(), checkpoint_path)


def main():
    dataset = MNIST(root="./data", train=True, download=True)

    fig, axes = plt.subplots(1, 10, figsize=(20, 2))
    for i in range(10):
        axes[i].imshow(dataset.train_data[i], cmap="gray")
        axes[i].axis("off")
        axes[i].set_title(dataset.train_labels[i].item())
