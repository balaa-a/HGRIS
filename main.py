from gui.Display import *

if __name__=="__main__":
    # 创建应用程序和对象
    app = QtWidgets.QApplication(sys.argv)
    ui = Dispaly()
    sys.exit(app.exec_())