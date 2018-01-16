import numpy as np
import cv2
import os


def save_data(image, src_pts, R, t, points4D):
    PointCount = len(src_pts)
    K1 = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    K2 = np.array([0., 0., 0.])
    f = open("Viewer/structure.yml", 'w')
    fs = cv2.FileStorage("Viewer/structure.yml", cv2.FILE_STORAGE_WRITE)
    fs.write('Camera Count', 2)
    fs.write('Point Count', PointCount)
    fs.write('Rotations', '[')
    fs['Rotations'] = K1
    '''
    fs.write('', R)
    fs.write('', ']')
    fs.write('Motions', '[')
    fs.write('', K2)
    fs.write('', t)
    fs.write('', ']')
    fs.write('Points', '[')
    for i in range(PointCount):
        fs.write('', str(points4D[i].tolist()))
    fs.write('', ']')
'''
'''
    data1 = {'%YAML':1.0, 'Camera Count': 2, 'Point Count': PointCount}
    data2 = {'Rotations': ['!!opencv-matrix'], 'rows': 3}
    yaml.dump(data2, f, default_flow_style=False)
    f.close()
'''