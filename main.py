import numpy as np
import cv2
import sift
import surf
import RANSAC
import time
import sfm
import save
import os
import kdtree
import RTMatrix

projMatr = np.mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
RList = []
tList = []
points = []
colors = []
RList.append(projMatr[:, 0:3])
tList.append(projMatr[:, 3:4])
dir = "../test"

def init_photos_reconstruction(dirpath, str1, str2):
    # 读入图像
    image1 = cv2.imread(dirpath + str1)
    image2 = cv2.imread(dirpath + str2)
    # image1 = cv2.resize(image1, (1000, 750))
    # image2 = cv2.resize(image2, (1000, 750))
    # sift、surf + KDTree
    sift_pts = sift.sift(image1, image2)
    surf_pts = surf.surf(image1, image2)
    pts = sift_pts + surf_pts
    # pts使用RANSAC, 返回RANSAC后的匹配点、本征矩阵、R、t矩阵、匹配点以及相机内参
    pts, essentialMat, R, t, src_pts, dst_pts, K = RANSAC.compute(pts)
    # 透视变换并保存
    # image3 = cv2.warpPerspective(image1, M, (1000, 720))
    # cv2.imwrite("warpPerspective.tif", image3)
    global projMatr, RList, tList, points, colors
    points4D, color4D, Mat = sfm.triangulate_compute(projMatr, R, t, src_pts, dst_pts, K, image1)
    projMatr = Mat
    RList.append(projMatr[:, 0:3])
    tList.append(projMatr[:, 3:4])
    points.append(points4D)
    colors.append(color4D)
    # 水平拼接
    # image = np.hstack((image1, image2))
    # 存储点云信息
    # save.save_data(image1, src_pts, R, t, points4D)
    # 显示匹配线段
    # sift.show_line(image, pts)
    # cv2.waitKey()
    # 显示点云
    # os.system('show')

    return dst_pts, points4D


def photos_reconstruction(dirpath, str1, str2, pre_dst_pts, pre_points4D):
    # 读入图像
    image1 = cv2.imread(dirpath + str1)
    image2 = cv2.imread(dirpath + str2)
    # image1 = cv2.resize(image1, (1000, 750))
    # image2 = cv2.resize(image2, (1000, 750))
    # sift、surf + KDTree
    sift_pts = sift.sift(image1, image2)
    surf_pts = surf.surf(image1, image2)
    pts = sift_pts + surf_pts
    # pts使用RANSAC, 返回RANSAC后的匹配点、本征矩阵、R、t矩阵、匹配点以及相机内参
    pts, essentialMat, R, t, src_pts, dst_pts, K = RANSAC.compute(pts)
    src_pts_PnP, src_pts_PnP4D = kdtree.KDTree_match_pre(pre_dst_pts, pre_points4D, src_pts, dst_pts)
    # print(src_pts_PnP, src_pts_PnP4D)
    retval, rvec, t, inliers = cv2.solvePnPRansac(src_pts_PnP4D, src_pts_PnP, K, np.zeros(4), flags=cv2.SOLVEPNP_EPNP, reprojectionError=8.0, confidence=0.99)
    R = cv2.Rodrigues(rvec)[0]
    # 透视变换并保存
    # image3 = cv2.warpPerspective(image1, M, (1000, 720))
    # cv2.imwrite("warpPerspective.tif", image3)
    global projMatr, RList, tList, points, colors
    print(t)
    # print(projMatr[:, 3:4])
    points4D, color4D, Mat = sfm.triangulate_compute_pre(projMatr, R, t, src_pts, dst_pts, K, image1)
    projMatr = Mat
    RList.append(projMatr[:, 0:3])
    tList.append(projMatr[:, 3:4])
    points.append(points4D)
    colors.append(color4D)
    # 水平拼接
    # image = np.hstack((image1, image2))
    # 存储点云信息
    # save.save_data(image1, src_pts, R, t, points4D)
    # 显示匹配线段
    # sift.show_line(image, pts)
    # cv2.waitKey()
    # 显示点云
    # os.system('show')

    return dst_pts, points4D



'''
main函数
'''
timeStart = time.time()


photoList = os.listdir(dir)
dst_pts, points4D = init_photos_reconstruction(dir + "/", photoList[0], photoList[1])
for i in range(1, len(photoList)-1):
    dst_pts, points4D = photos_reconstruction(dir + "/", photoList[i], photoList[i+1], dst_pts, points4D)
timeEnd = time.time()
save.SaveSession(RList, tList, points, colors).save()
os.system("show")

time = timeEnd - timeStart
print("耗时:" + str(time) + "s")


