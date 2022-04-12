from packages.Import import *

class MyDataset(Dataset):
    def __init__(self,imgs_dir,transform=None) -> None:
        super(Dataset,self).__init__()
        self.imgs_labels=[int(i) for i in os.listdir(imgs_dir)]
        self.imgs_dir=imgs_dir
        self.transform=transform
    

    def __len__(self):
        '''
        描述：返回每个标签的数据集的数据的个数；
        '''
        n=0
        for label in self.imgs_labels:
            n+=len(os.listdir(os.path.join(self.imgs_dir,str(label))))
        return n

    
    def __getitem__(self, label:string, index):
        '''
        描述：从标签label的数据下获取第index个图像；
        参数列表：标签label，下标index；
        返回值：img：tensor，标签label；
        '''
        imgs_path=os.path.join(self.imgs_dir,label)
        imgfile=os.path.join(imgs_path,os.listdir(imgs_path)[index])
        img=plt.imread(imgfile)
        if self.transform:
            img=self.transform(img)
        return img,int(label)
    

    def getDataLoader(self,batchsize=100,train_ratio=0.8):
        '''
        描述: 从指定的数据集路径中读取出所有的图像数据,转换为tensor数据,再将全部数据分为训练和测试,返回迭代器训练和测试的迭代器;
        参数列表: data_root指定数据集路径;batchsize;train_ratio;
        返回值: train_loader训练数据集迭代器;test_loader测试集迭代器.
        '''
        data_root=self.imgs_dir
        
        data_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize([224,224]),
            transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5, 0.5, 0.5])
        ])

        dataset = ImageFolder(data_root,transform = data_transform)
        trainsize=int(train_ratio*len(dataset))
        testsize=len(dataset)-trainsize
        trainset,testset = torch.utils.data.random_split(dataset,[trainsize,testsize])
        
        # trainloader,testloader表示训练数据与测试数据的迭代器，每个迭代元素包含100张图片及对应标签。
        train_loader = DataLoader(trainset,batch_size=batchsize)
        test_loader = DataLoader(testset, batch_size=batchsize)

        return train_loader,test_loader
