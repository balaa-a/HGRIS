from packages.Import import *
from packages.tool.Mouse import MOUSE
from packages.hand.HandExtract import HANDEXTRACT
from packages.tool.Utils import IMAGETOOL, SMOOTH,TRANS

class Control():
    def __init__(self) -> None:
        self.pre_figure_digital=-1
        self.pre_finger_point=None
        self.pre_screen_point=None
        self.scale=2
        self.mode=0
        # 手势图像与屏幕的映射区域
        self.finger_rect=(25,25,625,363)
        # 屏幕上对应的映射区域
        self.screen_rect=(0,0,1920,1080)
        # 手势图像映射区域四角坐标
        finger_corner=np.array([[self.finger_rect[0],self.finger_rect[1]],
            [self.finger_rect[2],self.finger_rect[1]],
            [self.finger_rect[0],self.finger_rect[3]],
            [self.finger_rect[2],self.finger_rect[3]]])
        # 屏幕四角坐标
        screen_corner=np.array([[self.screen_rect[0],self.screen_rect[1]],
            [self.screen_rect[2],self.screen_rect[1]],
            [self.screen_rect[0],self.screen_rect[3]],
            [self.screen_rect[2],self.screen_rect[3]]])
        # 指尖坐标映射到屏幕坐标的矩阵
        self.M=TRANS.getScaleTransMat(finger_corner,screen_corner)


    def calScreenLocByMap(self,finger_point,M):
        # 计算屏幕坐标
        X=int(M[0,0]*finger_point[0]+M[0,2])
        Y=int(M[0,0]*finger_point[1]+M[1,2])

        return IMAGETOOL.limit(X,Y,self.screen_rect)


    def calScreenLocByStimul(self,finger_point):
        if self.mode==0:
            self.pre_finger_point=[finger_point[0],finger_point[1]]
            self.pre_screen_point=[MOUSE.x,MOUSE.y]
            self.mode=1
        pre_x,pre_y=self.pre_finger_point[0],self.pre_finger_point[1]
        cur_x,cur_y=finger_point[0],finger_point[1]
        delta_x,delta_y=cur_x-pre_x,cur_y-pre_y
        delta_X,delta_Y=delta_x*self.scale,delta_y*self.scale
        pre_X,pre_Y=self.pre_screen_point[0],self.pre_screen_point[1]
        X,Y=pre_X+delta_X,pre_Y+delta_Y

        return IMAGETOOL.limit(X,Y,self.screen_rect)



    def control(self,figure_digital,hand_split_mask):
        if figure_digital==1:
            self.pre_figure_digital=1
            # 计算指尖坐标
            finger_point=HANDEXTRACT.getFingerPointFor1(hand_split_mask)
            # 映射法移动光标
            # screen_point=self.calScreenLocByMap(finger_point,self.M)
            # 模拟法移动光标
            screen_point=self.calScreenLocByStimul(finger_point)
            # 移动鼠标
            MOUSE.moveTo(screen_point[0],screen_point[1])
        
        elif figure_digital==0 and self.pre_figure_digital!=0:
            self.pre_figure_digital=0
            MOUSE.down()

        elif figure_digital==2:
            self.pre_figure_digital=2
            self.mode=0
            MOUSE.up()
        elif figure_digital==3 and self.pre_figure_digital!=3:
            self.pre_figure_digital=3
            MOUSE.rightClick()
        elif figure_digital==4 and self.pre_figure_digital!=4:
            self.pre_figure_digital=4
            MOUSE.leftClick()
        elif figure_digital==5 and self.pre_figure_digital!=5:
            self.pre_figure_digital=5
            MOUSE.leftDoubleClick()
        elif figure_digital==6 and self.pre_figure_digital!=6:
            self.pre_figure_digital=6
            # MOUSE.scrool()
        elif figure_digital==7 and self.pre_figure_digital!=7:
            self.pre_figure_digital=7
        elif figure_digital==8 and self.pre_figure_digital!=8:
            self.pre_figure_digital=8
        elif figure_digital==9 and self.pre_figure_digital!=9:
            self.pre_figure_digital=9
            MOUSE.up()
        
        
        
        
        
CONTROL=Control()