from packages.Import import *


class Mouse():
    def __init__(self,duration=0) -> None:
        pyautogui.FAILSAFE =False  
        x,y=pyautogui.position()
        self.x=x
        self.y=y
        self.duration=duration
        self.moveTo(x,y)
    
    def moveToByDirect(self,direction,displacement):
        if direction=='left':
            self.x-=displacement
        elif direction=='top':
            self.y-=displacement
        elif direction=='right':
            self.x+=displacement
        elif direction=='bottom':
            self.y+=displacement
        else:
            logger.info("请输入正确方向。")
            return
        pyautogui.moveTo(self.x,self.y,self.duration)
        
    def moveTo(self,x,y):
        self.setMousePos(x,y)
        pyautogui.moveTo(self.x,self.y,self.duration)
    
    def getMousePos(self):
        return self.x,self.y
    
    def setMousePos(self,x,y):
        self.x,self.y=x,y

    # 单击左键
    def leftClick(self):
        pyautogui.click(self.x,self.y,button='left')
    # 双击左键
    def leftDoubleClick(self):
        pyautogui.doubleClick(self.x,self.y)
    # 单击右键
    def rightClick(self):
        pyautogui.click(self.x,self.y,button='right')
    # 双击右键
    def rightDoubleClick(self):
        pyautogui.rightClick(self.x,self.y)
    # 按下
    def down(self):
        pyautogui.mouseDown()
    # 释放
    def up(self):
        pyautogui.mouseUp()
    # 滚动
    def scrool(self):
        pyautogui.scroll()



        

class Keyboard():
    def __init__(self) -> None:
        pass
    

            

# 创建对象
MOUSE=Mouse()