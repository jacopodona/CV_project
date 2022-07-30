import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import open3d as o3d
import time
import numpy as np

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

# walk
walk_1 = os.path.join(dir, 'data/Dona_camminata.csv')
walk_2 = os.path.join(dir, 'data/edoardo_camminata.csv')
walk_3 = os.path.join(dir, 'data/vittoria_camminata.csv')
walk_4 = os.path.join(dir, 'data/sgamb_camminata.csv')
walk_5 = os.path.join(dir, 'data/forna_camminata.csv')

# Find the path to the test data file located alongside the script.
# filename = os.path.join( os.path.abspath(os.path.dirname(__file__)), "sample_optitrack_take.csv")

# Read the file.
take = csv.Take().readCSV(run_1)

# Print out some statistics
print("Found rigid bodies:", take.rigid_bodies.keys())

# Process the first rigid body into a set of planes.
bodies = take.rigid_bodies

# for now:
xaxis = [1, 0, 0]
yaxis = [0, 1, 0]

body_edges = [[0, 1], [1, 2], [2, 3], [3, 4], [3, 5], [5, 6], [6, 7], [7, 8], [3, 9], [9, 10], [10, 11], [11, 12],
              [0, 13], [13, 14], [14, 15],
              [0, 16], [16, 17], [17, 18], [18, 20], [15, 19]]

bones_pos = []
if len(bodies) > 0:
    for body in bodies:
        bones = take.rigid_bodies[body]
        bones_pos.append(bones.positions)
        # for pos,rot in zip(body.positions, body.rotations):
        #     if pos is not None and rot is not None:
        #         xaxis, yaxis = quaternion_to_xaxis_yaxis(rot)
        # plane = rs.PlaneFromFrame(pos, xaxis, yaxis)

        # # create a visible plane, assuming units are in meters
        # rs.AddPlaneSurface( plane, 0.1, 0.1 )
bones_pos = np.array(bones_pos).T.tolist()
colors = [[1, 0, 0] for i in range(len(body_edges))]
keypoints = o3d.geometry.PointCloud()
keypoints.points = o3d.utility.Vector3dVector(bones_pos[0])
keypoints_center = keypoints.get_center()
keypoints.points = o3d.utility.Vector3dVector(bones_pos[0])
skeleton_joints = o3d.geometry.LineSet()
skeleton_joints.points = o3d.utility.Vector3dVector(bones_pos[0])
center_skel = skeleton_joints.get_center()
skeleton_joints.points = o3d.utility.Vector3dVector(bones_pos[0])
skeleton_joints.lines = o3d.utility.Vector2iVector(body_edges)
skeleton_joints.colors = o3d.utility.Vector3dVector(colors)

vis = o3d.visualization.Visualizer()

vis.create_window()
# This plot the entire skeleton
vis.add_geometry(skeleton_joints)
vis.add_geometry(keypoints)

for i in range(1000, 2003):
    print(i)
    new_joints = bones_pos[i]
    # center_skel = skeleton_joints.get_center()
    skeleton_joints.points = o3d.utility.Vector3dVector(new_joints)
    keypoints.points = o3d.utility.Vector3dVector(new_joints)
    print(new_joints)
    # This plot the entire skeleton
    vis.update_geometry(skeleton_joints)
    vis.update_geometry(keypoints)

    vis.update_renderer()
    vis.poll_events()


vis.run()