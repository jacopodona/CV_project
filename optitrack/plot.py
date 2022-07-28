import open3d as o3d
import time
import numpy as np
import matplotlib.pyplot as plt
from optitrack.geometry import *

###----- INITIALIZATION ------###

def get_bone_pos(bodies, take):
#
# Get the marker positions from the bodies and the time stamp
#
    bones_pos = []
    if len(bodies) > 0:
        for body in bodies: 
            bones = take.rigid_bodies[body]
            bones_pos.append(bones.positions)   # take position of each body part
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

def plot_marker_path_2D(marker_pos, plot = "xy"):
#
#   plot marker path on planes: "xy" - "xz" - "yz"
#
    if plot == "xz":
        plt.plot(marker_pos[0], marker_pos[2])
    if plot == "yz":
        plt.plot(marker_pos[1], marker_pos[2])
    if plot == "xy":
        plt.plot(marker_pos[0], marker_pos[1])


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

def plot_marker_traj(marker_pos, t, plot = "x"):
#
#   plot axle trajectory:
#   "x" = x- direction
#   "y" = y- direction
#   "z" = z- direction
#
    if plot=="x":
        plt.plot(t, marker_pos[0])
    if plot=="y":
        plt.plot(t, marker_pos[1])
    if plot=="z":
        plt.plot(t, marker_pos[2])   
      