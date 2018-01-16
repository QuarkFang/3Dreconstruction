import numpy as np
import cv2
import math

# 相机内参
K = np.mat([[818.793, 0, 501.999],
            [0, 817.801, 374.818],
            [0, 0, 1]])
'''
[ 818.793  0  501.999;  0  817.801  374.818;  0  0  1 ]
'''


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
    # 奇异值分解使本征矩阵秩为2
    U, sigma, VT = np.linalg.svd(essentialMat)
    sigma = np.mat([[sigma[0], 0, 0], [0, sigma[1], 0], [0, 0, 0]])
    essentialMat = U * sigma * VT
    # 恢复R、t值
    parameters = cv2.recoverPose(essentialMat, src_pts, dst_pts, K)
    R = parameters[1]
    t = parameters[2]

    # 返回本征矩阵
    return pts, essentialMat, R, t, src_pts, dst_pts, K


def delete_RANSAC(x, y):
    if y:
        return x


# 需要修改
'''
def find_right_Rt(R1, R2, t, x=1, y=1, z=1):
    r, jacobian= cv2.Rodrigues(R2)
    print(r)
    if x * t[0] > 0:
        return t, R2
    else:
        return -t, R2
'''