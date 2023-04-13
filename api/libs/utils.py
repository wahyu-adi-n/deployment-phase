import torch
from PIL import Image
from torchvision import transforms as T

def get_device():
    return 'cuda:0' if torch.cuda.is_available else 'cpu'

def predict(model: torch.nn.Module,
            image: Image, 
            transform = None,
            device: torch.device=get_device):
    
    if transform is not None:
        image_transform = transform
    else:
        image_transform = T.Compose([
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
    
    return target_image_pred_probs, target_image_pred_label