import numpy as np
import cv2

E = np.mat([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
W1 = np.mat([[0, -1, 0], [1, 0, 0], [0, 0, 1]])   # Rz(+pi/2)
W2 = np.mat([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])   # Rz(-pi/2)


def resolve(mat):
    U, sigma, VT = np.linalg.svd(mat)
    T = U * W1 * E * U.T
    R = U * W1.T * VT

    return T, R
