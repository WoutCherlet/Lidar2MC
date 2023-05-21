import anvil
import os

MIN_Y = -64
MAX_Y = 320

class PlotInfo:
    def __init__(self, name, x, z, x_length, z_length, description, type):
        self.name = name
        self.x = x
        self.z = z
        self.x_length = x_length
        self.z_length = z_length
        self.description = description
        self.type = type
        self.rotated = False

    def rotate(self):
        self.rotated = not self.rotated
        tmp = self.x_length
        self.x_length = self.z_length
        self.z_length = tmp

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

    chunk = anvil.EmptyChunk(x, z)
    
    bedrock = anvil.Block('minecraft','bedrock')

    for y in range(-3, 20):
        chunk.add_section(anvil.EmptySection(y)) # will init empty section as None blocks which is same as air
    if bedrock:
        btm = anvil.EmptySection(-4)
        for i in range(16):
            for j in range(16):
                btm.set_block(bedrock, i, 0, j)
        chunk.add_section(btm)
    else:
        chunk.add_section(anvil.EmptySection(-4))
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

def get_region(x, z, chunk=False):
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

def get_chunk_within_region(x, z):
    """
    Returns x,z of chunk that coordinates fall in

    Parameters
    ----------
    x_coord
        Absolute x coordinate
    z_coord
        Absolute z coordinate
    """
    x_reg, z_reg = get_region(x,z)

    return ((x-x_reg*512) // 16), ((z - z_reg*512) // 16)

def get_chunk_absolute(x,z):
    """
    Returns x,z of chunk that coordinates fall in

    Parameters
    ----------
    x_coord
        Absolute x coordinate
    z_coord
        Absolute z coordinate
    """
    return x // 16, z // 16

def flatten_chunk(region,x,z):
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

    chunk = region.get_chunk(x, z)

    for y in range(0, 20):
        chunk.add_section(anvil.EmptySection(y), replace = True) # will init empty section as None blocks which is same as air

    dirt = anvil.Block('minecraft', 'dirt')
    for i in range(16):
        for j in range(16):
            chunk.set_block(dirt, i, -1, j)
    return region

def flatten_region(world_dir, x,z):
    regionfile = f"r.{x}.{z}.mca"

    regionfile = os.path.join(world_dir, "region", regionfile)

    region = anvil.Region.from_file(regionfile)

    for i in range(x*32+32):
        for j in range(z*32+32):
            flatten_chunk(region, i, j)
    
    return region


if __name__ == "__main__":
    # quick tests
    assert (get_chunk_within_region(-1,-1) == (31,31))
    assert (get_chunk_within_region(1,1) == (0,0))
    assert(get_chunk_within_region(32, 54) == (2,3))
    assert(get_chunk_within_region(-512, -16) == (0,31))