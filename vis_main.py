from draw3d_box import *
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, 'data')
vis_dir = os.path.join(BASE_DIR, 'vis')
if not os.path.exists(vis_dir):
    os.makedirs(vis_dir)
scene = '005050'
box_name = scene + '_bbox.npy'
pts_name = scene + '_pc.npz'
box_dir = os.path.join(data_dir, box_name)
pts_dir = os.path.join(data_dir, pts_name)
out_box_dir = os.path.join(vis_dir, scene+'_box.txt')
out_pts_dir = os.path.join(vis_dir, scene+'_pts.txt')
points = np.load(pts_dir)['pc']  # (n, 6)
box_paras = np.load(box_dir)  # (n, 8)
box_paras[:, 3:6] *= 2
box_points = generate_3d_box(box_paras, 0.01)
np.savetxt(out_box_dir, box_points)
np.savetxt(out_pts_dir, points)
