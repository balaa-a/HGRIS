from packages.Import import *
from packages.tool.Utils import IMAGETOOL
from packages.hand.HandExtract import HANDEXTRACT
from packages.tool.Control import CONTROL
from packages.tool.Mouse import MOUSE


class HandSystem:
    def __init__(self) -> None:
        # 指定手部区域
        self.hand_region_rect=(620,10,1270,660)


    def start(self,MODEL,frame):
        ## flipCode=1表示依竖直中轴线翻转
        frame=cv2.flip(frame,flipCode=1)

        # 取手部感兴趣区域
        hand_roi=IMAGETOOL.SubImg(frame,self.hand_region_rect)

        # 肤色检测
        hand_split_mask=HANDEXTRACT.EllipseDetect(hand_roi)
        if not hand_split_mask.any():
            return
        
        # 手部分割图像
        hand_split_roi=cv2.bitwise_and(hand_roi,hand_roi,mask=hand_split_mask)
        
        # 识别手势
        figure_digital=MODEL.refer(hand_split_roi)
        cv2.putText(hand_split_roi,str(figure_digital),(100,200 ), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)
        
        # 指尖检测
        finger_point=None
        if figure_digital==1:
            finger_point=HANDEXTRACT.getFingerPointFor1(hand_split_mask)
            cv2.circle(hand_split_roi,finger_point,10,(0,0,255),-1)

        # 控制鼠标
        CONTROL.control(figure_digital,hand_split_mask)
        # print(figure_digital)
        # 后处理
        hand_split_roi=cv2.cvtColor(hand_split_roi,cv2.COLOR_BGR2RGB)
        hand_split_roi=cv2.resize(hand_split_roi,(380,380))


        return (hand_split_roi,figure_digital,finger_point,(MOUSE.x,MOUSE.y))
            


HANDSYSTEM=HandSystem()