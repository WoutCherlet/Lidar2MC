## Lidar2MC

Tool to create minecraft worlds from point clouds.
Tested using Minecraft 1.19 and using .ply files.

### Dependencies:
- Custom anvil parser using: https://github.com/WoutCherlet/anvil-parser
- Open3d
- simple_3dviz
- matplotlib
- Pillow


### TODO's:
#### Tree design

- Use FSCT or some other tool to get leaf-wood-ground seperation and use appropriate mc blocks.
- Give certain forest type for new plots, and use appropriate mc wood type (and biome!)

#### anvil-parser
- x and z detection from file seems broken