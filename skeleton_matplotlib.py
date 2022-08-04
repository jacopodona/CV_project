# Make sure that the Python libraries also contained within this course package
# are on the load path.  This adds the parent folder to the load path, assuming that this
# script is still located with the rhinoscripts/ subfolder of the Python library tree.
import sys, os

from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import matplotlib.pyplot as plt

from optitrack.plot import *
# Load the Optitrack CSV file parser module.
import optitrack.csv_reader as csv
from optitrack.geometry import *

def loadData(take):

    #legend = ['Hip','Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe']

    #run
    bodies = take.rigid_bodies
    positions = old_get_bone_pos(bodies, take)#contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    plot_take(positions)

def loadMultipleData(take1, take2,name1,name2):
    bodies1 = take1.rigid_bodies
    positions1 = old_get_bone_pos(bodies1,take1)  # contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    bodies2 = take2.rigid_bodies
    positions2 = old_get_bone_pos(bodies2,take2)  # contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    plot_takes(positions1,positions2,name1,name2)

def plot_take(take):
    figure = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')

    take_duration = len(take[0])

    # plt.legend(legend)
    ax.set_xlabel('X')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylabel('Y')
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlabel('Z')
    ax.set_zlim(0, 1.2)

    plt.ion()

    frame=0
    for i in range(frame, take_duration, 10):
        plot_3d_skeleton(take, ax, i, 'black')
        # plot_3d_skeleton(pos_walk_2, ax, i,'red')
        figure.canvas.draw()
        figure.canvas.flush_events()
        ax.clear()
        ax.set_xlabel('X')
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylabel('Y')
        ax.set_ylim(-2.5, 2.5)
        ax.set_zlabel('Z')
        ax.set_zlim(0, 1.2)
        plt.show()

def plot_takes(take1,take2,name1,name2):
    figure = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')

    take_duration = min(len(take1[0]),len(take2[0]))

    ax.set_xlabel('X')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylabel('Y')
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlabel('Z')
    ax.set_zlim(0, 1.2)

    legend_elements = [Line2D([0], [0], color='black', lw=4, label=name1),
                       Line2D([0], [0], color='red', lw=4, label=name2)]

    plt.ion()
    frame=0
    for i in range(frame, take_duration, 10):
        plot_3d_skeleton(take1, ax, i, 'black')
        plot_3d_skeleton(take2, ax, i,'red')
        figure.canvas.draw()
        figure.canvas.flush_events()
        ax.clear()
        ax.set_xlabel('X')
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylabel('Y')
        ax.set_ylim(-2.5, 2.5)
        ax.set_zlabel('Z')
        ax.set_zlim(0, 1.2)
        ax.legend(handles=legend_elements)
        plt.show()
    plt.close()

def sampleRun():
    dir = os.path.dirname(__file__)
    run_1 = os.path.join(dir, 'data/Dona_corsa.csv')
    walk_1 = os.path.join(dir, 'data/Dona_camminata.csv')
    walk_2 = os.path.join(dir, 'data/forna_camminata.csv')

    take_run_1 = csv.Take().readCSV(run_1)
    take_walk_1 = csv.Take().readCSV(walk_1)
    take_walk_2 = csv.Take().readCSV(walk_2)

    # legend = ['Hip','Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe']

    # run
    bodies_run_1 = take_run_1.rigid_bodies
    pos_run_1 = old_get_bone_pos(bodies_run_1, take_run_1)

    # walk
    bodies_walk_1 = take_walk_1.rigid_bodies
    pos_walk_1 = old_get_bone_pos(bodies_walk_1,
                                  take_walk_1)  # contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    bodies_walk_2 = take_walk_2.rigid_bodies
    pos_walk_2 = old_get_bone_pos(bodies_walk_2,
                                  take_walk_2)  # contiene 21 liste (per ogni joint) che contiene per ogni frame le posizioni x,y,z

    # plot_take(pos_walk_1)
    plot_takes(pos_walk_1, pos_run_1)

def main():
    print("Script for the visualization of skeletons through matplotlib")
    print("Data must be in .csv format and inside the /data folder for a being displayed ")
    print("Reading csv files...")
    command=''
    dir = os.path.dirname(__file__)
    path= os.path.join(dir, 'data/')
    csv_names=[]
    csv_takes=[]
    for file in os.listdir('data/'):
        if file.endswith('.csv'):
            file_path = os.path.join(dir, 'data/'+file)
            take = csv.Take().readCSV(file_path)
            csv_names.append(file)
            csv_takes.append(take)
    print("Loaded takes:")
    for i in range (0,len(csv_takes)):
        print("[",i,"] ",csv_names[i])
    while(command!='exit'):
        print("To display a single take, insert the number of the take (ex: 2)")
        print("To compare two takes, insert both takes number (ex: 1 2)")
        print("To terminate the program, type exit")
        command=input()
        if " " not in command:
            if command.isdigit() and int(command)<len(csv_takes):
                command=int(command)
                loadData(csv_takes[command])
            elif(command!="exit"):
                print("Insert a valid number")
        else:
            values=command.split()
            print(values)
            good=True
            for v in values:
                if v.isdigit() and int(v) < len(csv_takes):
                    good=True and good
                    print(int(v))
                else:
                    good=False
            if(good):
                take1=csv_takes[int(values[0])]
                take2=csv_takes[int(values[1])]
                name1 = csv_names[int(values[0])]
                name2 = csv_names[int(values[1])]
                loadMultipleData(take1,take2,name1,name2)
            elif(command!="exit"):
                print("Insert valid numbers")
main()