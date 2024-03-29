import os
import argparse
import json

import sys
# sys.path.insert(1, r'C:\Users\wcherlet\OneDrive - UGent\Documents\Lidar2MC')
sys.path.insert(1, r'C:\Users\cherl\Documents\Lidar2MC')

from lidar2mc.layout import PlotInfo

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--world", type=str, required=True)
    parser.add_argument("-o", "--out_dir", type=str, required=True)
    parser.add_argument("-r", "--resolution", type=float, required=True)

    args = parser.parse_args()

    # check if path is actual mc world
    if not (os.path.exists(args.world + "/region")):
        print("Error: no Minecraft world found at given path")
        print("To start a new world, create it in minecraft first, then provide the path to the savefile")
        print("Savefiles can normally be found at C:\\Users\<user>\Appdata\Roaming\.minecraft\saves")
        os._exit(1)
    
    if not (os.path.exists(args.out_dir)):
        print("output directory does not exist, exiting.")
        os._exit(1)
    
    worldname = os.path.basename(args.world)

    print(f"Creating new world_info file and reserving region 0,0 for world {worldname}.")

    base_plot = PlotInfo("base_plot", -16, -16, 16, 16, "Center base", "/")

    plots_list = [base_plot.__dict__]

    world_base_name = os.path.basename(args.world)

    dict = {"voxelsize": args.resolution, "m_world_name": world_base_name, "world_path": args.world, "plots": plots_list}
    with open( os.path.join(args.out_dir, f"{worldname}.json") , "w" ) as f:
        json.dump(dict, f)

    return

if __name__ == "__main__":
    main()