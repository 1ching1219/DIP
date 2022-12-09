import sys
import torch
import torchvision
print('python', sys.version.split('\n')[0])
print('torch', torch.__version__)
print('torchvision', torchvision.__version__)

import torch.nn as nn 
import torch.nn.functional as F

class YourCNNModel(nn.Module): 
    def __init__(self): 
        super().__init__()
        
        self.cnn_model = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, stride = 1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 128, 3, stride = 1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.2),

            nn.Conv2d(128, 128, 3, stride = 1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.2),

            nn.Conv2d(128, 256, 3, stride = 1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.2),

            nn.Conv2d(256, 256, 3, stride = 1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.fc_model = nn.Sequential(
            nn.Linear(256*3*3, 500),
            nn.Dropout(0.2),
            nn.ReLU(),
            nn.Linear(500, 5)
        )

    def forward(self, x): 
        if not isinstance(x, torch.Tensor):
            x = torch.Tensor(x)

        x = self.cnn_model(x)
        # print(x.shape)
        x = x.view(x.size(0), -1)
        x = self.fc_model(x)
        out = F.log_softmax(x, dim = 1)

        return out

device = torch.device('cuda')
# or
# device = torch.device('cpu')

model = YourCNNModel()
model = model.to(device)

ckpt = torch.load('./NAME_OF_THIS_EXPERIMENT.pt')
model.load_state_dict(ckpt)

from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
def load_data(path):
    img = Image.open(path)
    convert_tensor = transforms.Compose([transforms.Resize([224, 224]),
                                transforms.ToTensor(),
                                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])

    img = convert_tensor(img)
    img = img.unsqueeze(0)
    return img

img = load_data("./Eberndorf_Köcking_Sonnenblumenfeld_Biohof_Tomic_18072014_0792.jpg")

def predict(images, model):
    model.eval()
    with torch.no_grad():
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            output = predicted.item()
    if(output == 0):result = 'daisy'
    elif(output == 1):result = 'dandelion'
    elif(output == 2):result = 'rose'
    elif(output == 3):result = 'sunflower'
    elif(output == 4):result = 'tulip'
    return result

result = predict(img, model)
print(result)