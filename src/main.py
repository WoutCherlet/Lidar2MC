import anvil
import os
import argparse
import open3d as o3d
import numpy as np

from utils import clear_chunk

MIN_Y = -64
MAX_Y = 320

def test_read(args):
    file = args.world+"\\region\\r.0.0.mca"

    region = anvil.Region.from_file(file)

    chunk = anvil.Chunk.from_region(region, 0, 0)

    block = chunk.get_block(0, 0, 0)

    print(block) # <Block(minecraft:air)>
    print(block.id) # air
    print(block.properties) # {}
    return 

def test_write(args):
    # Create a new region with the `EmptyRegion` class at 0, 0 (in region coords)
    region = anvil.EmptyRegion(0, 0)

    # Create `Block` objects that are used to set blocks
    stone = anvil.Block('minecraft', 'stone')
    dirt = anvil.Block('minecraft', 'dirt')
    air = anvil.Block('minecraft', 'air')
    
    for y in range(32):
        for z in range(32):
            for x in range(32):
                region.set_block(stone, x, y, z)

    # Save to a file
    file = args.world+"\\region\\r.0.0.mca"

    region.save(file)
    return

def voxelize(args, resolution=1.0):

    pc = o3d.io.read_point_cloud(args.pointcloud)

    # Translate to 0,0,0
    min_bounds = pc.get_min_bound()
    pc = pc.translate(np.negative(min_bounds-resolution/2))

    # TODO: different voxelize method with min amount of points for voxel to be present?
    voxelgrid = o3d.geometry.VoxelGrid.create_from_point_cloud(pc, voxel_size=resolution)

    return voxelgrid


def draw_voxels(args, voxelgrid):

    max_bounds = voxelgrid.get_max_bound()

    region = anvil.EmptyRegion(0, 0)

    planks = anvil.Block('minecraft','oak_planks')
    
    # TODO: support for multiple regions + generic coordinates
    #clear area
    # info: mapping of real world coordinates to mc: x -> x, y -> -z, z -> y
    X_BUF = 16
    Z_BUF = 16
    for z in range(max_bounds[2]//16 + 2):
        for x in range(int(max_bounds[0])//16 + 2):
            clear_chunk(region, x, z)
            
    # draw voxelgrid with chunk buffer
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

    args = parser.parse_args()


    # check if path is actual mc world
    if not (os.path.exists(args.world + "/region")):
        print("Error: no Minecraft world found at given path")
        print("Create a dummy world in minecraft, then provide the path to the savefile")
        print("Savefiles can normally be found at C:\\Users\<user>\Appdata\Roaming\.minecraft\saves")
        os._exit(1)
    
    if not (os.path.exists(args.pointcloud)):
        print("Error: pointcloud not found at given path")
        os._exit(1)

    voxels = voxelize(args, resolution=0.10)

    draw_voxels(args, voxels)

    return

if __name__ == "__main__":
    main()