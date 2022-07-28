# Load the Rhino API.
# import rhinoscriptsyntax as rs


# Make sure that the Python libraries also contained within this course package
# are on the load path.  This adds the parent folder to the load path, assuming that this
# script is still located with the rhinoscripts/ subfolder of the Python library tree.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import open3d as o3d
import time
import os
import numpy as np
import matplotlib.pyplot as plt

from optitrack.plot import *
# Load the Optitrack CSV file parser module.
import optitrack.csv_reader as csv
from optitrack.geometry import *


## Find the files
# run
dir = os.path.dirname(__file__)
run_1 = os.path.join(dir, 'data/Dona_corsa.csv')
run_2 = os.path.join(dir, 'data/edoardo_corsa.csv')
run_3 = os.path.join(dir, 'data/vittoria_corsa.csv')
run_4 = os.path.join(dir, 'data/sgamb_corsa.csv')
run_5 = os.path.join(dir, 'data/forna_corsa_001.csv')
#run_1 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/Dona_corsa.csv"
#run_2 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/edoardo_corsa.csv"
#run_3 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/vittoria_corsa.csv"
#run_4 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/sgamb_corsa.csv"
#run_5 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/forna_corsa_001.csv"

# walk
walk_1 = os.path.join(dir, 'data/Dona_camminata.csv')
walk_2 = os.path.join(dir, 'data/edoardo_camminata.csv')
walk_3 = os.path.join(dir, 'data/vittoria_camminata.csv')
walk_4 = os.path.join(dir, 'data/sgamb_camminata.csv')
walk_5 = os.path.join(dir, 'data/forna_camminata.csv')
#walk_1 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/Dona_camminata.csv"
#walk_2 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/edoardo_camminata.csv"
#walk_3 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/vittoria_camminata.csv"
#walk_4 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/sgamb_camminata.csv"
#walk_5 = "/home/mmlab/Desktop/CVLaboratories/CV_project/data/forna_camminata.csv"

## Read the files
# run
take_run_1 = csv.Take().readCSV(run_1)
take_run_2 = csv.Take().readCSV(run_2)
take_run_3 = csv.Take().readCSV(run_3)
take_run_4 = csv.Take().readCSV(run_4)
take_run_5 = csv.Take().readCSV(run_5)

# walk
take_walk_1 = csv.Take().readCSV(walk_1)
take_walk_2 = csv.Take().readCSV(walk_2)
take_walk_3 = csv.Take().readCSV(walk_3)
take_walk_4 = csv.Take().readCSV(walk_4)
take_walk_5 = csv.Take().readCSV(walk_5)

# Print out some statistics
print("Found rigid bodies1:", take_run_1.rigid_bodies.keys())
print("Found rigid bodies1:", take_run_2.rigid_bodies.keys())
print("Found rigid bodies1:", take_run_3.rigid_bodies.keys())
print("Found rigid bodies1:", take_run_4.rigid_bodies.keys())
print("Found rigid bodies1:", take_run_5.rigid_bodies.keys())

## Create bodies and process in planes
# run
bodies_run_1 = take_run_1.rigid_bodies
bodies_run_2 = take_run_2.rigid_bodies
bodies_run_3 = take_run_3.rigid_bodies
bodies_run_4 = take_run_4.rigid_bodies
bodies_run_5 = take_run_5.rigid_bodies

# walk
bodies_walk_1 = take_walk_1.rigid_bodies
bodies_walk_2 = take_walk_2.rigid_bodies
bodies_walk_3 = take_walk_3.rigid_bodies
bodies_walk_4 = take_walk_4.rigid_bodies
bodies_walk_5 = take_walk_5.rigid_bodies


## Crete the path ##
#run
pos_run_1 = get_bone_pos(bodies_run_1, take_run_1)
pos_run_2 = get_bone_pos(bodies_run_2, take_run_2)
pos_run_3 = get_bone_pos(bodies_run_3, take_run_3)
pos_run_4 = get_bone_pos(bodies_run_4, take_run_4)
pos_run_5 = get_bone_pos(bodies_run_5, take_run_5)

#walk
pos_walk_1 = get_bone_pos(bodies_walk_1, take_walk_1)
pos_walk_2 = get_bone_pos(bodies_walk_2, take_walk_2)
pos_walk_3 = get_bone_pos(bodies_walk_3, take_walk_3)
pos_walk_4 = get_bone_pos(bodies_walk_4, take_walk_4)
pos_walk_5 = get_bone_pos(bodies_walk_5, take_walk_5)


