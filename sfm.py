import numpy as np
import cv2


def triangulate_compute(R, t, projPoints1, projPoints2, K, projMatr1=None):
    if projMatr1 is None:
        projMatr1 = np.mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    print(R, t)
    projMatr2 = projMatr1 * np.mat(inhomogeneous_to_homogeneous(np.column_stack((R, t))))
    print(projMatr2)
    # projMatr2 = homogeneous_to_inhomogeneous(projMatr2)
    points4D = []

    for i in range(len(projPoints1)):
        inhomoCoordinate = cv2.triangulatePoints(K * projMatr1, K * projMatr2, projPoints1[i], projPoints2[i])
        homoCoordinate = np.delete((inhomoCoordinate / inhomoCoordinate[3]), 3, 0)
        homoCoordinate = np.reshape(homoCoordinate, -1, 3)
        points4D.append(homoCoordinate)
    print(points4D)

    return points4D


def inhomogeneous_to_homogeneous(mat):
    a = [0, 0, 0, 1]
    result = np.row_stack((mat, a))

    return result


def homogeneous_to_inhomogeneous(mat):
    result = np.delete(mat, 3, axis=0)
    return result