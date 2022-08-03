# Make sure that the Python libraries also contained within this course package
# are on the load path.  This adds the parent folder to the load path, assuming that this
# script is still located with the rhinoscripts/ subfolder of the Python library tree.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import open3d as o3d
import time
import numpy as np
import matplotlib.pyplot as plt

from optitrack.plot import *
# Load the Optitrack CSV file parser module.
import optitrack.csv_reader as csv
from optitrack.geometry import *

def main():
    dir = os.path.dirname(__file__)
    run_1 = os.path.join(dir, 'data/Dona_corsa.csv')
    walk_1 = os.path.join(dir, 'data/Dona_camminata.csv')
    walk_2 = os.path.join(dir, 'data/forna_camminata.csv')

    take_run_1 = csv.Take().readCSV(run_1)
    take_walk_1 = csv.Take().readCSV(walk_1)
    take_walk_2 = csv.Take().readCSV(walk_2)

    legend = ['Hip','Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe']

    #run
    bodies_run_1 = take_run_1.rigid_bodies
    pos_run_1 = old_get_bone_pos(bodies_run_1, take_run_1)

    #walk
    bodies_walk_1 = take_walk_1.rigid_bodies
    pos_walk_1 = old_get_bone_pos(bodies_walk_1, take_walk_1)#contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    bodies_walk_2 = take_walk_2.rigid_bodies
    pos_walk_2 = old_get_bone_pos(bodies_walk_2, take_walk_2)#contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    #plot_take(pos_walk_1)
    plot_takes(pos_walk_1,pos_run_1)

def plot_take(take):
    figure = plt.figure(figsize=(8, 4))
    ax = plt.axes(projection='3d')

    take_duration = len(take[0])

    plt.title('Walk')
    # plt.legend(legend)
    ax.set_xlabel('X')
    ax.set_xlim(-2.5, 1)
    ax.set_ylabel('Y')
    ax.set_ylim(-2.5, 1)
    ax.set_zlabel('Z')
    ax.set_zlim(0, 1)

    plt.ion()

    frame=0
    for i in range(frame, take_duration, 10):
        plot_3d_skeleton(take, ax, i, 'black')
        # plot_3d_skeleton(pos_walk_2, ax, i,'red')
        figure.canvas.draw()
        figure.canvas.flush_events()
        ax.clear()
        ax.set_xlabel('X')
        ax.set_xlim(-2.5, 1)
        ax.set_ylabel('Y')
        ax.set_ylim(-2.5, 1)
        ax.set_zlabel('Z')
        ax.set_zlim(0, 1)
        plt.show()

def plot_takes(take1,take2):
    figure = plt.figure(figsize=(8, 4))
    ax = plt.axes(projection='3d')

    take_duration = min(len(take1[0]),len(take2[0]))

    plt.title('Walk')
    # plt.legend(legend)
    ax.set_xlabel('X')
    ax.set_xlim(-2.5, 1)
    ax.set_ylabel('Y')
    ax.set_ylim(-2.5, 1)
    ax.set_zlabel('Z')
    ax.set_zlim(0, 1)

    plt.ion()
    frame=0
    for i in range(frame, take_duration, 10):
        plot_3d_skeleton(take1, ax, i, 'black')
        plot_3d_skeleton(take2, ax, i,'red')
        figure.canvas.draw()
        figure.canvas.flush_events()
        ax.clear()
        ax.set_xlabel('X')
        ax.set_xlim(-2.5, 1)
        ax.set_ylabel('Y')
        ax.set_ylim(-2.5, 1)
        ax.set_zlabel('Z')
        ax.set_zlim(0, 1)
        plt.show()


main()