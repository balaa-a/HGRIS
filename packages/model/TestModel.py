from packages.model.MyResnet import *
from packages.model.MyDataset import *


def main():
    # 加载模型
    model=MyResnet(Bottleneck,[3,4,6,3],6)
    model.load_state_dict(torch.load("../../checkpoints/best.pt"))
    device= "cuda" if torch.cuda.is_available else "cpu"
    model.to(device)
    logger.info('Using {} device. '.format(device))
    logger.info("CUDA_VISIBLE_DEVICES {}.".format(torch.cuda.device_count()))


    # 加载测试数据
    data_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize([224,224]),
        transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5, 0.5, 0.5])
    ])
    data_path="./mydataset/"
    dataset = ImageFolder(data_path,transform = data_transform)
    data = DataLoader(dataset,batch_size=5,shuffle=True)


    # # 批量测试
    # with torch.no_grad():
    #     correct=0
    #     total=0
    #     for i,(inputs,labels) in enumerate(data):
    #         inputs,labels=inputs.to('cuda'),labels.to("cuda")
    #         out=model(inputs)

    #         _,predicted=torch.max(out,dim=1)
    #         print(labels)
    #         print(predicted)
    #         correct+=predicted.eq(labels.data).cpu().sum()
    #         total+=labels.size(0)
    #         # print(out)
    #     print(correct,"\t",total,"\t", correct/total)


    # 单个测试
    # data_path="./mydataset/"
    # DATASET=MyDataset(data_path,transform=data_transform)
    # start=time.time()
    # with torch.no_grad():
    #     correct=0
    #     total=0
    #     for i in range(20):
    #         img,label=DATASET.__getitem__('5',i)
    #         imgs=torch.unsqueeze(img,dim=0).to("cuda")

    #         out=model.forward(imgs)
    #         _,predicted=torch.max(out,dim=1)
    #         correct+= predicted.eq(label).sum()
    #         total+=1
    #         print(predicted)
    #     print("acc is: ",(correct/total).item())
    # end=time.time()
    # print(end-start)

    # wh测试集
    start=time.time()
    with torch.no_grad():
        img=plt.imread("./mydataset/5/1.jpg")
        img=data_transform(img)
        imgs=torch.unsqueeze(img,dim=0).to("cuda")

        out=model(imgs)
        _,predicted=torch.max(out,dim=1)
        print(predicted)
    end=time.time()
    print(end-start)


if __name__=="__main__":
    main()