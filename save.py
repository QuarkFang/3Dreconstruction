class SaveSession:
    # def __init__(self):
    #     self.rotation = []
    #     self.motion = []
    #     self.point = []
    #     self.color = []

    def __init__(self, rotation, motion, point, color):
        self.rotation = rotation
        self.motion = motion
        self.point = point
        self.color = color

    # def push(self, img, src_pts, points4D, R = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]), t = np.array([[0.], [0.], [0.]])):
    #     self.rotation.append(R)
    #     self.motion.append(t)
    #
    #     for i in range(0, len(points4D)):
    #         try:
    #             pointcolorpair = [', '.join(map(str, points4D[i])),
    #                               ', '.join([str(color) for color in img[int(src_pts[i][1])][int(src_pts[i][0])]])]
    #             self.point.append(pointcolorpair[0])
    #             self.color.append(pointcolorpair[1])
    #         except IndexError:
    #             print("Bad point: {}".format(src_pts[i]))
    #             pass

    def __flatten(self, arg):
        flattened = []

        if arg[0] is float:
            return arg

        for i in arg:
            flattened.extend(i)

        return flattened

    def __fake_cv_mat(self, mat, f):
        print("""   - !!opencv-matrix
          rows: {}
          cols: {}
          dt: d
          data: {}""".format(mat.shape[0],mat.shape[1],self.__flatten(mat.tolist())), file=f)

    def save(self):
        # BEGIN
        f = open("./viewer/structure.yml","w")
        # Header
        print("%YAML:1.0", file=f)
        print("Camera Count: {}".format(len(self.motion)),file=f)
        print("Point Count: {}".format(sum([len(i) for i in self.point])),file=f)
        # Rotation
        print("Rotations:",file=f)
        for rot in self.rotation:
            self.__fake_cv_mat(rot, f)
        # Motion
        print("Motions:",file=f)
        for mot in self.motion:
            self.__fake_cv_mat(mot, f)
        # Point
        print("Points:",file=f)
        for i in self.point:
            for j in i:
                print("  - [{}]".format(", ".join(map(str,j))), file=f)
        # Color
        print("Colors:",file=f)
        for i in self.color:
            for j in i:
               print("  - [{}]".format(", ".join(map(str,j))),file=f)
        # DONE
        f.close()