from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import numpy as np

writer = SummaryWriter("logs")
img_path = "data/hymenoptera_data/train/ants/0013035.jpg"
img_PIL = Image.open(img_path)
img_array = np.array(img_PIL)
print(type(img_array))
print(img_array.shape)

writer.add_image("test", img_array, dataformats="HWC")
for i in range(100):
    writer.add_scalar("y=2x", 2 * i, i)

writer.close()
