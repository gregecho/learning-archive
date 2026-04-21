import torch
from torch import nn
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms

test_data = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    transform=transforms.Compose(
        [
            transforms.Resize((256, 256)),  # 确保 resize 到你设定的 256
            transforms.ToTensor(),
        ]
    ),
    download=True,
)

test_loader = DataLoader(
    dataset=test_data, batch_size=64, shuffle=True, num_workers=0, drop_last=False
)


class Greg(nn.Module):
    def __init__(self) -> None:
        super(Greg, self).__init__()
        # CIFAR10图片是 32x32x3 = 3072
        self.linear1 = nn.Linear(3072, 10)

    def forward(self, input):
        # 重点：从第1维开始展平，保留第0维(Batch)
        # 形状变化：[64, 3, 32, 32] -> [64, 3072]
        output = torch.flatten(input, start_dim=1)
        return output


greg = Greg()
for data in test_loader:
    imgs, targets = data
    # print(imgs.shape)
    output = greg(imgs)
    print(f"输入形状: {imgs.shape}, 输出形状: {output.shape}")
