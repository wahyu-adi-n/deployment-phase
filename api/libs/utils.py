import torch
from PIL import Image
from torchvision import transforms as T
import cv2
import numpy as np
import base64


def get_device():
    return 'cuda:0' if torch.cuda.is_available() else 'cpu'

def get_class_names():
    return ['airplane',
             'automobile',
             'bird',
             'cat',
             'deer',
             'dog',
             'frog',
             'horse',
             'ship',
             'truck']
             
def predict(model: torch.nn.Module,
            image: Image,
            class_names = get_class_names(),
            transform=None,
            device: torch.device = get_device()):

    if transform is not None:
        image_transform = transform
    else:
        image_transform = T.Compose([
            T.Resize(size=(32, 32)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]),
        ])

    model.to(device)

    model.eval()
    with torch.inference_mode():
        transformed_image = image_transform(image).unsqueeze(dim=0)
        target_image_pred = model(transformed_image.to(device))
        target_image_pred_probs = torch.softmax(target_image_pred, dim=1)
        target_image_pred_label = torch.argmax(target_image_pred_probs, dim=1)

    return target_image_pred_probs.max().item(), class_names[target_image_pred_label.item()]


def readb64(uri):
    image = cv2.cvtColor(cv2.imdecode(np.frombuffer(base64.b64decode(
        uri.split(',')[-1]), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    return image
