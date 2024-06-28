from utils import to_cuda
from torchvision import transforms as T
from InsightFace_Pytorch.model import Backbone, MobileFaceNet
import torch

preprocess = T.Compose(
    [
        T.ToTensor(),
        T.Resize((112, 112), antialias=True),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


class FaceEmbedder:
    def __init__(self) -> None:
        # self.feature_extractor = Backbone(50, 0.5, "ir_se")
        self.feature_extractor = MobileFaceNet(512)
        # weight = torch.load("model_ir_se50.pth",map_location=torch.device('cpu'))
        weight = torch.load("model_mobilefacenet.pth", map_location=torch.device('cpu'))
        self.feature_extractor.load_state_dict(weight)
        # self.feature_extractor = to_cuda(self.feature_extractor)
        self.feature_extractor = self.feature_extractor.to(torch.device('cpu'))
        self.feature_extractor.eval()

    def embed_face(self, face_img):
        img = to_cuda(preprocess(face_img))
        img = img.reshape(1, *img.shape)
        
        return self.feature_extractor(img).detach().cpu().numpy()[0]
