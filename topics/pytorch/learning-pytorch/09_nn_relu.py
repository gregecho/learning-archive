import torch
from torch import nn
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

test_data = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    transform=torchvision.transforms.ToTensor(),
    download=True,
)

test_loader = DataLoader(
    dataset=test_data, batch_size=64, shuffle=True, num_workers=0, drop_last=False
)

input = torch.tensor([[1, -0.5], [-1, 3]])

output = torch.reshape(input, [-1, 1, 2, 2])


class Greg(nn.Module):
    def __init__(self) -> None:
        super(Greg, self).__init__()
        self.relu1 = nn.ReLU()
        self.sigmoid1 = nn.Sigmoid()

    def forward(self, input):
        output = self.sigmoid1(input)
        return output


greg = Greg()

writer = SummaryWriter("logs")
step = 0
for data in test_loader:
    imgs, targets = data
    writer.add_images("input", imgs, step)
    output = greg(imgs)
    writer.add_images("output", output, step)
    step += 1

writer.close()
