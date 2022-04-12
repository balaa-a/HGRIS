from gui.UI import MainWindow
from packages.Import import *
from packages.hand.HandSystem import HANDSYSTEM
from packages.model.Model import Model
from packages.tool.Utils import LOG



class Dispaly():
    
    def __init__(self):
        self.ui=MainWindow()
        LOG.log("手势识别系统开启...")
        self.ui.text5.setText(LOG.log_lst)
        # 关闭视频事件
        self.closeEvent = threading.Event()
        self.closeEvent.clear()
        # 暂停事件
        self.pauseEvent = threading.Event()
        self.pauseEvent.clear()
        self.n=0
        # 加载MODEL
        self.MODEL=Model('./resources/checkpoints/best-new-bak.pt')
        # 将按钮置灰
        self.ui.btn1.setEnabled(True)
        self.ui.btn2.setEnabled(False)
        self.ui.btn3.setEnabled(False)
        self.ui.btn1.clicked.connect(self.open)
        self.ui.btn2.clicked.connect(self.close)
        self.ui.btn3.clicked.connect(self.pause)
        


    def open(self):
        LOG.log("打开视频...")
        self.ui.text5.setText(LOG.log_lst)
        th = threading.Thread(target=self.display)
        th.start()



    def close(self):
        LOG.log("关闭视频...")
        self.ui.text5.setText(LOG.log_lst)
        if self.pauseEvent.is_set():
            self.n+=1
            self.pauseEvent.clear()
        self.closeEvent.set()



    def pause(self):
        self.n+=1

        if self.n%2==1:
            LOG.log("暂停视频...")
            self.pauseEvent.set()
            self.ui.btn3.setText("继续")
        else:
            LOG.log("继续视频...")
            self.pauseEvent.clear()
            self.ui.btn3.setText("暂停")
        self.ui.text5.setText(LOG.log_lst)



    def display(self):
        self.ui.btn1.setEnabled(False)
        self.ui.btn2.setEnabled(True)
        self.ui.btn3.setEnabled(True)

        # 打开视频
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
            # 暂停
            if self.pauseEvent.is_set():
                while self.n%2==1:
                    continue
            # 关闭视频
            if self.closeEvent.is_set():
                break
            # 播放视频
            ret,frame=camera.read()
            if not ret:
                logger.error("读取摄像头失败！")
                break
            # 手势识别交互
            result=HANDSYSTEM.start(self.MODEL,frame)
            if result is None:
                continue
            frame,figure_digital,finger_point,screen_point=result
            # 显示视频
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.label0.setPixmap(QPixmap.fromImage(img))
            self.ui.update()
            cv2.waitKey(1)

            # 将手势识别、指尖检测、光标坐标显示
            self.ui.labeltext1.setText(str(figure_digital))
            self.ui.labeltext2.setText(str(finger_point))
            self.ui.labeltext3.setText(str(screen_point))
            LOG.log(str(figure_digital))
            LOG.log(str(finger_point))
            LOG.log(str(screen_point))


        cv2.destroyAllWindows()
        camera.release()
        self.closeEvent.clear()
        self.pauseEvent.clear()
        self.ui.label0.setPixmap(QPixmap.fromImage(self.ui.bg))
        self.ui.btn1.setEnabled(True)
        self.ui.btn2.setEnabled(False)
        self.ui.btn3.setEnabled(False)
        
