from packages.model.MyResnet import *
from packages.model.MyDataset import *

class Model:
    def __init__(self,ptfile) -> None:
        # 加载模型
        self.model=MyResnet(Bottleneck,[3,4,6,3],10)
        self.model.load_state_dict(torch.load(ptfile))
        device= "cuda" if torch.cuda.is_available else "cpu"
        self.model.to(device)
        logger.info('Using {} device. '.format(device))
        logger.info("CUDA_VISIBLE_DEVICES {}.".format(torch.cuda.device_count()))

        # 数据变换
        self.data_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize([224,224]),
            transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5, 0.5, 0.5])
        ])
    

    def refer(self,img:ndarray):
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        with torch.no_grad():
            img=self.data_transform(img)
            imgs=torch.unsqueeze(img,dim=0).to("cuda")
            out=self.model(imgs)
            _,predicted=torch.max(out,dim=1)
            
        return predicted.item()
