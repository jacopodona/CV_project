import open3d as o3d
import time
import numpy as np
import matplotlib.pyplot as plt
from optitrack.geometry import *


###----- INITIALIZATION ------###
#
# get choosed joint
#
def get_joints(array, joints, legend):
    tmp = []
    legend_f = []
    for i in range(0, len(joints)):
        if joints[i] == True:
            tmp.append(array[i])
            legend_f.append(legend[i])
    return tmp, legend_f

def get_bone_pos(bodies, take):
#
# Get the marker positions from the bodies and the time stamp
#
    bones_pos = []
    b = [0, 13, 14, 15, 16, 17, 18, 19, 20]
    if len(bodies) > 0:
        for body in bodies: 
            bones = take.rigid_bodies[body]
            bones_pos.append(bones.positions)   # take position of each body part
    bones_pos = [ bones_pos[i] for i in b]
    return bones_pos

def get_marker_path(bones_pos, marker, take):
#
# take the positions of all the marker and
# extract only the chosen one
#
    # remove NoneType object
    lambda_obj = lambda x: (x is not None)
    tmp = list(filter(lambda_obj, bones_pos[marker]))

    # find the path
    path = np.transpose(tmp)

    # Compute time vector from frame rate   
    sample = 1/take.frame_rate
    time = np.arange(0, (len(path[0])*sample) - sample/2, sample)
    return [path[2], path[0], path[1]], time        # reorder the points in [x, y, z] from [y, z, x]

###----- PATH PLOT ------###

def plot_marker_path_2D(marker_pos, ax, frame, plot = "xy"):
#
#   plot marker path on planes: "xy" - "xz" - "yz"
#   
    start = 100
    if plot == "xz":
        ax.plot(marker_pos[0][start:frame], marker_pos[2][start:frame])
    if plot == "yz":
        ax.plot(marker_pos[1][start:frame], marker_pos[2][start:frame])
    if plot == "xy":
        ax.plot(marker_pos[0][start:frame], marker_pos[1][start:frame])


def plot_marker_path_3D(marker_pos, ax, frame = "none"):
#
#   plot 3D path
#   plot is parametric with numeber of frame selected 
#
    if frame == "none":
        frame = len(marker_pos[0])
    if frame <= len(marker_pos[0]):
        ax.plot3D(marker_pos[0][0:frame],marker_pos[1][0:frame], marker_pos[2][0:frame])
    else:
        print("frame selected out of bound, max number is: ", len(marker_pos[0]))
        

###----- TRAJECTORY PLOT ------###

def plot_marker_traj(marker_pos, t, ax, frame, label = "x", reverse_axis = False):
#
#   plot axle trajectory:
#   "x" = x- direction
#   "y" = y- direction
#   "z" = z- direction
#
    start = 100
    if reverse_axis:
        if label=="x":
            ax.plot(marker_pos[0][start:frame], t[start:frame])
        if label=="y":
            ax.plot(marker_pos[1][start:frame], t[start:frame])
        if label=="z":
            ax.plot(marker_pos[2][start:frame], t[start:frame])  
    else:
        if label=="x":
            ax.plot(t[start:frame], marker_pos[0][start:frame])
        if label=="y":
            ax.plot(t[start:frame], marker_pos[1][start:frame])
        if label=="z":
            ax.plot(t[start:frame], marker_pos[2][start:frame]) 
      