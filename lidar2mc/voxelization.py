from collections import Counter

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


class VoxelNode:
    def __init__(self, grid_index) -> None:
        self.points = []
        self.labels = []
        self.grid_index = grid_index # grid_index = (x,y,z)
        self.n_points = 0

    def add_point(self, point, label=None):
        self.points.append(point)
        self.n_points += 1
        if label is not None:
            self.labels.append(label)

    def get_voxel_label(self):
        # return most common label, if draw it returns a random one
        if len(self.labels) > 0:
            return Counter(self.labels).most_common(1)[0][0]
        return None



class VoxelGrid:
    def __init__(self, pointcloud : o3d.t.geometry.PointCloud, resolution, min_points_per_voxel=1) -> None:
        self.min_points = min_points_per_voxel

        pts_np = pointcloud.point.positions.numpy()
        try:
            labels = pointcloud.point.labels.numpy()
            self.labels_present = True
        except:
            print("No labels found")
            self.labels_present = False

        # get max and min bounds of pointcloud, calculate amount of bins in each dimension and init 3D voxel array

        max_bounds = pointcloud.get_max_bound().numpy()
        min_bounds = pointcloud.get_min_bound().numpy()
        ranges = max_bounds - min_bounds
        self.n_bins = ranges//resolution + 1
        
        # init voxelgrid array
        self.voxel_array = np.array([[[None for _ in range(int(self.n_bins[2]))] for _ in range(int(self.n_bins[1]))] for _ in range(int(self.n_bins[0]))])

        for i, point in enumerate(pts_np):
            idxs = (point - min_bounds) // resolution
            idxs = tuple(idxs.astype(int))

            if self.voxel_array[idxs] is None:
                self.voxel_array[idxs] = VoxelNode(idxs)
            if self.labels_present:
                self.voxel_array[idxs].add_point(point, label=labels[i])
            else:
                self.voxel_array[idxs].add_point(point)

        for index in np.ndindex(self.voxel_array.shape):
            if self.voxel_array[index] and self.voxel_array[index].n_points < self.min_points:
                self.voxel_array[index] = None

    def get_voxels(self):
        return self.voxel_array[self.voxel_array != np.array(None)]

    def plot(self):
        # plot using matplotlib

        # construct color array
        if self.labels_present:
            colors = np.empty(self.voxel_array.shape, dtype=object)
            colormap = {1: 'brown', 0: 'green'}
            for index in np.ndindex(self.voxel_array.shape):
                if self.voxel_array[index]:
                    label = self.voxel_array[index].get_voxel_label()
                    if label is not None:
                        colors[index] = colormap[label]
        else:
            colors = "green"

        boolean_voxels = self.voxel_array != None
        
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(boolean_voxels, facecolors=colors, edgecolor='k')
        ax.set_aspect('equal')

        plt.show()

def read_txt_file(path):
    points = []
    labels = []
    with open(path, 'r') as f:
        for line in f.readlines():
            els = line.split(' ')
            points.append([float(els[0]), float(els[1]), float(els[2])])
            labels.append(int(float(els[3].replace("\n", ""))))
    
    device = o3d.core.Device("CPU:0")

    pcd = o3d.t.geometry.PointCloud(device)

    pcd.point.positions = o3d.core.Tensor(points, o3d.core.float32, device)

    pcd.point.labels = o3d.core.Tensor(labels, o3d.core.int32, device)

    return pcd


def test_voxels(pc):
    vxlgrid = VoxelGrid(pc, resolution=0.5, min_points_per_voxel=50)

    vxlgrid.plot()

if __name__ == "__main__":
    # text file with labels
    test_path = r"C:\Users\wcherlet\OneDrive - UGent\data\singletrees\separated\dro_033_pc.txt"
    pc = read_txt_file(test_path)

    # ply file
    # test_path = r"C:\Users\wcherlet\OneDrive - UGent\data\singletrees\wytham_winter_5a.ply"
    # pc = o3d.t.io.read_point_cloud(test_path)


    test_voxels(pc)