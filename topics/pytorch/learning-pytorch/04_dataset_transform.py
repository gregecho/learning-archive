import torchvision
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

dataset_trans = transforms.Compose([transforms.ToTensor()])

train_set = torchvision.datasets.CIFAR10(
    root="./data", train=True, transform=dataset_trans, download=True
)
test_set = torchvision.datasets.CIFAR10(
    root="./data", train=False, transform=dataset_trans, download=True
)

writer = SummaryWriter("")
for i in range(10):
    img, target = test_set[i]
    writer.add_image("test_img", img_tensor=img, global_step=i)

writer.close()
