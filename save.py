import numpy as np

def flatten(arg):
    flattened = []

    if arg[0] is float:
        return arg

    for i in arg:
        flattened.extend(i)

    return flattened


def fake_cv_mat(mat, f):
    print("""   - !!opencv-matrix
      rows: {}
      cols: {}
      dt: d
      data: {}""".format(len(mat),len(mat[0]),flatten(mat.tolist())), file=f)

def save_data(image, src_pts, R, t, points4D):
    f = open("./viewer/structure.yml","w")
    print("%YAML:1.0", file=f)
    print("Camera Count: {}".format(2),file=f)
    print("Point Count: {}".format(len(points4D)),file=f)

    print("Rotations:",file=f)
    fake_cv_mat(np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]),f)
    fake_cv_mat(R,f)

    print("Motions:",file=f)
    fake_cv_mat(np.array([[0.], [0.], [0.]]),f)
    fake_cv_mat(t,f)


    pointcolorpairs = []
    for i in range(0, len(points4D)):
        try:
            pointcolorpair = [', '.join(map(str,points4D[i])), ', '.join([str(color) for color in image[int(src_pts[i][1])][int(src_pts[i][0])]])]
            pointcolorpairs.append(pointcolorpair)
        except IndexError:
            print("Bad point: {}".format(src_pts[i]))
            pass

    print("Points:",file=f)
    for i in pointcolorpairs:
        print("  - [{}]".format(i[0]), file=f)
    print("Colors:",file=f)
    for i in pointcolorpairs:
        print("  - [{}]".format(i[1]),file=f)