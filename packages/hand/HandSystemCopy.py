from packages.Import import *
from packages.tool.Utils import IMAGETOOL,SMOOTH
from packages.hand.HandExtract import HANDEXTRACT
from packages.tool.Control import CONTROL

fourcc=cv2.VideoWriter_fourcc(*"mp4v")
out=cv2.VideoWriter("/home/balaa/Desktop/aaa.mp4",fourcc,10,(650,650))


class HandSystem:
    def __init__(self) -> None:
        logger.info("手势识别系统开启...")
        # 指定手部区域
        self.hand_region_rect=(620,10,1270,660)


    def start(self,MODEL):
        # 打开摄像头
        camera=cv2.VideoCapture(0)
        # 如果没有成功打开摄像头
        if not camera.isOpened():
            logger.error("打开摄像头失败，请检查摄像头！")
            return
        # 如果成功打开摄像头，则打印出分辨率
        camera.set(3,1280)
        camera.set(4,720)
        logger.info("摄像头已经打开，视频流分辨率为({},{}), 帧率为{}fps.".format(camera.get(3),camera.get(4),camera.get(cv2.CAP_PROP_FPS)))

        
        while True:
            # 读视频
            ret,frame=camera.read()
            ## flipCode=1表示依竖直中轴线翻转
            frame=cv2.flip(frame,flipCode=1)

            # 控制退出及暂停视频
            if not ret:
                ## 打开摄像头不应该出现ret为false，如果出现说明出错
                logger.error("读取视频流失败，请检查！")
                break
            key=cv2.waitKey(1)
            if key==ord('q'):
                logger.info("正在退出手势识别系统...")
                break
            if key==32:
                logger.info("暂停视频流...")
                cv2.waitKey(0)

            
            # 取手部感兴趣区域
            hand_roi=IMAGETOOL.SubImg(frame,self.hand_region_rect)

            # 肤色检测
            hand_split_mask=HANDEXTRACT.EllipseDetect(hand_roi)
            if not hand_split_mask.any():
                continue
            
            # 手部分割图像
            hand_split_roi=cv2.bitwise_and(hand_roi,hand_roi,mask=hand_split_mask)
            
            # 识别手势
            # screen=cv2.resize(IMAGETOOL.grabScreen(),(1280,720))
            # figure_digital=MODEL.refer(hand_split_roi)
            # cv2.putText(hand_split_roi,str(figure_digital),(100,200 ), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)
            # if figure_digital==1:
            #     finger_point=HANDEXTRACT.getFingerPointFor1(hand_split_mask)
            #     cv2.circle(hand_split_roi,finger_point,10,(0,0,255),-1)

            # 计算指尖位置,控制鼠标
            # CONTROL.control(figure_digital,hand_split_mask)
            # if finger_point is not None:
            #     # 捕获屏幕画面
            #     x=int(finger_point[0]*1280/630)
            #     y=int(finger_point[1]*720/315)
                # cv2.circle(screen,(x,y),10,(0,0,255),10)
            

            out.write(hand_split_roi)
            cv2.namedWindow("Camera Feed",0)
            cv2.imshow("Camera Feed",hand_split_roi)
            


        cv2.destroyAllWindows()
        camera.release()
        logger.info("已退出手势识别系统.")