from typing import Any

from torch import nn
import torch


class Greg(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    def forward(self, input):
        output = input + 1
        return output


greg = Greg()
result = greg(torch.tensor(1.0))
print(result)
