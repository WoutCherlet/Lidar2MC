


class VoxelNode:
    def __init__(self) -> None:
        pass

    def add_points(self, point):
        pass
        # definition of point?

    def get_voxel_label(self, labelname):
        pass
        # check if labelname exists for points, then return most common one/ average?



class VoxelGrid:
    def __init__(self, pointcloud, resolution) -> None:
        pass
        # get pointcloud dimensions
        # init 3D array of voxelnodes
        # for each point: bin into appropriate voxelnode

