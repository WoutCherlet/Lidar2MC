import anvil
import os
import argparse

import lidar2mc.world_io as world_io

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

def draw_voxels(worldfile, voxelgrid):

    region = anvil.EmptyRegion(0, 0)

    planks = anvil.Block('minecraft','oak_planks')

    # clear region
    region = world_io.clear_region(0, 0)


    # TODO: draw in actual region file
            
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