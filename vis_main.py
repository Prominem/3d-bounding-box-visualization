from draw3d_box import *
import numpy as np
# **********************main*********************
folder_dir = 'D:\\study\\python_codes\\data\\sunrgbd\\'
scene = '005050'
box_name = scene + '_bbox.npy'
box_dir = folder_dir + box_name
box_paras = np.load(box_dir)  # (n, 8)
box_paras[:, 3:6] *= 2
box_points = generate_3d_box(box_paras, 0.01)
out_dir = folder_dir +scene + '_bbox.txt'
np.savetxt(out_dir, box_points)