from sklearn.neighbors import KDTree
import sift


def KDTree_match(location1, location2, descriptors1, descriptors2, DR=0.6):
    loc = []
    tree = KDTree(descriptors2[1], leaf_size=128, metric='euclidean')
    for i in range(len(location1)):
        dist, ind = tree.query([descriptors1[1][i]], k=2)
        if dist[0][0] / dist[0][1] < DR:
            loc.append([round(location1[i][0]), round(location1[i][1]), round(location2[ind[0][0]][0]),
                        round(location2[ind[0][0]][1])])

    return loc