############################## RUN 1 -- marker = TRUE #############################################
marker_r = 20
path_run_1, t_run_1 = get_marker_path(pos_run_1, marker_r, take_run_1)
path_run_2, t_run_2 = get_marker_path(pos_run_2, marker_r, take_run_2)
path_run_3, t_run_3 = get_marker_path(pos_run_3, marker_r, take_run_3)
path_run_4, t_run_4 = get_marker_path(pos_run_4, marker_r, take_run_4)  
path_run_5, t_run_5 = get_marker_path(pos_run_5, marker_r, take_run_5)


#-- x
plt.figure(1)
plot_marker_traj(path_run_1, t_run_1, "x")
plot_marker_traj(path_run_2, t_run_2, "x") 
plot_marker_traj(path_run_3, t_run_3, "x")
plot_marker_traj(path_run_4, t_run_4, "x") 
plot_marker_traj(path_run_5, t_run_5, "x")
plt.xlabel('time [s]')
plt.ylabel('x position [m]')


#-- y
plt.figure(2)
plot_marker_traj(path_run_1, t_run_1, "y")
plot_marker_traj(path_run_2, t_run_2, "y") 
plot_marker_traj(path_run_3, t_run_3, "y")
plot_marker_traj(path_run_4, t_run_4, "y") 
plot_marker_traj(path_run_5, t_run_5, "y")
plt.xlabel('time [s]')
plt.ylabel('y position [m]')
plt.show()

#-- z
plot_marker_traj(path_run_1, t_run_1, "z")
plot_marker_traj(path_run_2, t_run_2, "z") 
plot_marker_traj(path_run_3, t_run_3, "z")
plot_marker_traj(path_run_4, t_run_4, "z") 
plot_marker_traj(path_run_5, t_run_5, "z")
plt.xlabel('time [s]')
plt.ylabel('z position [m]')
plt.show()

#-- 3D
ax = plt.axes(projection='3d')
plot_marker_path_3D(path_run_1, ax)
plot_marker_path_3D(path_run_2, ax)
plot_marker_path_3D(path_run_3, ax)
plot_marker_path_3D(path_run_4, ax)
plot_marker_path_3D(path_run_5, ax)
ax.set_ylabel('y [m]')
ax.set_xlabel('x [m]')
ax.set_zlabel('z [m]')
plt.show()

############################# WALK 1 -- marker = TRUE #############################################
marker_w = 20
path_walk_1, t_walk_1 = get_marker_path(pos_walk_1, marker_w, take_walk_1)
path_walk_2, t_walk_2 = get_marker_path(pos_walk_2, marker_w, take_walk_2)
path_walk_3, t_walk_3 = get_marker_path(pos_walk_3, marker_w, take_walk_3)
path_walk_4, t_walk_4 = get_marker_path(pos_walk_4, marker_w, take_walk_4)  
path_walk_5, t_walk_5 = get_marker_path(pos_walk_5, marker_w, take_walk_5)


#-- x
plt.subplot(131)
plot_marker_traj(path_walk_1, t_walk_1, "x")
plot_marker_traj(path_walk_2, t_walk_2, "x") 
plot_marker_traj(path_walk_3, t_walk_3, "x")
plot_marker_traj(path_walk_4, t_walk_4, "x") 
plot_marker_traj(path_walk_5, t_walk_5, "x")
plt.xlabel('time [s]')
plt.ylabel('x position [m]')

#-- y
plt.subplot(132)
plot_marker_traj(path_walk_1, t_walk_1, "y")
plot_marker_traj(path_walk_2, t_walk_2, "y") 
plot_marker_traj(path_walk_3, t_walk_3, "y")
plot_marker_traj(path_walk_4, t_walk_4, "y") 
plot_marker_traj(path_walk_5, t_walk_5, "y")
plt.xlabel('time [s]')
plt.ylabel('y position [m]')

#-- z
plt.subplot(133)
plot_marker_traj(path_walk_1, t_walk_1, "z")
plot_marker_traj(path_walk_2, t_walk_2, "z") 
plot_marker_traj(path_walk_3, t_walk_3, "z")
plot_marker_traj(path_walk_4, t_walk_4, "z") 
plot_marker_traj(path_walk_5, t_walk_5, "z")
plt.xlabel('time [s]')
plt.ylabel('z position [m]')
plt.show()

