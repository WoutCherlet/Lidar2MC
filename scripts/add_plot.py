import os
import argparse
import json
import math as m

import sys
sys.path.insert(1, r'C:\Users\cherl\Documents\Lidar2MC')

from lidar2mc.pc_io import read_point_cloud
from lidar2mc.voxelization import VoxelGrid
from lidar2mc.layout import layout_plot


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-w", "--world", type=str, required=True)
    parser.add_argument("-i", "--world_info", type=str, required=True)
    parser.add_argument("-p", "--pointcloud", type=str, required=True)

    args = parser.parse_args()

    # check if path is actual mc world
    # if not (os.path.exists(args.world + "/region")):
    #     print("Error: no Minecraft world found at given path")
    #     print("To start a new world, create it in minecraft first, then provide the path to the savefile")
    #     print("Savefiles can normally be found at C:\\Users\<user>\Appdata\Roaming\.minecraft\saves")
    #     os._exit(1)
    
    if not (os.path.exists(args.world_info)):
        print(f"world_info file {args.world_info} does not exist, exiting.")
        os._exit(1)

    if not (os.path.exists(args.pointcloud)):
        print(f"pointcloud file {args.pointcloud} does not exist, exiting.")
        os._exit(1)

    with open(args.world_info) as f:
        world_info = json.load(f)


    world_path = world_info["world_path"]

    if not os.path.exists(world_path):
        print("Couldn't find mc world path")
        print("Trying in default location")

        m_world_name = world_info["m_world_name"]
        default_path = os.path.join(os.environ['USERPROFILE'], "Appdata", "Roaming", ".minecraft", "saves", m_world_name)

        if not os.path.exists(default_path):
            print("Default path also not found, exiting")
            os._exit(1)
        else:
            world_path = default_path

    
    # TODO: check if leaf-wood seperated? do this in here?
    # for now, assume it is or neglect
            
    # read point cloud
    pointcloud = read_point_cloud(args.pointcloud)

    # voxelize
    resolution = world_info["voxelsize"]
    vxlgrid = VoxelGrid(pointcloud, resolution=resolution, min_points_per_voxel=50)
    # vxlgrid.plot()

    # layout new plot on world
    layout_loc_x, layout_loc_z = layout_plot(world_info, vxlgrid)

    print(layout_loc_x, layout_loc_z)

    # TODO: add world in mc
    add_world_mc(layout_loc, vxlgrid)






        




    return

if __name__ == "__main__":
    main()