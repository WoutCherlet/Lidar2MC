import anvil
import os
import argparse
import time
import utils

import open3d as o3d
import numpy as np


MIN_Y = -64
MAX_Y = 320

def voxelize(args, resolution=1.0):

    pc = o3d.io.read_point_cloud(args.pointcloud)

    # Translate to 0,0,0
    min_bounds = pc.get_min_bound()
    pc = pc.translate(np.negative(min_bounds-resolution/2))

    # TODO: switch to custom voxelisation
    voxelgrid = o3d.geometry.VoxelGrid.create_from_point_cloud(pc, voxel_size=resolution)

    return voxelgrid

def draw_voxels(args, voxelgrid):

    region = anvil.EmptyRegion(0, 0)

    planks = anvil.Block('minecraft','oak_planks')

    # clear region
    region = utils.clear_region(0, 0)
            
    # draw voxelgrid with chunk buffer
    X_BUF = 16
    Z_BUF = 16
    # info: mapping of real world coordinates to mc: x -> x, y -> -z, z -> y
    for voxel in voxelgrid.get_voxels():
        idx = voxel.grid_index
        region.set_block(planks, idx[0] + X_BUF, idx[2]-63, idx[1] + Z_BUF)

    # Save to a file
    file = args.world+"\\region\\r.0.0.mca"

    region.save(file)
    return    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--world", type=str, required=True)
    parser.add_argument("-p", "--pointcloud", type=str, required=True)
    parser.add_argument("-o", "--occupation_file", type=str, required=True)
    parser.add_argument("-r", "--resolution", type=float, default=None)

    args = parser.parse_args()


    # check if path is actual mc world
    if not (os.path.exists(args.world + "/region")):
        print("Error: no Minecraft world found at given path")
        print("To start a new world, create it in minecraft first, then provide the path to the savefile")
        print("Savefiles can normally be found at C:\\Users\<user>\Appdata\Roaming\.minecraft\saves")
        os._exit(1)
    
    if not (os.path.exists(args.pointcloud)):
        print("Error: pointcloud not found at given path")
        os._exit(1)

    if not (os.path.exists(args.occupation_file)):
        print(f"Couldn't find occupation file at {args.occupation_file}, quitting")
        print(f"Create new occupation file?")
        # TODO: read in new occu file name with resolution etc.
        return

    print("Voxelizing pointcloud")
    voxels = voxelize(args, resolution=args.resolution)
    
    print("Drawing voxels in minecraft")
    draw_voxels(args, voxels)
    return

if __name__ == "__main__":
    main()