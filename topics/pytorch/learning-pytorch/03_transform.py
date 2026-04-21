from torchvision import transforms
from PIL import Image

img_path = "data/hymenoptera_data/train/ants/0013035.jpg"
img = Image.open(img_path)

print(type(img))

img_trans = transforms.ToTensor()

tensor_img = img_trans(img)
print(tensor_img, type(tensor_img))
