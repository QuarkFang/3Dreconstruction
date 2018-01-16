import numpy as np
import cv2
import sift
import surf
import RANSAC
import time
import sfm
import save
import os
import RTMatrix

timeStart = time.time()
# 读入图像
image1 = cv2.imread("3.tif")
image2 = cv2.imread("4.tif")
image1 = cv2.resize(image1, (1000, 750))
image2 = cv2.resize(image2, (1000, 750))
# sift、surf + KDTree
sift_pts = sift.sift(image1, image2)
surf_pts = surf.surf(image1, image2)
pts = sift_pts + surf_pts
# pts使用RANSAC, 返回RANSAC后的匹配点、本征矩阵、R、t矩阵、匹配点以及相机内参
pts, essentialMat, R, t, src_pts, dst_pts, K = RANSAC.compute(pts)
# 透视变换并保存
# image3 = cv2.warpPerspective(image1, M, (1000, 720))
# cv2.imwrite("warpPerspective.tif", image3)
points4D = sfm.triangulate_compute(R, t, src_pts, dst_pts, K)
# 水平拼接
image = np.hstack((image1, image2))
# 存储点云信息
save.save_data(image1, src_pts, R, t, points4D)
# 显示匹配线段
sift.show_line(image, pts)
timeEnd = time.time()
cv2.waitKey()
time = timeEnd - timeStart
print("耗时:" + str(time) + "s")
# 显示点云
os.system('show')
