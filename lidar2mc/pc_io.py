import open3d as o3d

def read_txt_file(path):
    points = []
    labels = []
    with open(path, 'r') as f:
        for line in f.readlines():
            els = line.split(' ')
            points.append([float(els[0]), float(els[1]), float(els[2])])
            labels.append(int(float(els[3].replace("\n", ""))))
    
    device = o3d.core.Device("CPU:0")

    pcd = o3d.t.geometry.PointCloud(device)

    pcd.point.positions = o3d.core.Tensor(points, o3d.core.float32, device)

    pcd.point.semantic = o3d.core.Tensor(labels, o3d.core.int32, device)

    return pcd

def read_ply_file(path, label_name=None):
    
    pcd = o3d.t.read_point_cloud(path)

    # convert custom label_name to standard semantic field
    if label_name is not None:
        pcd.point.semantic = pcd.point[label_name]
        del pcd.point[label_name]
