import torch
from torch import nn

from torch.nn import Conv2d, Flatten, Linear, MaxPool2d, Sequential
from torch.utils.tensorboard import SummaryWriter


class Greg(nn.Module):
    def __init__(self):
        super(Greg, self).__init__()
        self.model1 = nn.Sequential(
            nn.Conv2d(3, 32, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 32, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),  # 这里的 Flatten 默认 start_dim=1，非常正确
            nn.Linear(1024, 64),
            nn.Linear(64, 10),
        )

    def forward(self, x):
        return self.model1(x)


greg = Greg()
print(greg)
writer = SummaryWriter("logs")

input = torch.ones((64, 3, 32, 32))
output = greg(input)

writer.add_graph(greg, input)
writer.close()