#-- 3D
ax2 = plt.axes(projection='3d')
plot_marker_path_3D(path_walk_1, ax2)
plot_marker_path_3D(path_walk_2, ax2)
plot_marker_path_3D(path_walk_3, ax2)
plot_marker_path_3D(path_walk_4, ax2)
plot_marker_path_3D(path_walk_5, ax2)
ax2.set_ylabel('y [m]')
ax2.set_xlabel('x [m]')
ax2.set_zlabel('z [m]')
plt.show()

############################## RUN -- all marker #############################################
n_frame = 1000
legend = ['Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe']

fig = plt.figure(figsize=(8,4))
ax = fig.add_subplot(121, projection='3d')
# ax = plt.axes(projection='3d')
for i in range(13, len(take_run_1.rigid_bodies.keys())):
    path_run_1_i, t = get_marker_path(pos_run_1, i, take_run_1)
    plot_marker_path_3D(path_run_1_i, ax, n_frame)
plt.title('1° run')
plt.legend(legend)
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
# plt.show()
ax = fig.add_subplot(122, projection='3d')
# ax = plt.axes(projection='3d')
# ax.subplot(232)
for i in range(13, len(take_run_2.rigid_bodies.keys())):
    path_run_2_i, t = get_marker_path(pos_run_2, i, take_run_2)
    plot_marker_path_3D(path_run_2_i, ax, n_frame)
plt.title('2° run')
plt.legend(legend)
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()

# ax = plt.axes(projection='3d')
# ax.subplot(233)
for i in range(13, len(take_run_3.rigid_bodies.keys())):
    path_run_3_i, t = get_marker_path(pos_run_3, i, take_run_3)
    plot_marker_path_3D(path_run_3_i, ax, n_frame)
plt.title('3° run')
plt.legend(legend)
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
# plt.show()

# ax = plt.axes(projection='3d')
# ax.subplot(234)
for i in range(13, len(take_run_4.rigid_bodies.keys())):
    path_run_4_i, t = get_marker_path(pos_run_4, i, take_run_4)
    plot_marker_path_3D(path_run_4_i, ax, n_frame)
plt.title('4° run')
plt.legend(legend)
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
# plt.show()

# ax = plt.axes(projection='3d')
# ax.subplot(235)
for i in range(13, len(take_run_5.rigid_bodies.keys())):
    path_run_5_i, t = get_marker_path(pos_run_5, i, take_run_5)
    plot_marker_path_3D(path_run_5_i, ax, n_frame)
plt.title('5° run')
plt.legend(legend)
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()


### WALK all joint ###
n_frame = 2000

ax = plt.axes(projection='3d')
for i in range(13, len(take_walk_1.rigid_bodies.keys())):
    path_walk_1_i, t = get_marker_path(pos_walk_1, i, take_walk_1)
    plot_marker_path_3D(path_walk_1_i, ax, n_frame)
plt.title('1° walk')
plt.legend(legend)    
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()

ax = plt.axes(projection='3d')
for i in range(13, len(take_walk_2.rigid_bodies.keys())):
    path_walk_2_i, t = get_marker_path(pos_walk_2, i, take_walk_2)
    plot_marker_path_3D(path_walk_2_i, ax, n_frame)
plt.title('2° walk')
plt.legend(legend)   
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()

ax = plt.axes(projection='3d')
for i in range(13, len(take_walk_3.rigid_bodies.keys())):
    path_walk_3_i, t = get_marker_path(pos_walk_3, i, take_walk_3)
    plot_marker_path_3D(path_walk_3_i, ax, n_frame)
plt.title('3° walk')
plt.legend(legend)   
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()

ax = plt.axes(projection='3d')
for i in range(13, len(take_walk_4.rigid_bodies.keys())):
    path_walk_4_i, t = get_marker_path(pos_walk_4, i, take_walk_4)
    plot_marker_path_3D(path_walk_4_i, ax, n_frame)
plt.title('4° walk')
plt.legend(legend)   
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()

ax = plt.axes(projection='3d')
for i in range(13, len(take_walk_5.rigid_bodies.keys())):
    path_walk_5_i, t = get_marker_path(pos_walk_5, i, take_walk_5)
    plot_marker_path_3D(path_walk_5_i, ax, n_frame)
plt.title('5° walk')
plt.legend(legend)   
ax.set_xlabel('X')
ax.set_xlim(-2.5, 2.5)
ax.set_ylabel('Y')
ax.set_ylim(-2.5, 2.5)
ax.set_zlabel('Z')
ax.set_zlim(0, 2)
plt.show()


