import anvil
import os
import math as m

MIN_Y = -64
MAX_Y = 320

VERSION = 2731 # version number of mc to get newest version behaviour in anvil

def clear_chunk(region, x, z, bedrock=True):
    """
    Clears chunk into all air with optional bottom layer of bedrock

    Parameters
    ----------
    region
        region of chunk
    x
        Chunk x
    z
        Chunk z
    """
    if not region.inside(x,0,z,chunk=True):
        print("Attempting to clear chunk in region where it is not located")
        return

    # init empty chunk
    chunk = anvil.Chunk(nbt_data=None, x=x, z=z, version=VERSION)
    

    for y in range(-3, 20):
        chunk.add_section(anvil.Section(data=None, chunk_version=VERSION, y=y)) # will init empty section as None blocks which is same as air
    if bedrock:
        bedrock_blk = anvil.Block('minecraft','bedrock')
        btm = anvil.Section(data=None, chunk_version=VERSION, y=-4)
        for i in range(16):
            for j in range(16):
                btm.set_block(bedrock_blk, i, 0, j)
        chunk.add_section(btm)
    else:
        chunk.add_section(anvil.Section(data=None, chunk_version=VERSION, y=-4))
    region.add_chunk(chunk)
    return region

def clear_region(x,z, bedrock=True):
    """
    Returns region with all chunks turned into air with optional layer of bedrock below it

    Parameters
    ----------
    x
        Region x
    z
        Region z
    """

    region = anvil.EmptyRegion(x,z)

    for i in range(x*32+32):
        for j in range(z*32+32):
            clear_chunk(region, i, j, bedrock=bedrock)

    return region

def get_region_xz(x, z, chunk=False):
    """
    Returns x,z of region that coordinates fall in

    Parameters
    ----------
    x_coord
        x coordinate
    z_coord
        z coordinate
    chunk
        whether coordinates are chunk x,z or absolute x,z
    """
    if chunk:
        return (x // 32), (z // 32)
    else:
        return (x // 512), (z // 512)

def get_chunk_xz_within_region(x, z):
    """
    Returns local (within-region) chunk coordinates that global coordinates fall in

    Parameters
    ----------
    x_coord
        Absolute x coordinate
    z_coord
        Absolute z coordinate
    """
    x_reg, z_reg = get_region_xz(x,z)

    return ((x-x_reg*512) // 16), ((z - z_reg*512) // 16)

def get_chunk_xz_absolute(x,z):
    """
    Returns global x,z chunk coordinates that coordinates fall in

    Parameters
    ----------
    x_coord
        Absolute x coordinate
    z_coord
        Absolute z coordinate
    """
    return x // 16, z // 16



def add_world_mc(world_path, layout_loc, voxelgrid):

    # TODO: read appropriate region instead of empty region

    # TODO: fix this so it works for plots spanning borders of regions
    region_x, region_z = get_region_xz(*layout_loc, chunk=True)

    file = world_path+f"\\region\\r.{region_x}.{region_z}.mca"
    print(file)

    if not os.path.exists(file):
        print(f"INFO: region file {file} not found, creating empty region")
        region = anvil.EmptyRegion(region_x, region_z)
    else: 
        region = anvil.Region.from_file(file)

    vxlgrid_dims = voxelgrid.get_dimensions()
    chunk_x_range = range(layout_loc[0], layout_loc[0] + m.ceil(vxlgrid_dims[0] / 16))
    chunk_z_range = range(layout_loc[1], layout_loc[1] + m.ceil(vxlgrid_dims[1] / 16))

    print("Clearing chunks")

    for chunk_x in chunk_x_range:
        for chunk_z in chunk_z_range:
            clear_chunk(region, chunk_x, chunk_z)

    print("Adding voxelgrid")

    # TODO: wood and leaves based on forest type
    # wood = anvil.Block('minecraft','log')
    # leaves = anvil.Block('minecraft', 'leaves')

    # # info: mapping of real world coordinates to mc: x -> x, y -> -z, z -> y
    # for voxel in voxelgrid.get_voxels():
    #     idx = voxel.grid_index
    #     if voxel.get_voxel_label() == 1:
    #         block = wood
    #     else:
    #         block = leaves
    #     region.set_block(block, layout_loc[0]+idx[0], idx[2]-63, layout_loc[1]+idx[1])

    print("saving world file")

    # Save to a file
    file = world_path+f"\\region\\r.{region_x}.{region_z}.mca"

    region.save(file)

    return


if __name__ == "__main__":
    # quick tests
    assert (get_chunk_xz_within_region(-1,-1) == (31,31))
    assert (get_chunk_xz_within_region(1,1) == (0,0))
    assert(get_chunk_xz_within_region(32, 54) == (2,3))
    assert(get_chunk_xz_within_region(-512, -16) == (0,31))