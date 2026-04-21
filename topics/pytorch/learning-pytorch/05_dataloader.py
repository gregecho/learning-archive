import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset_trans = transforms.Compose([transforms.ToTensor()])

test_data = torchvision.datasets.CIFAR10(
    root="./data", train=False, transform=dataset_trans, download=True
)

test_loader = DataLoader(
    dataset=test_data, batch_size=64, shuffle=True, num_workers=0, drop_last=False
)

img, target = test_data[0]
print(img.shape)
print(target)
print(test_loader)

writer = SummaryWriter("logs")
step = 0
for data in test_loader:
    imgs, targets = data
    writer.add_images("loader_img", imgs, step)
    step += 1
    # print(imgs.shape)
    # print(targets)
writer.close()
