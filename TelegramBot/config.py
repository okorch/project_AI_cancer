import torch
from PIL import Image
import torchvision.transforms as transforms
from TelegramBot import Model1


async def process_photo(stream):
    '''
     Preprocesses the photo to be fed into the model for prediction.
    Parameters:
        - stream: A file-like object representing the image file.
    Returns:
        - image: A PyTorch tensor of the preprocessed image.
    '''
    image = Image.open(stream)
    image = transforms.ToTensor()(image)
    image = transforms.Resize((64, 64))(image)
    return image

async def predict(input_tensor):
    '''
    Uses a pre-trained PyTorch model to predict whether the given image contains cancer.
    Parameters:
        - input_tensor: A PyTorch tensor representing the preprocessed image.
    Returns:
        - predicted.item(): The predicted label for the given image (0 for no cancer, 1 for cancer).
    '''
    model = Model1.Model()
    weight = 'weight.pth'
    weight = torch.load(weight)
    model.load_state_dict(weight)

    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output.data, 1)

    return predicted.item()