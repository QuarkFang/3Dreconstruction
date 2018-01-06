import numpy as np
import cv2
import sift
import surf
import RANSAC
import time

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
# pts使用RANSAC
pts = RANSAC.compute(pts)
# 水平拼接
image = np.hstack((image1, image2))
# 显示匹配线段
sift.show_line(image, pts)

timeEnd = time.time()
cv2.waitKey()
time = timeEnd - timeStart
print("耗时:" + str(time) + "s")
