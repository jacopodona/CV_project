import time
import numpy as np
import matplotlib.pyplot as plt
from optitrack.geometry import *


#######################################----- INITIALIZATION ------#######################################
#
# Select choosen joint from the 21 body parts
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
    bones_pos = [bones_pos[i] for i in b]
    return bones_pos


def get_joint_pos(bodies, take):
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
# Take the positions of all the marker and
# extract only the chosen one
#
    # remove NoneType object (Truncation)
    lambda_obj = lambda x: (x is not None)
    tmp = list(filter(lambda_obj, bones_pos[marker]))

    # find the path
    path = np.transpose(tmp)

    # Compute time vector from frame rate   
    sample = 1/take.frame_rate
    time = np.arange(0, (len(path[0])*sample) - sample/2, sample)
    return [path[2], path[0], path[1]], time        # reorder the points in [x, y, z] from [y, z, x]

#######################################----- PATH PLOT -----#######################################

def plot_marker_path_2D(marker_pos, ax, frame, plot = "xy"):
#
#   plot marker path on planes: "xy" - "xz" - "yz"
#   
    start = 100     # start after 100 frame to reduce initial noise
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
    ax.plot3D(marker_pos[0][0:frame],marker_pos[1][0:frame], marker_pos[2][0:frame])
        

#######################################----- TRAJECTORY PLOT -----#######################################

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

#######################################----- 3D SKELETON -----#######################################

def plot_3d_joints(joints, ax, frame):
#
#   Plot 3D point plot is parametric with frame istance
#
    # plot the hip
    if(joints[0][frame]!= None):
        ax.scatter(joints[0][frame][2], joints[0][frame][0], joints[0][frame][1])

    # plot the lower body
    points_of_interest=[0,13,14,15,16,17,18,19,20]  # joints id of hip and lower body
    for i in points_of_interest:    # Plot all lower body
        if(joints[i][frame] != None):
            ax.scatter(joints[i][frame][2], joints[i][frame][0], joints[i][frame][1])


def plot_3d_line(ax, first, second, color):
#
# Plots a 3d line between two 3d points
#
    x=[first[2], second[2]]
    y=[first[0], second[0]]
    z=[first[1], second[1]]
    ax.plot(x, y, z, color)


def plot_3d_skeleton(joints, ax, frame, color):
    #
    # Plot all points
    #
        plot_3d_joints(joints, ax, frame)
        # Plot edge connections
        body_edges = [[0, 1], [0, 13], [13, 14], [14, 15],[0, 16], [16, 17], [17, 18], [18, 20], [15, 19]]
        for joint1,joint2 in body_edges:
            if (joints[joint1][frame]!=None and joints[joint2][frame]!=None):
                plot_3d_line(ax,joints[joint1][frame],joints[joint2][frame],color)
      