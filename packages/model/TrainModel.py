from MyDataset import *
from MyResnet import *

os.chdir("./Hand/code")
logger.add("./log.txt")

def main():
    device= "cuda" if torch.cuda.is_available else "cpu"
    logger.info('Using {} device. '.format(device))
    logger.info('CUDA_VISIBLE_DEVICES ',torch.cuda.device_count())
    
    # 加载训练数据
    data_path="../data/train/"
    batch_size=10
    train_ratio=0.8
    DATASET=MyDataset(data_path)

    # 创建模型
    num_class=6
    model=MyResnet(Bottleneck,[3,4,6,3],num_class)
    model=model.to(device)
    logger.info(model)

    # 损失函数
    criterion=nn.CrossEntropyLoss()
    lr=0.0001
    optim=torch.optim.Adam(model.parameters(),lr=lr)
    epoches=100
    

    # 训练过程
    logger.info("Start Training!")
    val_acc_lst=[]
    ## 保存模型参数
    out_dir="checkpoints/" 
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # 训练、验证    
    for epoch in range(epoches):
        train_loader,val_loader=DATASET.getDataLoader(batch_size,train_ratio)
        train_len=train_loader.__len__()
        model.train()
        sum_loss=0
        correct=0
        total=0
        
        ## 训练
        logger.info("Epoch{}, Traing...".format(epoch))
        for i,(inputs,labels) in enumerate(train_loader):
            inputs,labels=inputs.to(device),labels.to(device)
            out=model(inputs)
            loss=criterion(out,labels)
            optim.zero_grad()
            loss.backward()
            optim.step()
            
            sum_loss+=loss.item()
            _,predicted=torch.max(out,dim=1)
            ### 计算训练过程中正确率
            total+=labels.size(0)
            correct+=predicted.eq(labels.data).cpu().sum()
            logger.info('[epoch:{}, iter:{}] Loss:{} | Acc: {}'.format(epoch + 1, (i + 1 + epoch * train_len), sum_loss / (i + 1), 100. * correct / total))
        

        ## 测试
        logger.info("Epoch{}, Val...".format(epoch))
        with torch.no_grad():
            model.eval()
            correct=0
            total=0
            for i,(inputs,labels) in enumerate(val_loader):
                inputs,labels=inputs.to(device),labels.to(device)
                out=model(inputs)
                
                _, predicted = torch.max(out.data, dim=1)
                total += labels.size(0)
                correct += (predicted == labels).sum()

            logger.info('Val\'s ac is: {}'.format(100 * correct / total))
            acc_val = 100 * correct / total
            val_acc_lst.append(acc_val)
 
        ## 模型参数保存
        torch.save(model.state_dict(), out_dir+"last.pt")
        ## 将表现最好的模型参数保存
        if acc_val == max(val_acc_lst):
            torch.save(model.state_dict(), out_dir+"best.pt")
            logger.info("save epoch {} model.".format(epoch))


if __name__=="__main__":
    main()