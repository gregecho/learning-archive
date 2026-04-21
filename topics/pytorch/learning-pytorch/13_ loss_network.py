import torch
from torch import nn

from torch.nn import Conv2d, Flatten, Linear, MaxPool2d, Sequential
from torch.utils.tensorboard import SummaryWriter
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader

test_data = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    transform=transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    ),
    download=True,
)

test_loader = DataLoader(
    dataset=test_data, batch_size=4, shuffle=True, num_workers=0, drop_last=False
)


class Greg(nn.Module):
    def __init__(self):
        super(Greg, self).__init__()
        self.model1 = nn.Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),  # 这里的 Flatten 默认 start_dim=1，非常正确
            Linear(1024, 64),
            Linear(64, 10),
        )

    def forward(self, x):
        return self.model1(x)


greg = Greg()
print(greg)
writer = SummaryWriter("logs")

loss = torch.nn.CrossEntropyLoss()
for data in test_loader:
    imgs, targets = data
    outputs = greg(imgs)
    result_loss = loss(outputs, targets)
    print(result_loss)
    result_loss.backward()
