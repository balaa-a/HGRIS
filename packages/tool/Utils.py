from packages.Import import *


class Log():
    '''
    描述：此Log类给GUI的日志文本框使用；
    '''
    def __init__(self) -> None:
        self.log_lst=" === Start Logging ===\n"


    def log(self,log_str):
        '''
        描述：以日志字符串形式保存，持续叠加；
        '''
        aline=time.ctime()+"  "+os.path.relpath(__file__)+"  "+log_str+"\n"
        self.log_lst=self.log_lst+aline
        


class ImageTool:
    def __init__(self) -> None:
        pass

    def SubImg(self,src:ndarray,rect:tuple):
        '''
        参数：img表示源图像，rect表示要裁剪图像的矩形区域，保存左上角、右下角坐标；
        '''
        return src[rect[1]:rect[3],rect[0]:rect[2]]

    def grabScreen(self):
        '''
        描述：获取屏幕全屏画面；
        参数：无；
        返回：ndarray，RGB格式；
        '''
        screen=ImageGrab.grab()
        screen=np.array(screen)
        screen=cv2.cvtColor(screen,cv2.COLOR_BGR2RGB)
        return screen

    def limit(self,x,y,rect:tuple):
        # 若屏幕坐标超出屏幕，则边界
        if x<rect[0]:
            x=rect[0]
        elif x>rect[2]:
            x=rect[2]        
        if y<rect[1]:
            y=rect[1]
        elif y>rect[3]:
            y=rect[3]
        return (x,y)



class Trans():
    def __init__(self) -> None:
        pass
    

    def getScaleTransMat(self,src,dst):
        '''
        描述：根据src、dst计算出适合的缩放、平移矩阵；
        返回：返回2×3矩阵；
        '''
        x,y=src[:,0],src[:,1]
        xx,yy=dst[:,0],dst[:,1]
        
        # 计算矩阵参数    
        num = len(x)
        bigp1 = [[x[0], 1, 0], [y[0], 0, 1]]
        bigp2 = [[xx[0]], [yy[0]]]
        for i in range(1, num):
            p1 = [[x[i], 1, 0], [y[i], 0, 1]]
            bigp1 = np.array(np.vstack((bigp1, p1)), dtype="float32")
            p2 = [[xx[i]], [yy[i]]]
            bigp2 = np.array(np.vstack((bigp2, p2)), dtype="float32")
        Mline = np.dot(np.dot(np.linalg.inv(np.dot(bigp1.T, bigp1)), bigp1.T), bigp2)
        M = np.float32([[Mline[0], 0, Mline[1]], [0, Mline[0], Mline[2]]])
        
        return M


class Smooth:
    def __init__(self,length=10) -> None:
        self.qu=queue.Queue()
        self.queue_length=length
        self.sum_x=0
        self.sum_y=0

    def smooth(self,x:int,y:int):
        '''
        描述：一次平均平滑。用于实现动态序列的平滑，采取对当前值的前n帧取平均作为新的当前值方法平滑；
        参数：待平滑x、y；
        返回：tuple，已平滑x、y;
        '''
        # 前n个序列保存进队列
        if self.qu.qsize()<self.queue_length:
            self.qu.put([x,y])
            self.sum_x+=x
            self.sum_y+=y
            return None
            
        # 取出队列队头元素，放入第i个值
        cur_x=self.sum_x//self.queue_length
        cur_y=self.sum_y//self.queue_length
        tmp=self.qu.get()
        self.sum_x=self.sum_x-tmp[0]+x
        self.sum_y=self.sum_y-tmp[1]+y
        self.qu.put([x,y])

        return (int(cur_x),int(cur_y))
    

    def smooth_2(self,x,y):
        '''
        描述：二次平均平滑。用于实现动态序列的平滑，采取对当前值的前n帧取平均作为新的当前值方法平滑；
        参数：待平滑x、y；
        返回：tuple，已平滑x、y;
        '''
        # 前n个序列保存进队列
        if self.qu.qsize()<self.queue_length:
            self.qu.put([x,y])
            self.sum_x+=x**2
            self.sum_y+=y**2
            return None
            
        # 取出队列队头元素，放入第i个值
        tmp=self.qu.get()
        self.sum_x=self.sum_x-tmp[0]**2+x**2
        self.sum_y=self.sum_y-tmp[1]**2+y**2
        self.qu.put([x,y])

        cur_x=math.sqrt(self.sum_x/self.queue_length)
        cur_y=math.sqrt(self.sum_y/self.queue_length)

        return (int(cur_x),int(cur_y))




class Smooth_WH:
    def __init__(self,length=20) -> None:
        self.lst=[]
        self.tail=0
        self.length=length

    def smooth(self,x,y):
        '''
        描述：用于实现动态序列的平滑，采取对当前值的前n帧后n帧取平均作为新的当前值方法平滑；
        参数：待平滑x、y；
        返回：tuple，已平滑x、y;
        '''
        if len(self.lst)<self.length:
            self.lst.append([x,y])
            self.tail=(self.tail+1)%self.length
            return
        else:
            self.lst=np.array(self.lst)

        # 计算前20帧里面的[\delta x , \delta y]
        self.lst[self.tail]=[x,y]
        self.tail=(self.tail+1)%self.length

        # 求平均x\y方向delta
        q=(self.tail+1)%self.length
        delta_sum=np.array([0,0])
        while q!=self.tail:
            delta_sum=delta_sum+self.lst[q]-self.lst[(q+self.length-1)%self.length]
            q=(q+1)%self.length
        delta_mean=delta_sum/(self.length-1)

        # 计算平滑值，前20帧取已有的，后20帧插值计算的
        x_sum=np.sum(self.lst[:,0])
        y_sum=np.sum(self.lst[:,1])
        last_point=self.lst[(self.tail+self.length-1)%self.length]
        delta_mean=np.array([0,0])
        x_sum=x_sum+((self.length)*last_point[0]+delta_mean[0]*(self.length+1)*self.length/2)
        y_sum=y_sum+((self.length)*last_point[1]+delta_mean[1]*(self.length+1)*self.length/2)
        x_smooth=x_sum//(self.length*2)
        y_smooth=y_sum//(self.length*2)
        
        return (int(x_smooth.item()),int(y_smooth.item()))
        
        

class Stable:
    '''
    描述：手势有可能识别错误，错误率比较低，所以我们希望当偶尔出现错误时候不影响；未使用。
    '''
    def __init__(self,length=10) -> None:
        # lst用于保存连续十个手势数字，[0,1,2,3,4,5]
        self.lst=[]
        self.tail=0
        self.length=length

    def stable(self,x):
        if len(self.lst)<self.length:
            self.lst.append(x)
            self.tail=(self.tail+1)%self.length
            return None
        
        self.lst[self.tail]=x
        self.tail=(self.tail+1)%self.length

        # x取值范围[0,1,2,3,4,5],计数最大的下标对应了其值
        idx=np.argmax(np.bincount(self.lst))
        return idx



# 创建对象
IMAGETOOL=ImageTool()
SMOOTH=Smooth()
TRANS=Trans()
LOG=Log()
