from packages.Import import *


class HandExtract:

    def __init__(self) -> None:
        pass

    def EllipseDetect(self, src: ndarray):
        '''
        描述：椭圆法肤色检测；
        参数：源图像,接收到的应该是1:1的图像；
        返回：仅包含肤色部分的图像，其余部分全部黑色；
        '''
        h,w,_=src.shape
        # 预处理，缩小原图像，使得更快处理
        src=cv2.resize(src,(112,112))

        # 使用一副图像存储椭圆，内部1,外部0
        skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)
        cv2.ellipse(skinCrCbHist, (113, 155), (23, 15), 43, 0, 360, (255, 255, 255), -1)

        # 将原图像转换到ycrcb色彩空间
        YCRCB = cv2.cvtColor(src, cv2.COLOR_BGR2YCR_CB)
        (y, cr, cb) = cv2.split(YCRCB)
        # skin是肤色的mask
        skin = np.zeros(cr.shape, dtype=np.uint8)
        (x, y) = cr.shape
        for i in range(0, x):
            for j in range(0, y):
                CR = YCRCB[i, j, 1]
                CB = YCRCB[i, j, 2]
                if skinCrCbHist[CR, CB] > 0:
                    skin[i, j] = 255
        
        # 后处理，恢复原图像大小
        skin=cv2.resize(skin,(w,h))
        # skin=cv2.dilate(skin,(5,5))
        skin = cv2.erode(skin,(13,13),iterations = 1)

        return skin


    def CrOtsu(self, img):
        '''
        描述：otsu肤色检测；
        返回：肤色区域二值化图像，肤色区域原图像；
        '''
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

        (y, cr, cb) = cv2.split(ycrcb)
        cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
        _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        dst = cv2.bitwise_and(img, img, mask=skin)
        return skin, dst



    def GetFingerPoint(self, finger_roi_mask):
        '''
        描述：凸包凸缺陷方法指尖检测食指指尖，适用所有手势。传入二值化的感兴趣图像，返回指尖坐标；
        '''
        # 首先对二值化图像模糊，使得更容易识别指尖
        roi = cv2.GaussianBlur(finger_roi_mask, (13, 13), 0)

        # 找到roi图像中所有轮廓
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 取轮廓面积最大的一个，记为手部轮廓
        if len(contours) == 0:
            return None
        else:
            # 自定义max，比较各个contour的面积，返回面积最大的轮廓
            cnt = max(contours, key=cv2.contourArea)

        # 找到手部轮廓凸包
        hull = cv2.convexHull(cnt, returnPoints=False)
        # 找到凸点
        defects = cv2.convexityDefects(cnt, hull)
        if defects is None:
            return None
        # 指尖点坐标并返回
        sidx, eidx, fidx, depth = defects[0, 0]
        figure_point = cnt[sidx][0]

        return figure_point


    def getFingerPointFor1(self,finger_roi_mask):
        '''
        描述：极值方法检测食指指尖，仅适用手势1。
        返回：tuple
        '''
        result=cv2.minMaxLoc(finger_roi_mask)
        # result元祖包含最小值下标、最大值下标、最小值、最大值
        max_point=result[3]
        return max_point


# 创建对象
HANDEXTRACT = HandExtract()
