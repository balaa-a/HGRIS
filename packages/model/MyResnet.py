from packages.Import import *

class Bottleneck(nn.Module):
    # 用于生成网络层数
    extention=4

    def __init__(self,inchannel,midchannel,stride,downsample=None) -> None:
        super(Bottleneck,self).__init__()
        # bollteneck层的卷积操作，conv2、conv3不会改变图像的尺寸但会改变通道数，conv1可以改变尺寸和通道数。
        self.conv1=nn.Conv2d(inchannel,midchannel,kernel_size=1,stride=stride,bias=False)
        self.bn1=nn.BatchNorm2d(midchannel)
        
        self.conv2=nn.Conv2d(midchannel,midchannel,kernel_size=3,stride=1,padding=1,bias=False)
        self.bn2=nn.BatchNorm2d(midchannel)
        
        self.conv3=nn.Conv2d(midchannel,midchannel*self.extention,kernel_size=1,stride=1,bias=False)
        self.bn3=nn.BatchNorm2d(midchannel*self.extention)
        
        self.downsample=downsample
        self.relu=nn.ReLU(inplace=True)
        

    def forward(self,x):
        residual=x
        
        out=self.bn1(self.conv1(x))
        out=self.bn2(self.conv2(out))
        out=self.bn3(self.conv3(out))
        
        # 若downsample存在不为None则注意将残差操作之后再相加，因为不操作x可能无法对齐无法逐元素相加
        if self.downsample!=None:
            residual=self.downsample(x)
        
        return self.relu(out+residual)



class MyResnet(nn.Module):
    def __init__(self,Block,blocknum_lst,classes_num) -> None:
        super(MyResnet,self).__init__()
        self.inchannel=64
        
        # stem
        self.conv1=nn.Conv2d(in_channels=3,out_channels=self.inchannel,kernel_size=7,stride=2,padding=3,bias=False)
        self.bn1=nn.BatchNorm2d(self.inchannel)
        self.relu=nn.ReLU()
        self.maxpool=nn.MaxPool2d(kernel_size=3,stride=2,padding=1)
        
        # stages
        ## 产生四个stage，主要参数是 Block模板，卷积层的通道数，层数，步长
        self.stage1=self.make_layer(Block,64,blocknum_lst[0],1)
        self.stage2=self.make_layer(Block,128,blocknum_lst[1],2)
        self.stage3=self.make_layer(Block,256,blocknum_lst[2],2)
        self.stage4=self.make_layer(Block,512,blocknum_lst[3],2)
        
        # tail
        self.avgpool=nn.AvgPool2d(kernel_size=7,stride=1)
        self.fc=nn.Linear(512*Block.extention,classes_num)
    

    def make_layer(self,Block,midchannel,block_num,stride):
        '''
        描述：根据Block模板生成网络模块；
        参数：Block模板；midchannel（基本确定）；block_num表示Block中层的个数；stride表示步长；
        返回：序列化的网络层；
        '''
        layers_lst=[]
        
        # downsample为判断生成conv blovk还是identity block标志
        downsample=None
        if (stride!=1)|(midchannel*Block.extention!=self.inchannel):
            downsample=nn.Sequential(
                nn.Conv2d(self.inchannel,midchannel*Block.extention,stride=stride,kernel_size=1,bias=False),
                nn.BatchNorm2d(midchannel*Block.extention)
            )
        
        # Conv Block输入和输出的维度（通道数和size）是不一样的，所以不能连续串联，他的作用是改变网络的维度
        # Identity Block 输入维度和输出（通道数和size）相同，可以直接串联，用于加深网络
        
        #Conv_block
        conv_block=Block(self.inchannel,midchannel,stride=stride,downsample=downsample)
        layers_lst.append(conv_block)
        self.inchannel=midchannel*Block.extention

        #Identity Block
        for i in range(1,block_num):
            layers_lst.append(Block(self.inchannel,midchannel,stride=1))

        return nn.Sequential(*layers_lst)
    

    def forward(self,x):
        out=self.maxpool(self.relu(self.bn1(self.conv1(x))))
        out=self.stage4(self.stage3(self.stage2(self.stage1(out))))
        # out=self.fc(torch.flatten(self.avgpool(out),1))
        out=self.avgpool(out)
        out=torch.flatten(out,1)
        out=self.fc(out)
        return out

