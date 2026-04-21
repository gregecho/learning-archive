import torch
import torch.nn

input = torch.tensor([1, 2, 3], dtype=torch.float32)
output = torch.tensor([1, 2, 5], dtype=torch.float32)

loss = torch.nn.L1Loss()
result = loss(input, output)
print(result)
