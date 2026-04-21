"""
卷积就是一个“滑动窗口”在图像上移动，提取局部特征的过程。
https://github.com/vdumoulin/conv_arithmetic

Kernel Size,卷积核大小,决定“视野”多大（常用 3×3 或 5×5）。
Stride,步长,决定窗口滑动的速度。步长越大，输出图片越小。
Padding,填充,在图片边缘补零。防止图片边缘信息丢失，保持尺寸一致。
Channel,通道,输入（如 RGB 3通道）到输出（提取特征后的多通道）的映射。

卷积到底在干什么？

卷积的本质是 “特征提取器”：
浅层卷积：提取边缘、线条、颜色等基础纹理。
中层卷积：组合边缘，识别圆圈、方块、形状。
深层卷积：识别复杂的语义信息，如“人脸”、“猫耳朵”。
"""

import torch
import torch.nn.functional as F

input = torch.tensor(
    [
        [1, 2, 0, 3, 1],
        [0, 1, 2, 3, 1],
        [1, 2, 1, 0, 0],
        [5, 2, 3, 1, 1],
        [2, 1, 0, 1, 1],
    ]
)

kernel = torch.tensor([[1, 2, 1], [0, 1, 0], [2, 1, 0]])

input = torch.reshape(input, (1, 1, 5, 5))
kernel = torch.reshape(kernel, (1, 1, 3, 3))

print(input.shape)
print(kernel.shape)

output = F.conv2d(input, kernel, stride=1)
print(output)
