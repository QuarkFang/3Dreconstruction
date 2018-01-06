import numpy as np
import cv2

def compute(pts):
    src_pts = np.array(pts)[:, 0:2]
    dst_pts = np.array(pts)[:, 2:4]
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 6.0)
    matchesMask = mask.ravel().tolist()
    pts = list(map(delete_RANSAC, pts, matchesMask))

    return pts


def delete_RANSAC(x, y):
    if y:
        return x