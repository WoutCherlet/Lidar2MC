from typing import Union

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
        if label:
            self.labels.append(label)

    def get_voxel_label(self, labelname):
        pass
        # check if labelname exists for points, then return most common one/ average?



class VoxelGrid:
    def __init__(self, pointcloud : o3d.t.geometry.PointCloud, resolution, min_points_per_voxel=1) -> None:
        self.min_points = min_points_per_voxel

        pts_np = pointcloud.point.positions.numpy()

        # get max and min bounds of pointcloud, calculate amount of bins in each dimension and init 3D voxel array

        max_bounds = pointcloud.get_max_bound().numpy()
        min_bounds = pointcloud.get_min_bound().numpy()
        ranges = max_bounds - min_bounds
        self.n_bins = ranges//resolution + 1
        
        # init voxelgrid array

        self.voxel_array = np.array([[[None for _ in range(int(self.n_bins[2]))] for _ in range(int(self.n_bins[1]))] for _ in range(int(self.n_bins[0]))])

        # TODO: parallelize with numpy ? smarter way to do this: first do count, some map reduce type structure?

        for point in pts_np:
            idxs = (point - min_bounds) // resolution
            idxs = tuple(idxs.astype(int))

            if self.voxel_array[idxs] is None:
                self.voxel_array[idxs] = VoxelNode(idxs)
            self.voxel_array[idxs].add_point(point)

        for index in np.ndindex(self.voxel_array.shape):
            if self.voxel_array[index] and self.voxel_array[index].n_points < self.min_points:
                self.voxel_array[index] = None

    def get_voxels(self):
        # create list of only occupied voxel
        pass

    def plot(self):
        # plot using matplotlib

        boolean_voxels = self.voxel_array != None
        
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(boolean_voxels, edgecolor='k')
        ax.set_aspect('equal')

        plt.show()


def test_voxels(path):
    pc = o3d.t.io.read_point_cloud(path)

    vxlgrid = VoxelGrid(pc, resolution=0.5, min_points_per_voxel=100)

    vxlgrid.plot()


if __name__ == "__main__":
    test_path = r"C:\Users\wcherlet\OneDrive - UGent\data\singletrees\wytham_winter_5a.ply"
    test_voxels(test_path)