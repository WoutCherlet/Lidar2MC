## Lidar2MC

Tool to create minecraft worlds from point clouds.
Tested using Minecraft 1.19 and using .ply files.

### Dependencies:
- Custom anvil parser using: https://github.com/WoutCherlet/anvil-parser
- Open3d


### TODO's:
#### Layout
Use some form of grid selector (search for library), to layout new plots into the world
Should keep track of reserved/occupied space, and probably some title/description per plot to indicate what is there
Probably would be nice to have spaces dedicated to certain forest types

#### Tree design

- Use FSCT or some other tool to get leaf-wood-ground seperation and use appropriate mc blocks.
- Give certain forest type for new plots, and use appropriate mc wood type (and biome!)

#### anvil-parser-package
- Encode and decode biomes is not implemented yet
- Additional functionality?