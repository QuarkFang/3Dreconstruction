import numpy as np
import cv2
import sift
import surf
import RANSAC
import time
import RTMatrix

timeStart = time.time()
# 读入图像
image1 = cv2.imread("3.tif")
image2 = cv2.imread("4.tif")
image1 = cv2.resize(image1, (1000, 720))
image2 = cv2.resize(image2, (1000, 720))
# sift、surf + KDTree
sift_pts = sift.sift(image1, image2)
surf_pts = surf.surf(image1, image2)
pts = sift_pts + surf_pts
# pts使用RANSAC, 返回RANSAC后的匹配点、本征矩阵、R、t矩阵
pts, essentialMat, R, t = RANSAC.compute(pts)
# 透视变换并保存
# image3 = cv2.warpPerspective(image1, M, (1000, 720))
# cv2.imwrite("warpPerspective.tif", image3)
# 水平拼接
image = np.hstack((image1, image2))
# 显示匹配线段
sift.show_line(image, pts)
timeEnd = time.time()
cv2.waitKey()
time = timeEnd - timeStart
print("耗时:" + str(time) + "s")
