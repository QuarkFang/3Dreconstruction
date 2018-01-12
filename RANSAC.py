import numpy as np
import cv2

# 相机内参‘

K = np.mat([[17.22441, 0, 0],
     [0, 16.53543, 0],
     [0, 0, 1]])

def compute(pts):
    src_pts = np.array(pts)[:, 0:2]
    dst_pts = np.array(pts)[:, 2:4]
    # 计算单应性矩阵
    homographyMat, homographyMask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 6.0)
    matchesMask = homographyMask.ravel().tolist()
    # map返回一个对象
    pts_obj = map(delete_RANSAC, pts, matchesMask)
    pts = list(filter(None, pts_obj))
    src_pts = np.array(pts)[:, 0:2]
    dst_pts = np.array(pts)[:, 2:4]
    # 计算基础矩阵
    # fundamentalMat, fundamentalMask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 6.0)
    # fundamentalMat, fundamentalMask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_8POINT, 6.0)
    # 计算本征矩阵
    essentialMat, essentialMask = cv2.findEssentialMat(src_pts, dst_pts, K)
    parameters = cv2.recoverPose(essentialMat, src_pts, dst_pts, K)
    R = parameters[1]
    t = parameters[2]

    # 返回本征矩阵
    return pts, essentialMat, R, t


def delete_RANSAC(x, y):
    if y:
        return x