import anvil

MIN_Y = -64
MAX_Y = 320

def clear_chunk(region, x, z):
    air = anvil.Block('minecraft','air')
    bedrock = anvil.Block('minecraft','bedrock')

    # TODO: refactor: just init all regions manually

    for i in range(x*16, x*16+16):
        for j in range(z*16, z*16+16):
            for y in range(MIN_Y+1, MAX_Y):
                region.set_block(air, i, y, j)
            region.set_block(bedrock, i, -64, j)
    return region


def clear_region(x,z):

    # TODO: empty an entire region so it can be built on with voxelgrid
    # need to do this with smarter way then using set_block as it will be slow

    return