import os
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--world", type=str, required=True)
    parser.add_argument("-", "--world_info", type=str, required=True)
    parser.add_argument("-p", "--pointcloud", type=str, required=True)

    args = parser.parse_args()

    # check if path is actual mc world
    if not (os.path.exists(args.world + "/region")):
        print("Error: no Minecraft world found at given path")
        print("To start a new world, create it in minecraft first, then provide the path to the savefile")
        print("Savefiles can normally be found at C:\\Users\<user>\Appdata\Roaming\.minecraft\saves")
        os._exit(1)
    
    if not (os.path.exists(args.world_info)):
        print(f"world_info file {args.world_info} does not exist, exiting.")
        os._exit(1)

    if not (os.path.exists(args.pointcloud)):
        print(f"pointcloud file {args.pointcloud} does not exist, exiting.")
        os._exit(1)
    
    # steps to add new plot:

    # read in point cloud
    # read in resolution from world_info file
    # voxelize point cloud and create plotinfo
    # init selector window
    # get location and render in minecraft.

    with open(args.world_info) as f:
        data = json.load(f)

    resolution = data["resolution"]
    print(resolution)

    return

if __name__ == "__main__":
    main()