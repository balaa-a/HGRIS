from gui.Gui import *

if __name__ == '__main__':
    logger.add("./log/log.txt")
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())