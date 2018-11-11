import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torch import nn

from memgen.transforms import Thumbnail


class _ResNetFeatureExtractor(nn.Module):
    def __init__(self, avg_size=1, pretrained=True):
        super().__init__()

        self.model = nn.Sequential(
            *list(models.resnet152(pretrained=pretrained).children())[:-2],
            nn.AdaptiveAvgPool2d(avg_size)
        )
        self.output_size = 512 * (avg_size * 4)

    def forward(self, x):
        return self.model(x)


class Embedder:
    def __init__(self):
        self.fe = _ResNetFeatureExtractor()
        self.fe.eval()

        self.transform = transforms.Compose([
            Thumbnail((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

        ])

    def embed(self, image):
        image = image.convert('RGB')
        x = self.transform(image).unsqueeze(0).detach()
        with torch.no_grad():
            e = self.fe(x)
        e = e.squeeze().detach().numpy()
        if e.shape[0] != self.fe.output_size:
            return None
        return e
