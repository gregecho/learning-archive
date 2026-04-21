"""
在深度学习的卷积神经网络（CNN）中，最大池化（Max Pooling） 紧跟在卷积层之后，它的核心任务是“压缩”和“提纯”。
可以把它理解为一个**“择优录取”**的过程：在一块区域内，只保留信号最强的那个特征。

2. 为什么需要最大池化？（核心价值）

降维与加速：最直观的作用是减小数据量（例如 2×2 池化能减少 75% 的参数），从而降低计算开销，防止过拟合。

特征不变性（Invariance）：这是最牛的地方。只要最强的那个特征信号还在窗口内，哪怕它稍微偏移了几像素，最大池化的输出依然是一样的。这让模型对物体的旋转、平移更有鲁棒性。

提取显著特征：在图像处理中，大的数值通常代表“这里有我们要找的特征”（比如一条边缘）。最大池化确保了最关键的信号能进入下一层。
"""

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

input = torch.tensor(
    [
        [1, 2, 0, 3, 1],
        [0, 1, 2, 3, 1],
        [1, 2, 1, 0, 0],
        [5, 2, 3, 1, 1],
        [2, 1, 0, 1, 1],
    ],
    dtype=torch.float32,
)

input = torch.reshape(input, [-1, 1, 5, 5])
print(input.shape)


class Greg(nn.Module):
    def __init__(self) -> None:
        super(Greg, self).__init__()
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, ceil_mode=True)

    def forward(self, input):
        output = self.maxpool1(input)
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
