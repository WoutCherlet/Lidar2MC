import anvil

MIN_Y = -64
MAX_Y = 320

def clear_chunk(region, x, z, bedrock=True):
    """
    Clears chunk into all air with optional bottom layer of bedrock

    Parameters
    ----------
    region
        region in which to clear chunk
    x
        Region x
    z
        Region z
    """
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

def get_region(x, z):
    """
    Returns x,z of region that coordinates fall in

    Parameters
    ----------
    x_coord
        Absolute x coordinate
    z_coord
        Absolute z coordinate
    """

    return (x // 512), (z // 512)

def get_chunk(x, z):
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

if __name__ == "__main__":
    # quick tests
    assert (get_chunk(-1,-1) == (31,31))
    assert (get_chunk(1,1) == (0,0))
    assert(get_chunk(32, 54) == (2,3))
    assert(get_chunk(-512, -16) == (0,31))