import cv2
import numpy as np
import kdtree


# 读入图像
def sift(image1, image2):
    # image1 = cv2.resize(image1, (1000, 720))
    # image2 = cv2.resize(image2, (1000, 720))
    # 获取关键点信息
    # keypoints --> kp; descriptors --> dsp; location --> loc;
    kp1, dsp1, loc1 = compute(image1)
    kp2, dsp2, loc2 = compute(image2)
    # 特征点匹配
    # result = match_sift(loc1, loc2, dsp1, dsp2, 0.6)
    result = kdtree.KDTree_match(loc1, loc2, dsp1, dsp2, 0.6)
    # 水平拼接
    # image = np.hstack((image1, image2))
    # 显示匹配线段
    # show_line(image, result)

    return result


# 计算特征点
def compute(image):
    sift = cv2.xfeatures2d.SIFT_create()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    keypoints = sift.detect(gray, None)
    descriptors = sift.compute(gray, keypoints)
    location = cv2.KeyPoint_convert(keypoints)

    return keypoints, descriptors, location


# 显示特征点
def show_keypoints(image, keypoints, descriptors):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.drawKeypoints(gray, keypoints, image)
    cv2.imshow("img", img)
    cv2.waitKey(0)


# 显示匹配线段
def show_line(image, result):
    for i in range(len(result)):
        if result[i] is not None:
            cv2.line(image, (result[i][0], result[i][1]), (int(result[i][2] + 1000), result[i][3]), (255, 0, 0), 1)
    # 将关键点在图像上显示
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.imshow("test", image)


# 特征点匹配
def match_sift(location1, location2, descriptors1, descriptors2, DR=0.6):
    loc = []
    for i in range(len(location1)):
        l1 = 10000
        l2 = 10000
        for j in range(len(location2)):
            length = distance(descriptors1[1][i], descriptors2[1][j])
            if length < l1:
                l1 = length
                location2_l1 = j
            elif length < l2:
                l2 = length
        if l1 / l2 < DR:
            loc.append([round(location1[i][0]), round(location1[i][1]), round(location2[location2_l1][0]),
                        round(location2[location2_l1][1])])
            print([[l1, l2]])
        if i % 100 == 0:
            print(str(i) + "/" + str(len(location1)))

    print(loc)
    return loc


# 计算距离
def distance(a, b):
    dis = np.linalg.norm(a - b)

    return dis
