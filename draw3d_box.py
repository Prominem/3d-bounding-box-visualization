import numpy as np
import math

def get_origin_vertices(box_paras):
    '''
    functions: get vertices referred to the origin, ordered by octant
    inputs:
    box_paras: shape = (3,), dx,dy,dz
    returns:
    vertices: shape = (8,3), x,y,z
    '''
    dx, dy, dz = box_paras
    vertices = np.zeros((8, 3))
    vertices[0, :] = [dx / 2, dy / 2, dz / 2]
    vertices[1, :] = [-dx / 2, dy / 2, dz / 2]
    vertices[2, :] = [-dx / 2, -dy / 2, dz / 2]
    vertices[3, :] = [dx / 2, -dy / 2, dz / 2]
    vertices[4, :] = [dx / 2, dy / 2, -dz / 2]
    vertices[5, :] = [-dx / 2, dy / 2, -dz / 2]
    vertices[6, :] = [-dx / 2, -dy / 2, -dz / 2]
    vertices[7, :] = [dx / 2, -dy / 2, -dz / 2]

    return vertices

def draw_or_lines(vertices, pts_stride):
    '''
    get lines from vertices referred to origin
    inputs:
    vertices: shape=(8, 3), x,y,z, ordered by octant
    pts_stride: float, stride of discrete points
    returns:
    box_points: shape=(n, 3), x,y,z
    '''
    line21 = []
    x_node = vertices[1, 0]
    while x_node <= vertices[0, 0]:
        line21.append([x_node, vertices[0, 1], vertices[0, 2]])
        x_node += pts_stride
    line21 = np.array(line21)  # (n, 3)

    line34 = line21.copy()
    line34[:, 1] *= -1

    line65 = line21.copy()
    line65[:, 2] *= -1

    line78 = line34.copy()
    line78[:, 2] *= -1

    line32 = []
    y_node = vertices[2, 1]
    while y_node <= vertices[1, 1]:
        line32.append([vertices[1, 0], y_node, vertices[1, 2]])
        y_node += pts_stride
    line32 = np.array(line32)  # (n, 3)

    line41 = line32.copy()
    line41[:, 0] *= -1

    line76 = line32.copy()
    line76[:, 2] *= -1

    line85 = line41.copy()
    line85[:, 2] *= -1

    line51 = []
    z_node = vertices[4, 2]
    while z_node <= vertices[0, 2]:
        line51.append([vertices[0, 0], vertices[0, 1], z_node])
        z_node += pts_stride
    line51 = np.array(line51)

    line62 = line51.copy()
    line62[:, 0] *= -1

    line73 = line62.copy()
    line73[:, 1] *= -1

    line84 = line51.copy()
    line84[:, 1] *= -1  # (n, 3)

    line1 = np.array([line21, line34, line65, line78])
    line2 = np.array([line32, line41, line76, line85])
    line3 = np.array([line51, line62, line73, line84])
    line1 = np.concatenate(line1, axis=0)  # (n, 3)
    line2 = np.concatenate(line2, axis=0)
    line3 = np.concatenate(line3, axis=0)
    line = np.concatenate((line1, line2), axis=0)  # (n, 3)
    line = np.concatenate((line, line3), axis=0)  # (n, 3)

    return line



def generate_per_box(box_paras, pts_stride):
    '''
    inputs:
    box_paras: shape=(8,), x,y,z,dx,dy,dz,theta,class
    pts_stride: float, stride of discrete points
    returns:
    box_points:shape=(n,4), x,y,z,class
    '''
    or_vertices = get_origin_vertices(box_paras[3:6])
    # (8, 3), vertices ordered by octant, box placed at origin without rotate
    or_box_points = draw_or_lines(or_vertices, pts_stride)  # (n, 3), discrete points alone the box
    theta = box_paras[6] % (2*np.pi)
    R = np.array([[math.cos(theta), math.sin(theta), 0.0], [-math.sin(theta), math.cos(theta), 0.0], [0.0, 0.0, 1.0]])
    # rotate the box
    or_r_box_points = np.matmul(or_box_points, R)  # (n, 3)
    # translate the box
    r_t_box_points = or_r_box_points + box_paras[:3]  # (n, 3)
    box_points = np.concatenate((r_t_box_points, np.ones((r_t_box_points.shape[0], 1))*box_paras[-1]), axis=-1)  # (n, 4)

    return box_points

def generate_3d_box(box_paras, pts_stride):
    '''
    inputs:
    box_paras:shape=(n, 8), x,y,z,dx,dy,dz,theta,class
    pts_stride: float, stride of discrete points
    theta：radian，float； class: digit
    returns:
    box_points:shape=(n2,4), x,y,z,class
    '''
    box_points = None
    for i in range(box_paras.shape[0]):
        per_box_paras = box_paras[i, :]  # (8,)
        per_box_points = generate_per_box(per_box_paras, pts_stride)  # (n3, 4), x,y,z,class
        if box_points is None:
            box_points = per_box_points
        else:
            box_points = np.concatenate((box_points, per_box_points), axis=0)

    return box_points
