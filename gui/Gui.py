from packages.Import import *
from packages.hand.HandSystem import HANDSYSTEM
from packages.model.Model import Model
from packages.tool.Mouse import MOUSE
from packages.tool.Utils import LOG,MY



class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        # 设置工具窗口的大小，前两个参数决定窗口的位置

        # 显示视频
        self.label0=QLabel(self)
        self.label0.setGeometry(QRect(20, 20, 380, 380))
        img=cv2.imread("./resources/imgs/bg.png")
        self.bg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.label0.setPixmap(QPixmap.fromImage(self.bg))


        # 当前手势
        self.label1 = QLabel(self)
        ## 设置标签的左边距，上边距，宽，高
        self.label1.setGeometry(QRect(420, 20, 90, 20))
        ## 设置文本标签的字体和大小，粗细等
        self.label1.setFont(QtGui.QFont("Roman times", 10))
        self.label1.setText("当前手势")
        ## 显示手势 
        self.labeltext1 = QLabel(self)
        self.labeltext1.setGeometry(QRect(420, 40, 160, 60))
        self.labeltext1.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext1.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")

        
        # 指尖坐标
        self.label2 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label2.setGeometry(QRect(420, 120, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label2.setFont(QtGui.QFont("Roman times", 10))
        self.label2.setText("指尖坐标")
        # 添加设置一个文本框
        self.labeltext2 = QLabel(self)
        self.labeltext2.setGeometry(QRect(420, 140, 160, 60))
        self.labeltext2.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext2.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 光标坐标
        self.label3 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label3.setGeometry(QRect(420, 220, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label3.setFont(QtGui.QFont("Roman times", 10))
        self.label3.setText("光标坐标")
        # 添加设置一个文本框
        self.labeltext3 = QLabel(self)
        self.labeltext3.setGeometry(QRect(420, 240, 160, 60))
        self.labeltext3.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext3.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 准确率
        self.label4 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label4.setGeometry(QRect(420, 320, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label4.setFont(QtGui.QFont("Roman times", 10))
        self.label4.setText("待选文本框")
        # 添加设置一个文本框
        self.text4 = QTextEdit(self)
        self.text4.setGeometry(QRect(420, 340, 160, 60))
        self.text4.setLineWrapMode(True)
        

        # 日志
        self.label5 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label5.setGeometry(QRect(20, 420, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label5.setFont(QtGui.QFont("Roman times", 10))
        self.label5.setText("日志打印")
        # 添加设置一个文本框
        self.text5 = QTextEdit(self)
        self.text5.setGeometry(QRect(20, 440, 560, 140))
        self.text5.setLineWrapMode(True)


        # 输入文本框
        self.text6 = QTextEdit(self)
        # 调整文本框的位置大小
        self.text6.setGeometry(QRect(20, 610, 140, 50))
        self.text6.setLineWrapMode(True)
        self.text6.setText("1812050129-王浩-基于视觉手势识别的交互系统")


        # OPEN按钮
        self.btn1 = QPushButton(self)
        self.btn1.setGeometry(QRect(180, 610, 120, 50))
        self.btn1.setText("开始")

        # CLOSE按钮
        self.btn2 = QPushButton(self)
        self.btn2.setGeometry(QRect(320, 610, 120, 50))
        self.btn2.setText("结束")

        # PAUSE按钮
        self.btn3 = QPushButton(self)
        self.btn3.setGeometry(QRect(460, 610, 120, 50))
        self.btn3.setText("暂停")
        self.show()
        

        # 重要
        LOG.log("手势识别系统开启...")
        self.text5.setText(LOG.log_lst)
        # 关闭视频事件
        self.closeEvent = threading.Event()
        self.closeEvent.clear()
        # 暂停事件
        self.pauseEvent = threading.Event()
        self.pauseEvent.clear()
        self.n=0
        self.a=0# a=0表示未启动系统，a=1表示系统已启动
        # 将按钮置灰
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn1.clicked.connect(lambda: self.open(self.label0))
        self.btn2.clicked.connect(self.close)
        self.btn3.clicked.connect(self.pause)
        


    def open(self,label):
        self.a=1
        LOG.log("打开视频...")
        self.text5.setText(LOG.log_lst)
        th = threading.Thread(target=self.display,args=(label,))
        th.start()



    def close(self):
        self.a=0
        LOG.log("关闭视频...")
        self.text5.setText(LOG.log_lst)
        if self.pauseEvent.is_set():
            self.n+=1
            self.pauseEvent.clear()
        self.closeEvent.set()
        reply = QMessageBox.information(self,"提示","是否保存本次录像视频？",
            QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if reply==QMessageBox.Yes:
            MY.number+=1
        else:
            os.remove(MY.video_path+"/"+MY.video_name_type+str(MY.number)+".mp4")

    def pause(self):
        self.n+=1

        if self.n%2==1:
            LOG.log("暂停视频...")
            self.pauseEvent.set()
            self.btn3.setText("继续")
        else:
            LOG.log("继续视频...")
            self.pauseEvent.clear()
            self.btn3.setText("暂停")
        self.text5.setText(LOG.log_lst)



    def display(self,label):
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)
        self.btn3.setEnabled(True)
        # 加载模型
        self.MODEL=Model('./resources/checkpoints/best-10.pt')
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
        fourcc=cv2.VideoWriter_fourcc(*"mp4v")
        out=cv2.VideoWriter(MY.video_path+"/"+MY.video_name_type+str(MY.number)+".mp4",fourcc,10,(380,380))
        
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
            out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
            # 显示视频
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(img))
            self.update()
            cv2.waitKey(1)

            # 将手势识别、指尖检测、光标坐标显示
            self.labeltext1.setText(str(figure_digital))
            self.labeltext2.setText(str(finger_point))
            self.labeltext3.setText(str(screen_point))
            LOG.log(str(figure_digital))
            LOG.log(str(finger_point))
            LOG.log(str(screen_point))


        cv2.destroyAllWindows()
        camera.release()
        self.closeEvent.clear()
        self.pauseEvent.clear()
        self.label0.setPixmap(QPixmap.fromImage(self.bg))
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)





class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = '基于视觉手势识别的交互系统'
        self.left = 100
        self.top = 200
        self.width = 600
        self.height = 720
        self.centerWindow=MainWindow()
        self.setCentralWidget(self.centerWindow)
        self.printer=QPrinter()
        self.menu()
        self.central()

    def central(self):
        # 显示视频
        label0=QLabel()
        label0.setGeometry(QRect(20, 20, 380, 380))
        img=cv2.imread("./resources/imgs/bg.png")
        bg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        label0.setPixmap(QPixmap.fromImage(bg))


        # 当前手势
        self.label1 = QLabel(self)
        ## 设置标签的左边距，上边距，宽，高
        self.label1.setGeometry(QRect(420, 20, 90, 20))
        ## 设置文本标签的字体和大小，粗细等
        self.label1.setFont(QtGui.QFont("Roman times", 10))
        self.label1.setText("当前手势")
        ## 显示手势 
        self.labeltext1 = QLabel(self)
        self.labeltext1.setGeometry(QRect(420, 40, 160, 60))
        self.labeltext1.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext1.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")

        
        # 指尖坐标
        self.label2 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label2.setGeometry(QRect(420, 120, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label2.setFont(QtGui.QFont("Roman times", 10))
        self.label2.setText("指尖坐标")
        # 添加设置一个文本框
        self.labeltext2 = QLabel(self)
        self.labeltext2.setGeometry(QRect(420, 140, 160, 60))
        self.labeltext2.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext2.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 光标坐标
        self.label3 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label3.setGeometry(QRect(420, 220, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label3.setFont(QtGui.QFont("Roman times", 10))
        self.label3.setText("光标坐标")
        # 添加设置一个文本框
        self.labeltext3 = QLabel(self)
        self.labeltext3.setGeometry(QRect(420, 240, 160, 60))
        self.labeltext3.setFont(QtGui.QFont("Roman times", 10))
        self.labeltext3.setStyleSheet("QLabel{background:white;}"
            "QLabel{color:rgb(100,100,100,250);font-size:20px;qproperty-alignment:AlignCenter;font-family:Roman times;}"
            "QLabel:hover{color:rgb(100,100,100,120);}")
        

        # 准确率
        self.label4 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label4.setGeometry(QRect(420, 320, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label4.setFont(QtGui.QFont("Roman times", 10))
        self.label4.setText("待选文本框")
        # 添加设置一个文本框
        self.text4 = QTextEdit(self)
        self.text4.setGeometry(QRect(420, 340, 160, 60))
        self.text4.setLineWrapMode(True)
        

        # 日志
        self.label5 = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.label5.setGeometry(QRect(20, 420, 90, 20))
        # 设置文本标签的字体和大小，粗细等
        self.label5.setFont(QtGui.QFont("Roman times", 10))
        self.label5.setText("日志打印")
        # 添加设置一个文本框
        self.text5 = QTextEdit(self)
        self.text5.setGeometry(QRect(20, 440, 560, 140))
        self.text5.setLineWrapMode(True)


        # 输入文本框
        self.text6 = QTextEdit(self)
        # 调整文本框的位置大小
        self.text6.setGeometry(QRect(20, 610, 140, 50))
        self.text6.setLineWrapMode(True)
        self.text6.setText("1812050129-王浩-基于视觉手势识别的交互系统")


        # OPEN按钮
        self.btn1 = QPushButton(self)
        self.btn1.setGeometry(QRect(180, 610, 120, 50))
        self.btn1.setText("开始")

        # CLOSE按钮
        self.btn2 = QPushButton(self)
        self.btn2.setGeometry(QRect(320, 610, 120, 50))
        self.btn2.setText("结束")

        # PAUSE按钮
        self.btn3 = QPushButton(self)
        self.btn3.setGeometry(QRect(460, 610, 120, 50))
        self.btn3.setText("暂停")


    def menu(self):
        #设置窗体标题
        self.setWindowTitle(self.title)
        #设置几何位置以及形状
        self.setGeometry(self.left, self.top, self.width, self.height)


        # 子菜单通过addMenu（name）添加
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('文件')
        editMenu = mainMenu.addMenu('编辑')
        viewMenu = mainMenu.addMenu('视图')
        videoMenu = mainMenu.addMenu('视频')
        helpMenu = mainMenu.addMenu('帮助')


        #创建一个action(行为)，标题为"exti"， self 为parent
        exitButton = QAction(self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('退出当前应用')
        exitButton.setText("退出")
        fileMenu.addAction(exitButton)
        exitButton.triggered.connect(self.close)
        

        rebootButton = QAction(self)
        rebootButton.setShortcut('Ctrl+R')
        rebootButton.setStatusTip('重启软件')
        rebootButton.setText("重启")
        fileMenu.addAction(rebootButton)
        rebootButton.triggered.connect(self.rebootWindow)

        pageButton = QAction(self)
        pageButton.setShortcut('Ctrl+P')
        pageButton.setStatusTip('简单调整打印页面')
        pageButton.setText("页面设置")
        fileMenu.addAction(pageButton)
        pageButton.triggered.connect(self.onFilePageSetup)

        printButton = QAction(self)
        printButton.setShortcut('Ctrl+p')
        printButton.setStatusTip('打印日志内容')
        printButton.setText("打印日志")
        fileMenu.addAction(printButton)
        printButton.triggered.connect(self.onFilePrint)

        newWindowButton = QAction(self)
        newWindowButton.setShortcut('N')
        newWindowButton.setStatusTip('新窗口')
        newWindowButton.setText("新窗口")
        fileMenu.addAction(newWindowButton)
        newWindowButton.triggered.connect(self.newWindow)


        # editMenu
        preferButton = QAction(self)
        preferButton.setShortcut('p')
        preferButton.setStatusTip('首选项')
        preferButton.setText("首选项")
        editMenu.addAction(preferButton)
        preferButton.triggered.connect(self.preference)

        # viewMenu
        fullButton = QAction(self)
        fullButton.setShortcut('F')
        fullButton.setStatusTip('全屏')
        fullButton.setText("全屏")
        viewMenu.addAction(fullButton)
        fullButton.triggered.connect(self.fullScreen)

        restoreButton = QAction(self)
        restoreButton.setShortcut('S')
        restoreButton.setStatusTip('恢复')
        restoreButton.setText("恢复")
        viewMenu.addAction(restoreButton)
        restoreButton.triggered.connect(self.restore)

        hideStatusButton = QAction(self)
        hideStatusButton.setStatusTip('状态栏隐藏显示')
        hideStatusButton.setText("隐藏状态栏")
        viewMenu.addAction(hideStatusButton)
        hideStatusButton.setCheckable(True)
        hideStatusButton.triggered.connect(lambda: self.hideStatusBar(hideStatusButton))
        

        # videoMenu
        playBackButton = QAction(self)
        playBackButton.setShortcut('O')
        playBackButton.setStatusTip('播放回放')
        playBackButton.setText("回放")
        videoMenu.addAction(playBackButton)
        playBackButton.triggered.connect(self.playBack)
        

        # helpMenu
        shortcutButton = QAction(self)
        shortcutButton.setShortcut('K')
        shortcutButton.setStatusTip('快捷键详情')
        shortcutButton.setText("快捷键")
        helpMenu.addAction(shortcutButton)
        shortcutButton.triggered.connect(self.shortcutInfo)

        aboutButton = QAction(self)
        aboutButton.setShortcut('A')
        aboutButton.setStatusTip('关于系统')
        aboutButton.setText("关于系统")
        helpMenu.addAction(aboutButton)
        aboutButton.triggered.connect(self.about)
        
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        # self.statusBarInit()
        self.show()

    def statusBarInit(self):
        # 实时时间
        statusBar_1 = QLabel('{:<}'.format(''))
        statusBar_2 = QLabel('{:<}'.format(''))
        self.statusBar_3 = QLabel('{:<}'.format(''))
        self.statusBar_4 = QLabel('{:>}'.format(''))
        self.statusBar.addWidget(statusBar_1, 1)
        self.statusBar.addWidget(statusBar_2, 1)
        self.statusBar.addWidget(self.statusBar_3, 1)
        self.statusBar.addWidget(self.statusBar_4, 1)
        th=threading.Thread(target=self.showTime,args=(self.statusBar_4,))
        th.start()

    def showTime(self,label):
        print(self.statusBar_4.text())
        while not self.isHidden():
            local_time=time.localtime()
            format_now = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            label.setText(format_now)

    def hideStatusBar(self,btn):
        if btn.isChecked():
            self.statusBar.hide()
        else:
            self.statusBar.show()


    def rebootWindow(self):
        self.reboot_window=App()
        self.reboot_window.show()
        self.close()


    def newWindow(self):
        self.new_window=App()
        self.new_window.show()


    def preference(self):
        self.preference_window=PreferenceWindow("首选项")
        self.preference_window.show()


    def fullScreen(self):
        self.resize(1920,1080)
    

    def restore(self):
        self.resize(self.width,self.height)


    def playBack(self):
        self.playBack_window = TabWindow("回放窗口")
        self.playBack_window.show()


    def shortcutInfo(self):
        self.shortcutInfo_window=ShowWindow("快捷方式")
        self.shortcutInfo_window.show()


    def about(self):
        url = 'https://balaa.gitee.io/posts/20211231/'
        webbrowser.open_new_tab(url)


    def msgCritical(self, strInfo):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Critical)
        dlg.setText(strInfo)
        dlg.show()
        

    def onFileOpen(self):
        path,_ = QFileDialog.getOpenFileName(self, '打开文件', '', '文本文件 (*.txt)')
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.msgCritical(str(e))
            else:
                self.path = path
                self.centerWindow.text5.setPlainText(text)
    

    def onFilePageSetup(self):
        dlgPageSetup = QPageSetupDialog(self.printer, self)
        dlgPageSetup.exec()
        

    def onFilePrint(self):
        dlgPrint = QPrintDialog(self.printer, self)
        if QDialog.Accepted == dlgPrint.exec():
            self.centerWindow.text5.print(self.printer)




class ShowWindow(QWidget):
    def __init__(self,title):
        super(ShowWindow, self).__init__()
        x,y=pyautogui.position()
        self.setGeometry(x,y,400,400)
        # self.resize(400,400)
        self.setWindowTitle(title)

        h_layout=QHBoxLayout()
        h1_layout=QHBoxLayout()
        h2_layout=QHBoxLayout()
        
        # 快捷键
        v11_layout=QVBoxLayout()
        v12_layout=QVBoxLayout()
        v11_layout.addWidget(QLabel("Ctrl+p"))
        v11_layout.addWidget(QLabel("Ctrl+r"))
        v11_layout.addWidget(QLabel("Ctrl+P"))
        v11_layout.addWidget(QLabel("N"))
        v11_layout.addWidget(QLabel("Ctrl+Q"))
        v11_layout.addWidget(QLabel("O"))
        v12_layout.addWidget(QLabel("打印"))
        v12_layout.addWidget(QLabel("重启"))
        v12_layout.addWidget(QLabel("页面设置"))
        v12_layout.addWidget(QLabel("新建窗口"))
        v12_layout.addWidget(QLabel("退出"))
        v12_layout.addWidget(QLabel("回放"))
        h1_layout.addLayout(v11_layout)
        h1_layout.addLayout(v12_layout)

        # 快捷键
        v21_layout=QVBoxLayout()
        v22_layout=QVBoxLayout()
        v21_layout.addWidget(QLabel("P"))
        v21_layout.addWidget(QLabel("F"))
        v21_layout.addWidget(QLabel("S"))
        v21_layout.addWidget(QLabel("K"))
        v21_layout.addWidget(QLabel("A"))
        v21_layout.addWidget(QLabel(""))
        v22_layout.addWidget(QLabel("首选项"))
        v22_layout.addWidget(QLabel("全屏"))
        v22_layout.addWidget(QLabel("恢复"))
        v22_layout.addWidget(QLabel("快捷键"))
        v22_layout.addWidget(QLabel("关于"))
        v22_layout.addWidget(QLabel(""))
        h2_layout.addLayout(v21_layout)
        h2_layout.addLayout(v22_layout)
        
        h_layout.addLayout(h1_layout)
        h_layout.addLayout(h2_layout)
        

        v2_layout=QVBoxLayout()
        h_layout.addLayout(v2_layout)
        self.setLayout(h_layout)
        
        


    
class PreferenceWindow(QWidget):
    def __init__(self,title):
        super(PreferenceWindow, self).__init__()
                # 添加窗口标题
        self.setWindowTitle(title)
        # 将窗口设置为动图大小
        x,y=pyautogui.position()
        self.move(x,y)

        self.list = QListWidget()
        self.list.setMaximumWidth(100)

        # 设置列表内容（stack的索引）
        self.list.insertItem(0, '通用')
        self.list.insertItem(1, '编辑器')
        self.list.insertItem(2, '视频')

        # 创建三个stack页面
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        # 分别加载三个Stack的内容
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        # 将三个stack页面加入stackWidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.addWidget(self.stack1)
        self.stackWidget.addWidget(self.stack2)
        self.stackWidget.addWidget(self.stack3)

        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addWidget(self.stackWidget)
        self.setLayout(hbox)

        # 为List绑定事件，当条目改变时，切换stack（重要）
        self.list.currentRowChanged.connect(self.stackSwitch)



    def stack1UI(self):
        layout = QFormLayout()
        # 光标计算模式
        male_rb = QRadioButton("映射式")
        female_rb = QRadioButton("模拟式")
        h_layout = QHBoxLayout()
        h_layout.addWidget(male_rb)
        h_layout.addWidget(female_rb)
        layout.addRow("光标计算模式: ",h_layout)



        self.stack1.setLayout(layout)

    def getFont(self):
        font,ok=QFontDialog.getFont()
        if ok:
            MY.font=font

    def stack2UI(self):
        layout = QFormLayout()
        # 字体选择
        fontChoose=QPushButton("字体选择器")
        fontChoose.clicked.connect(self.getFont)
        layout.addRow(fontChoose)
        self.stack2.setLayout(layout)


    def stack3UI(self):
        # 表单样式
        layout = QFormLayout()
        # 回放保存路径
        layout.addRow(QLabel("默认保存路径:"))
        h_layout = QHBoxLayout()
        # 文本框
        path_text=QLineEdit("路径")
        # 按钮
        path_choose=QPushButton("选择路径")
        path_choose.clicked.connect(lambda: self.selectPath(path_text))
        h_layout.addWidget(path_text)
        h_layout.addWidget(path_choose)
        layout.addRow(h_layout)

        # 命名格式
        layout.addRow(QLabel("命名格式:"))
        h_layout = QHBoxLayout()
        # 文本框
        nameType=QLineEdit("playback-%y%m%H%m.mp4")
        # 按钮
        nameTypeBtn=QPushButton("确认")
        nameTypeBtn.clicked.connect(lambda: self.confirmNameType(nameType))
        h_layout.addWidget(nameType)
        h_layout.addWidget(nameTypeBtn)
        layout.addRow(h_layout)


        self.stack3.setLayout(layout)
    
    def confirmNameType(self,textEdit):
        nameType=textEdit.text()
        MY.video_name_type=nameType

    def selectPath(self,textEdit):
        directory = QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        MY.video_path=directory
        textEdit.setText(MY.video_path)

    # 切换list时触发槽函数切换Stack
    def stackSwitch(self, index):
        self.stackWidget.setCurrentIndex(index)



# 回放窗口
class TabWindow(QTabWidget):  #继承标签页类

    def __init__(self,title):
        super(TabWindow, self).__init__()
        self.setWindowTitle(title)
        # 标签页大小设置
        x,y=pyautogui.position()
        self.setGeometry(x,y,380,460)
        # self.resize(380, 460) 
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

        # 实例化一个标签
        self.tab1 = QWidget()
        self.addTab(self.tab1, '选择回放视频')

        # 给该标签添加选项列表
        label=QLabel("请从下面列表中选择出需要回放的视频：",self.tab1)
        label.setGeometry(10,10,380,50)
        self.listCom = QListWidget(self.tab1)
        self.listCom.setGeometry(10,60,360,330)
        # 选项列表元素为videopath下的mp4文件
        mp4_lst = os.listdir(MY.video_path)
        for item in mp4_lst:
            if ".mp4" in item:
                self.listCom.addItem(item)
        # 添加双击事件
        self.listCom.doubleClicked.connect(self.newTab)
        self.clipImage=None

    def newTab(self):
        # 取出列表中当前选中元素
        item = self.listCom.currentItem()
        # 新建标签页，用于显示视频
        tab = QWidget()
        self.addTab(tab, item.text())

        # 新建label用于显示视频
        label = QLabel(tab)
        # 暂停关闭按钮
        pauseBtn = QPushButton("Pause", tab)
        closeBtn=QPushButton("Close",tab)
        pauseBtn.setCheckable(True)
        closeBtn.setCheckable(True)
        pauseBtn.move(10,385)
        closeBtn.move(280,385)

        th = threading.Thread(target=self.display, args=(
            label,
            item.text(),
            pauseBtn,
            closeBtn,
        ))
        th.start()

    def openMenu(self,position):
        print("label")
        menu = QMenu(self)
        quitAction = QAction("复制图像",menu)
        saveAction=QAction("保存图像",menu)
        menu.addAction(quitAction)
        menu.addAction(saveAction)
        
        action=menu.exec_(QCursor.pos())
        if action is None:
            return
        if action.text()=="复制图像":
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(QPixmap.fromImage(self.clipImage))
            print("COPY")
        if action.text()=="保存图像":
            file_name,_ = QFileDialog.getSaveFileName(self,"save file dialog","/home/balaa/")
            print(file_name)
            self.clipImage.save(file_name,"jpg")
            print("SAVE")
        

    def closeTab (self, currentIndex):
        currentQWidget = self.widget(currentIndex)
        currentQWidget.deleteLater()
        self.removeTab(currentIndex)


    def display(self, label, mp4_file, pausebtn,closebtn):
         # 右键菜单
        label.setContextMenuPolicy(Qt.CustomContextMenu)
        label.customContextMenuRequested.connect(self.openMenu)

        video = cv2.VideoCapture(MY.video_path +"/"+ mp4_file)

        while not self.isHidden():
            # 读取视频
            ret, frame = video.read()
            if not ret:
                break
            # 关闭按钮按下
            if closebtn.isChecked():
                closebtn.toggle()
                break
            # 暂停按钮按下
            if  pausebtn.isChecked():
                while  pausebtn.isChecked():
                    if closebtn.isChecked():
                        pausebtn.toggle()
                        break
                    continue
            
            frame = cv2.resize(frame, (380, 380))
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.clipImage=img
            label.setPixmap(QPixmap.fromImage(img))
            sleep(0.1)

        label.setAlignment(Qt.AlignCenter)
        label.setText("视频播放完毕")

