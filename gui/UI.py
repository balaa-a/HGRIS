from packages.Import import *
from packages.hand.HandSystem import HANDSYSTEM
from packages.model.Model import Model
from packages.tool.Utils import LOG


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        # 设置工具窗口的大小，前两个参数决定窗口的位置
        self.setGeometry(100, 100, 600, 680)
        # 设置工具窗口的标题
        self.setWindowTitle("基于视觉手势识别的交互系统")
        # 设置窗口的图标
        # w.setWindowIcon(QtGui.QIcon('x.jpg'))
        

        # 显示视频
        self.label0=QtWidgets.QLabel(self)
        self.label0.setGeometry(QtCore.QRect(20, 20, 380, 380))
        img=cv2.imread("./resources/imgs/bg.png")
        self.bg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.label0.setPixmap(QPixmap.fromImage(self.bg))


        # 当前手势
        self.label1 = QtWidgets.QLabel(self)
        ## 设置标签的左边距，上边距，宽，高
        self.label1.setGeometry(QtCore.QRect(420, 20, 90, 20))
        ## 设置文本标签的字体和大小，粗细等
        self.label1.setFont(QtGui.QFont("Roman times", 10))
        self.label1.setText("当前手势")
        ## 显示手势 
        self.labeltext1 = QtWidgets.QLabel(self)
        self.labeltext1.setGeometry(QtCore.QRect(420, 40, 160, 60))
        self.labeltext1.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext1.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")

        
        # 指尖坐标
        self.label2 = QtWidgets.QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label2.setGeometry(QtCore.QRect(420, 120, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label2.setFont(QtGui.QFont("Roman times", 10))
        self.label2.setText("指尖坐标")
        # 添加设置一个文本框
        self.labeltext2 = QtWidgets.QLabel(self)
        self.labeltext2.setGeometry(QtCore.QRect(420, 140, 160, 60))
        self.labeltext2.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext2.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 光标坐标
        self.label3 = QtWidgets.QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label3.setGeometry(QtCore.QRect(420, 220, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label3.setFont(QtGui.QFont("Roman times", 10))
        self.label3.setText("光标坐标")
        # 添加设置一个文本框
        self.labeltext3 = QtWidgets.QLabel(self)
        self.labeltext3.setGeometry(QtCore.QRect(420, 240, 160, 60))
        self.labeltext3.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext3.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 准确率
        self.label4 = QtWidgets.QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label4.setGeometry(QtCore.QRect(420, 320, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label4.setFont(QtGui.QFont("Roman times", 10))
        self.label4.setText("待选文本框")
        # 添加设置一个文本框
        self.text4 = QtWidgets.QTextEdit(self)
        self.text4.setGeometry(QtCore.QRect(420, 340, 160, 60))
        self.text4.setLineWrapMode(True)
        

        # 日志
        self.label5 = QtWidgets.QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label5.setGeometry(QtCore.QRect(20, 420, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label5.setFont(QtGui.QFont("Roman times", 10))
        self.label5.setText("日志打印")
        # 添加设置一个文本框
        self.text5 = QtWidgets.QTextEdit(self)
        self.text5.setGeometry(QtCore.QRect(20, 440, 560, 140))
        self.text5.setLineWrapMode(True)


        # 输入文本框
        self.text6 = QtWidgets.QTextEdit(self)
        # 调整文本框的位置大小
        self.text6.setGeometry(QtCore.QRect(20, 610, 140, 50))
        self.text6.setLineWrapMode(True)
        self.text6.setText("1812050129-王浩-基于视觉手势识别的交互系统")


        # OPEN按钮
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setGeometry(QtCore.QRect(180, 610, 120, 50))
        self.btn1.setText("开始")

        # CLOSE按钮
        self.btn2 = QtWidgets.QPushButton(self)
        self.btn2.setGeometry(QtCore.QRect(320, 610, 120, 50))
        self.btn2.setText("结束")

        # PAUSE按钮
        self.btn3 = QtWidgets.QPushButton(self)
        self.btn3.setGeometry(QtCore.QRect(460, 610, 120, 50))
        self.btn3.setText("暂停")
        
        
        # 显示窗体
        self.show()
        
        
