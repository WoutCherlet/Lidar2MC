import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from collections import Counter
from simple_3dviz import Mesh, Lines
from simple_3dviz.window import show

from lidar2mc.pc_io import read_txt_file


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
        self.resolution = resolution
        self.pointcloud = pointcloud

        pts_np = pointcloud.point.positions.numpy()
        try:
            labels = pointcloud.point.semantic.numpy()
            self.labels_present = True
        except:
            print("No labels found")
            self.labels_present = False

        # get max and min bounds of pointcloud, calculate amount of bins in each dimension and init 3D voxel array

        max_bounds = pointcloud.get_max_bound().numpy()
        min_bounds = pointcloud.get_min_bound().numpy()
        ranges = max_bounds - min_bounds
        self.n_voxels = ranges//resolution + 1
        
        # init voxelgrid array
        self.voxel_array = np.array([[[None for _ in range(int(self.n_voxels[2]))] for _ in range(int(self.n_voxels[1]))] for _ in range(int(self.n_voxels[0]))])

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
    
    def get_dimensions(self):
        return self.n_voxels

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
    
    def show(self):
        min_bounds = self.pointcloud.get_min_bound().numpy()/10
        max_bounds = self.pointcloud.get_max_bound().numpy()/10

        if self.labels_present:
            colors = np.empty(self.voxel_array.shape + (3,), dtype=object)
            colormap = {1: (0.6, 0.3, 0), 0: (0, 1, 0)}
            for index in np.ndindex(self.voxel_array.shape):
                if self.voxel_array[index]:
                    label = self.voxel_array[index].get_voxel_label()
                    if label is not None:
                        colors[index] = colormap[label]
        else:
            colors = (1, 0, 0)


        boolean_voxels = self.voxel_array != None

        # m = Mesh.from_voxel_grid(voxels=boolean_voxels, colors=colors, bbox=[[0,0,0], max_bounds-min_bounds], sizes = [self.resolution/10, self.resolution/10, self.resolution/10])
        m = Mesh.from_voxel_grid(voxels=boolean_voxels, colors=colors)
        l = Lines.from_voxel_grid(voxels=boolean_voxels, colors=(0, 0, 0.), width=0.01)
        show([m,l])




def test_voxels(pc):
    vxlgrid = VoxelGrid(pc, resolution=0.5, min_points_per_voxel=50)

    vxlgrid.show()

if __name__ == "__main__":
    # text file with labels
    test_path = r"C:\Users\cherl\OneDrive - UGent\data\singletrees\separated\dro_034_pc.txt"
    pc = read_txt_file(test_path)

    # ply file
    # test_path = r"C:\Users\wcherlet\OneDrive - UGent\data\singletrees\wytham_winter_5a.ply"
    # pc = o3d.t.io.read_point_cloud(test_path)
    test_voxels(pc)
