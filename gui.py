from kivy.app import App
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.uix.label import Label
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from optitrack.plot import *
import optitrack.csv_reader as csv
from datetime import datetime
from optitrack.geometry import *



# Initialization of the window
Window.maximize()
Builder.load_file('gui.kv')

# Setup matplot color cycle
colors = ["indianred", "forestgreen", "royalblue", 
            "darkorange", "aqua", "hotpink", 
            "gold", "darkorchid", "chocolate"]

matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=colors)

# time stamp to create different file names in saves
def getTimestamp():
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = str(datetime.timestamp(dt))
    ts = ts.replace('.','_')
    return ts


class MyLayout(TabbedPanel):
    # Initialize class variable
    legend = ['Hip','Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe'] 
    set_frame = -1  
    slider = False
    save_plt = False
    file_name = ""
    data_path = []
    data_path_sel = []
    spinner = []
    my_path = os.path.dirname(__file__)
    color_count = 0
    n_file = 0
    
    # Initialize file-chooser
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.spinner_joint.values = MyLayout.legend
        self.ids.filechooser.path = MyLayout.my_path
        
    # Save tmp selected file
    def selected(self, file_path):
        if file_path:
            MyLayout.file_name = file_path[0]

    # Change opacity in file button
    def choose_file(self, number):
        if MyLayout.data_path:
            
            # Manages single file choose for multiple body part case
            # select file by change button opacity
            if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":
                MyLayout.n_file = number
                if number == 0:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_zero.background_color[3] = 0.4
                if number == 1:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_one.background_color[3] = 0.4
                if number == 2:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_two.background_color[3] = 0.4
                if number == 3:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_three.background_color[3] = 0.4
                if number == 4:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_four.background_color[3] = 0.4
                if number == 5:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_five.background_color[3] = 0.4
                if number == 6:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_six.background_color[3] = 0.4
                if number == 7:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_sev.background_color[3] = 0.4
                if number == 8:
                    MyLayout.set_file_color_to_std(self)
                    self.ids.f_label_eigth.background_color[3] = 0.4
            
            # Manages multiple file choose for single body part case
            # select file by change button opacity
            if self.ids.multi_graph.text == "[b]Disable multiple\nfile joint[/b]":
                if number == 0 and self.ids.f_label_zero.background_color[3] == 1:
                    self.ids.f_label_zero.background_color[3] = 0.4
                    return
                if number == 0 and self.ids.f_label_zero.background_color[3] == 0.4:
                    self.ids.f_label_zero.background_color[3] = 1
                if number == 1 and self.ids.f_label_one.background_color[3] == 1:
                    self.ids.f_label_one.background_color[3] = 0.4
                    return
                if number == 1 and self.ids.f_label_one.background_color[3] == 0.4:
                    self.ids.f_label_one.background_color[3] = 1
                if number == 2 and self.ids.f_label_two.background_color[3] == 1:
                    self.ids.f_label_two.background_color[3] = 0.4
                    return
                if number == 2 and self.ids.f_label_two.background_color[3] == 0.4:
                    self.ids.f_label_two.background_color[3] = 1
                if number == 3 and self.ids.f_label_three.background_color[3] == 1:
                    self.ids.f_label_three.background_color[3] = 0.4
                    return
                if number == 3 and self.ids.f_label_three.background_color[3] == 0.4:
                    self.ids.f_label_three.background_color[3] = 1
                if number == 4 and self.ids.f_label_four.background_color[3] == 1:
                    self.ids.f_label_four.background_color[3] = 0.4
                    return
                if number == 4 and self.ids.f_label_four.background_color[3] == 0.4:
                    self.ids.f_label_four.background_color[3] = 1
                if number == 5 and self.ids.f_label_five.background_color[3] == 1:
                    self.ids.f_label_five.background_color[3] = 0.4
                    return
                if number == 5 and self.ids.f_label_five.background_color[3] == 0.4:
                    self.ids.f_label_five.background_color[3] = 1
                if number == 6 and self.ids.f_label_six.background_color[3] == 1:
                    self.ids.f_label_six.background_color[3] = 0.4
                    return
                if number == 6 and self.ids.f_label_six.background_color[3] == 0.4:
                    self.ids.f_label_six.background_color[3] = 1
                if number == 7 and self.ids.f_label_sev.background_color[3] == 1:
                    self.ids.f_label_sev.background_color[3] = 0.4
                    return
                if number == 7 and self.ids.f_label_sev.background_color[3] == 0.4:
                    self.ids.f_label_sev.background_color[3] = 1
                if number == 8 and self.ids.f_label_eigth.background_color[3] == 1:
                    self.ids.f_label_eigth.background_color[3] = 0.4
                    return
                if number == 8 and self.ids.f_label_eigth.background_color[3] == 0.4:
                    self.ids.f_label_eigth.background_color[3] = 1

    # Set opacity to 1 for all button
    def set_file_color_to_std(self):
        self.ids.f_label_zero.background_color[3] = 1
        self.ids.f_label_one.background_color[3] = 1
        self.ids.f_label_two.background_color[3] = 1
        self.ids.f_label_three.background_color[3] = 1
        self.ids.f_label_four.background_color[3] = 1
        self.ids.f_label_five.background_color[3] = 1
        self.ids.f_label_six.background_color[3] = 1
        self.ids.f_label_sev.background_color[3] = 1
        self.ids.f_label_eigth.background_color[3] = 1
            
    # Manage multiple file choose, enable-disable body parts checks
    def multi_graph(self):
        if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":
            self.ids.multi_graph.text = "[b]Disable multiple\nfile joint[/b]"
            self.ids.hip_check.disabled = True
            self.ids.l_thigh_check.disabled = True
            self.ids.l_shin_check.disabled = True
            self.ids.l_foot_check.disabled = True
            self.ids.r_thigh_check.disabled = True
            self.ids.r_shin_check.disabled = True
            self.ids.r_foot_check.disabled = True
            self.ids.l_toe_check.disabled = True
            self.ids.r_toe_check.disabled = True
            self.ids.spinner_joint.disabled = False
            self.ids.button_sel.disabled = True

        else:
            self.ids.multi_graph.text = "[b]Enable multiple\nfile joint[/b]"
            self.ids.hip_check.disabled = False
            self.ids.l_thigh_check.disabled = False
            self.ids.l_shin_check.disabled = False
            self.ids.l_foot_check.disabled = False
            self.ids.r_thigh_check.disabled = False
            self.ids.r_shin_check.disabled = False
            self.ids.r_foot_check.disabled = False
            self.ids.l_toe_check.disabled = False
            self.ids.r_toe_check.disabled = False
            self.ids.spinner_joint.disabled = True
            self.ids.button_sel.disabled = False
        MyLayout.set_file_color_to_std(self)

    # Load data 
    def load_data(self):
        if MyLayout.file_name not in MyLayout.data_path and ".csv" in MyLayout.file_name:
            # Set name on GUI
            self.ids.load_data_label.add_widget(Label(text =  os.path.basename(MyLayout.file_name),
                                                        font_size = 20))
            MyLayout.data_path.append(MyLayout.file_name)   # Save file path
            
            pr = True
            # Set name of file
            if self.ids.f_label_zero.disabled and pr == True:
                self.ids.f_label_zero.disabled = False
                self.ids.f_label_zero.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_zero.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_one.disabled and pr == True:
                self.ids.f_label_one.disabled = False
                self.ids.f_label_one.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_one.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_two.disabled and pr == True:
                self.ids.f_label_two.disabled = False
                self.ids.f_label_two.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_two.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_three.disabled and pr == True:
                self.ids.f_label_three.disabled = False
                self.ids.f_label_three.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_three.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_four.disabled and pr == True:
                self.ids.f_label_four.disabled = False
                self.ids.f_label_four.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_four.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_five.disabled and pr == True:
                self.ids.f_label_five.disabled = False
                self.ids.f_label_five.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_five.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_six.disabled and pr == True:
                self.ids.f_label_six.disabled = False
                self.ids.f_label_six.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_six.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_sev.disabled and pr == True:
                self.ids.f_label_sev.disabled = False
                self.ids.f_label_sev.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_sev.background_color = colors[MyLayout.color_count]
                pr = False
            if self.ids.f_label_eigth.disabled and pr == True:
                self.ids.f_label_eigth.disabled = False
                self.ids.f_label_eigth.text = os.path.basename(MyLayout.file_name)
                self.ids.f_label_eigth.background_color = colors[MyLayout.color_count]
                pr = False

            MyLayout.color_count += 1   # Manage color Matplot cycle color         

    # Clear data and plot
    def clear_data(self):
        # Clear plot widget 
        self.ids.load_data_label.clear_widgets()
        del MyLayout.data_path[:]
        self.ids.graph_x.clear_widgets()
        self.ids.graph_y.clear_widgets()
        self.ids.graph_z.clear_widgets()
        self.ids.graph_xyz.clear_widgets()
        self.ids.graph_3d.clear_widgets()
        MyLayout.color_count = 0

        # Set button color to standard
        self.ids.f_label_zero.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_one.background_color = (1, 237/255, 237/255, 1)       
        self.ids.f_label_two.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_three.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_four.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_five.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_six.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_sev.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_eigth.background_color = (1, 237/255, 237/255, 1)
        
        # Set button text to standard
        self.ids.f_label_zero.text = " "
        self.ids.f_label_one.text = " "
        self.ids.f_label_two.text = " "
        self.ids.f_label_three.text = " "
        self.ids.f_label_four.text = " "
        self.ids.f_label_five.text = " "
        self.ids.f_label_six.text = " "
        self.ids.f_label_sev.text = " "
        self.ids.f_label_eigth.text = " "
        
        # Set button state to Disabled
        self.ids.f_label_zero.disabled = True
        self.ids.f_label_one.disabled = True
        self.ids.f_label_two.disabled = True
        self.ids.f_label_three.disabled = True
        self.ids.f_label_four.disabled = True
        self.ids.f_label_five.disabled = True
        self.ids.f_label_six.disabled = True
        self.ids.f_label_sev.disabled = True
        self.ids.f_label_eigth.disabled = True
        
    # Manage check box for multiple body part
    def select_all(self):
        # Check all the boxes
        if self.ids.button_sel.text == "[b]Check all[/b]":
            self.ids.hip_check.active = True
            self.ids.l_thigh_check.active = True
            self.ids.l_shin_check.active = True
            self.ids.l_foot_check.active = True
            self.ids.r_thigh_check.active = True
            self.ids.r_shin_check.active = True
            self.ids.r_foot_check.active = True
            self.ids.l_toe_check.active = True
            self.ids.r_toe_check.active = True
            self.ids.button_sel.text = "[b]Uncheck all[/b]"
        else: 
            # Uncheck all the boxes
            self.ids.hip_check.active = False
            self.ids.l_thigh_check.active = False
            self.ids.l_shin_check.active = False
            self.ids.l_foot_check.active = False
            self.ids.r_thigh_check.active = False
            self.ids.r_shin_check.active = False
            self.ids.r_foot_check.active = False
            self.ids.l_toe_check.active = False
            self.ids.r_toe_check.active = False
            self.ids.button_sel.text = "[b]Check all[/b]"

    # Arrange data to be ready to Plot in multiple file case
    def select_data_path_from_file(self):
        count = 0
        color = []

        # Finds choosen file
        if self.ids.f_label_zero.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[0])
        count += 1
            
        if self.ids.f_label_one.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[1])
        count += 1

        if self.ids.f_label_two.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[2])
        count += 1
            
        if self.ids.f_label_three.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[3])
        count += 1
            
        if self.ids.f_label_four.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[4])
        count += 1
            
        if self.ids.f_label_five.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[5])
        count += 1
            
        if self.ids.f_label_six.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[6])
        count += 1
            
        if self.ids.f_label_sev.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[7])
        count += 1
            
        if self.ids.f_label_eigth.background_color[3] == 0.4:
            MyLayout.data_path_sel.append(MyLayout.data_path[count])
            color.append(colors[8])

        # Change matplot color cycle for plot
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=color)
            
    # Manage All 2D plots
    def plot_all(self):
        # Set matplot color cycle to standard
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=colors)

        if MyLayout.data_path:

            # Single file - multiple body parts case
            if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":

                # get joints selection
                joints = [self.ids.hip_check.active,
                        self.ids.l_thigh_check.active,
                        self.ids.l_shin_check.active,
                        self.ids.l_foot_check.active,
                        self.ids.r_thigh_check.active,
                        self.ids.r_shin_check.active,
                        self.ids.r_foot_check.active,
                        self.ids.l_toe_check.active,
                        self.ids.r_toe_check.active]

                # If no file is selected select the first one
                if MyLayout.n_file == 0:
                    self.ids.f_label_zero.background_color[3] = 0.4

                # Plot legend on check boxes
                MyLayout.set_joint_color(self, joints)
        
                # Compute position
                take, pos_joint = MyLayout.compute_pos(self)

                # Select joints
                selc_joints, legend = get_joints(pos_joint, joints, MyLayout.legend)

                # Set slider max value
                if MyLayout.set_frame == -1 and True in joints:
                    self.ids.slider.max = len(selc_joints[0])
                    self.ids.slider.value = len(selc_joints[0])

                # PLOTS
                MyLayout.plot_x_t(self, selc_joints, legend, take)
                MyLayout.plot_y_t(self, selc_joints, legend, take)
                MyLayout.plot_z_t(self, selc_joints, legend, take)
                MyLayout.plot_xyz(self, selc_joints, legend, take)
            else:

                # Multiple file - single body parts case
                # initialize local variable
                MyLayout.data_path_sel.clear()
                joints = []
                take = []
                pos_joint = []
                select_joint = ""

                # Select joint
                for i in MyLayout.legend:
                    if self.ids.spinner_joint.text == i:
                        joints.append(True)
                        select_joint = i
                    else:
                        joints.append(False)

                # If no body part is selcted, select HIP
                if not True in joints and joints:
                    joints[0] = True
                    self.ids.spinner_joint.text = "Hip"

                # Get selected files
                MyLayout.select_data_path_from_file(self)

                # If no data is selected, select the first file
                if len(MyLayout.data_path_sel) == 0:
                    self.ids.f_label_zero.background_color[3] = 0.4
                    MyLayout.select_data_path_from_file(self)

                # Get data path
                for i in MyLayout.data_path_sel:
                    MyLayout.file_name = i
                    take_tmp, pos_joint_tmp = MyLayout.compute_pos(self)
                    selc_joints, legend = get_joints(pos_joint_tmp, joints, MyLayout.legend)
                    take.append(take_tmp)
                    pos_joint.append(selc_joints)
            
                # Compute max frame for slider
                if MyLayout.set_frame == -1 and True in joints:
                    first = True
                    for i in pos_joint:
                        if len(i[0]) < self.ids.slider.max or first == True:
                            self.ids.slider.max = len(i[0])
                            self.ids.slider.value = len(i[0])
                            first = False
                
                # PLOTS
                MyLayout.plot_x_t_sJoint(self, pos_joint, select_joint, take)
                MyLayout.plot_y_t_sJoint(self, pos_joint, select_joint, take)
                MyLayout.plot_z_t_sJoint(self, pos_joint, select_joint, take)
                MyLayout.plot_xyz_sJoint(self, pos_joint, select_joint, take)

    # Copute Take and position from file name (2D)
    def compute_pos(self):

        if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":
            # Multiple file - single joint
            take = csv.Take().readCSV(MyLayout.data_path[MyLayout.n_file])
        else:
            # Single file - multiple joints
            take = csv.Take().readCSV(MyLayout.file_name)
        body = take.rigid_bodies
        pos = get_bone_pos(body, take)
        return take, pos

    # Copute Take and position from file name (3D)
    def compute_pos_3d(self):
        take = csv.Take().readCSV(MyLayout.file_name)
        body = take.rigid_bodies
        pos = get_bone_pos(body, take)
        return take, pos

    # Set file name in label text for 3D
    def text_file_plt(self):
        # Setup local varibles
        count = 0
        zero =False
        one = False
        two = False
        three = False
        four = False
        five = False
        six = False
        sev =False
        eigth = False

        # Look at the selected files
        if self.ids.f_label_zero.background_color[3] == 0.4:
            count += 1
            zero = True
        if self.ids.f_label_one.background_color[3] == 0.4:
            count += 1
            one = True
        if self.ids.f_label_two.background_color[3] == 0.4:
            count += 1
            two = True
        if self.ids.f_label_three.background_color[3] == 0.4:
            count += 1
            three = True
        if self.ids.f_label_four.background_color[3] == 0.4:
            count += 1
            four = True
        if self.ids.f_label_five.background_color[3] == 0.4:
            count += 1
            five = True
        if self.ids.f_label_six.background_color[3] == 0.4:
            count += 1
            six = True
        if self.ids.f_label_sev.background_color[3] == 0.4:
            count += 1
            sev = True
        if self.ids.f_label_eigth.background_color[3] == 0.4:
            count += 1
            eigth = True

        # warning label text for data
        if count == 0:
            if MyLayout.data_path:
                self.ids.f_label_zero.background_color[3] = 0.4
                self.ids.text_sel_file.text = f"The selected file is: [b]{self.ids.f_label_zero.text}[/b]"
            else:
                self.ids.text_sel_file.text = f"No file is selected"

        # If more file are selected choose the first one
        if count > 1:
            MyLayout.set_file_color_to_std(self)
            self.ids.f_label_zero.background_color[3] = 0.4
            self.ids.text_sel_file.text = f"The selected file is: [b]{self.ids.f_label_zero.text}[/b]"
        
        # Print the choosen file
        if count == 1:
            if zero == True:
                text = self.ids.f_label_zero.text
            if one == True:
                text = self.ids.f_label_one.text
            if two == True:
                text = self.ids.f_label_two.text
            if three == True:
                text = self.ids.f_label_three.text
            if four == True:
                text = self.ids.f_label_four.text
            if five == True:
                text = self.ids.f_label_five.text
            if six == True:
                text = self.ids.f_label_six.text
            if sev == True:
                text = self.ids.f_label_sev.text
            if eigth == True:
                text = self.ids.f_label_eigth.text
            self.ids.text_sel_file.text = f"The selected file is: [b]{text}[/b]"

    # 2D plot x(t) - single file - multiple joint
    def plot_x_t(self, selc_joints, legend, take):
        # Initialize plot
        self.ids.graph_x.clear_widgets()
        fig_x, ax = plt.subplots()

        # Plot all selected joint time vs x 
        for i in range(0, len(selc_joints)):
            path_x, t_x = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_x, t_x, ax, MyLayout.set_frame, "x")
        
        # Set title and axes names
        ax.set_xlabel("t")
        ax.set_ylabel("x")
        ax.set_title("Evolution of x(t) for multiple body part")

        # Save plot
        if MyLayout.save_plt:
            my_file = 'x_t take_'+ getTimestamp() +'.png'
            fig_x.savefig(os.path.join(MyLayout.my_path, my_file))

        # Plot the graph in the boxPlot in the GUI
        plot_x_t = FigureCanvas(fig_x)
        graph_x = self.ids.graph_x
        graph_x.add_widget(plot_x_t)
        
    # 2D plot x(t) - multiple file - single joint
    def plot_x_t_sJoint(self, pos_joint, select_joint, take):
        # Initialize plot
        self.ids.graph_x.clear_widgets()
        fig_x_sJoint, ax_sJoint = plt.subplots()

        # For each file plot the selected joint
        for pos_sJoint, take_sJoint in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_x_sJoint, t_x_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_x_sJoint, t_x_sJoint, ax_sJoint, MyLayout.set_frame, "x")

        # Set title and axes names
        ax_sJoint.set_xlabel("t")
        ax_sJoint.set_ylabel("x")
        ax_sJoint.set_title(f"Evolution of x(t) for multiple files [{self.ids.spinner_joint.text}]")

        # Save plot
        if MyLayout.save_plt:
            my_file = f'x_t_{select_joint} take_'+ getTimestamp() +'.png'
            fig_x_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
        
        # Plot the graph in the boxPlot in the GUI
        plot_x_t_sJoint = FigureCanvas(fig_x_sJoint)
        graph_x = self.ids.graph_x
        graph_x.add_widget(plot_x_t_sJoint)

    # 2D plot y(t) - single file - multiple joint
    def plot_y_t(self, selc_joints, legend, take):
        # Initialize plot
        self.ids.graph_y.clear_widgets()
        fig_y, ay=plt.subplots(figsize=plt.rcParams["figure.figsize"][::-1])
        fig_y.subplots_adjust(left=0.1, right=0.875, top=0.9,bottom=0.125)  # adjust graph dimension

        # Plot all selected joint time vs y with rotate axle
        for i in range(0, len(selc_joints)):
            path_y, t_y = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_y, t_y, ay, MyLayout.set_frame, "y", reverse_axis = True)

        # Set title and axes names and rotation
        ay.set_ylabel("t", rotation=90)
        ay.yaxis.tick_right()
        ay.yaxis.set_label_position("right")
        ay.set_title("Evolution of y(t) for multiple body part")    
        ay.set_xlabel("y")
        ay.invert_xaxis()
        ay.invert_yaxis()

        # Save plot
        if MyLayout.save_plt:
            my_file = 'y_t take_'+ getTimestamp() +'.png'
            fig_y.savefig(os.path.join(MyLayout.my_path, my_file))

        # Plot the graph in the boxPlot in the GUI# Save plot
        plot_y_t = FigureCanvas(fig_y)
        graph_y = self.ids.graph_y
        graph_y.add_widget(plot_y_t)

    # 2D plot y(t) - multiple file - single joint
    def plot_y_t_sJoint(self, pos_joint, select_joint, take):
        # Initialize plot
        self.ids.graph_y.clear_widgets()
        fig_y_sJoint, ay_sJoint = plt.subplots()

        # For each file plot the selected joint
        for pos_sJoint, take_sJoint in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_y_sJoint, t_y_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_y_sJoint, t_y_sJoint, ay_sJoint, MyLayout.set_frame, "y", reverse_axis = True)

        # Set title and axes names and rotation
        ay_sJoint.set_ylabel("t", rotation=90)
        ay_sJoint.yaxis.tick_right()
        ay_sJoint.yaxis.set_label_position("right")    
        ay_sJoint.set_xlabel("y")
        ay_sJoint.invert_xaxis()
        ay_sJoint.invert_yaxis()
        ay_sJoint.set_title(f"Evolution of y(t) for multiple files [{self.ids.spinner_joint.text}]")

        # Save plot
        if MyLayout.save_plt:
            my_file = f'y_t_{select_joint} take_'+ getTimestamp() +'.png'
            fig_y_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))

        # Plot the graph in the boxPlot in the GUI
        plot_y_t_sJoint = FigureCanvas(fig_y_sJoint)
        graph_y = self.ids.graph_y
        graph_y.add_widget(plot_y_t_sJoint)

    # 2D plot z(t) - single file - multiple joint
    def plot_z_t(self, selc_joints, legend, take):
        # Initialize plot
        self.ids.graph_z.clear_widgets()
        fig_z, az = plt.subplots()

        # Plot all selected joint time vs z 
        for i in range(0, len(selc_joints)):
            path_z, t_z = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_z, t_z, az, MyLayout.set_frame, "z")

        # Set title and axes names
        az.set_xlabel("t")
        az.set_ylabel("z")
        az.set_title("Evolution of z(t) for multiple body part")

        # Save plot
        if MyLayout.save_plt:
            my_file = 'z_t take_'+getTimestamp()+'.png'
            fig_z.savefig(os.path.join(MyLayout.my_path, my_file))

        # Plot the graph in the boxPlot in the GUI# Save plot
        plot_z_t = FigureCanvas(fig_z)
        graph_z = self.ids.graph_z
        graph_z.add_widget(plot_z_t)
       
    # 2D plot z(t) - multiple file - single joint
    def plot_z_t_sJoint(self, pos_joint, select_joint, take):
        # Initialize plot
        self.ids.graph_z.clear_widgets()
        fig_z_sJoint, az_sJoint = plt.subplots()

        # For each file plot the selected joint
        for pos_sJoint, take_sJoint  in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_z_sJoint, t_z_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_z_sJoint, t_z_sJoint, az_sJoint, MyLayout.set_frame, "z")

        # Set title and axes names
        az_sJoint.set_xlabel("t")
        az_sJoint.set_ylabel("z")
        az_sJoint.set_title(f"Evolution of z(t) for multiple files [{self.ids.spinner_joint.text}]")

        # Save plot
        if MyLayout.save_plt:
            my_file = f'z_t_{select_joint} take_'+getTimestamp()+'.png'
            fig_z_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
        
        # Plot the graph in the boxPlot in the GUI
        plot_z_t_sJoint = FigureCanvas(fig_z_sJoint)
        graph_z = self.ids.graph_z
        graph_z.add_widget(plot_z_t_sJoint)

    # 2D plot x/y/z - single file - multiple joint
    def plot_xyz(self, selc_joints, legend, take):

        if self.ids.multiple_choice.text == "Plot X-Z":
            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint in X-Z plane
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "xz")

            # Set title and axes names
            axyz.set_xlabel("x")
            axyz.set_ylabel("z")
            axyz.set_title("Evolution on X-Z plane for multiple body part")

            # Save plot
            if MyLayout.save_plt:
                my_file = 'x_z take_'+ getTimestamp() +'.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))

            # Plot the graph in the boxPlot in the GUI
            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)

        if self.ids.multiple_choice.text == "Plot X-Y" or self.ids.multiple_choice.text == "Choose the plot":

            # Set plane X-Y as defaul if not choosen
            self.ids.multiple_choice.text = "Plot X-Y"

            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint in X-Y plane 
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "xy")

            # Set title and axes names
            axyz.set_xlabel("x")
            axyz.set_ylabel("y")
            axyz.set_title("Evolution on X-Y plane for multiple body part")

            # Save plot
            if MyLayout.save_plt:
                my_file = 'x_y_take_'+getTimestamp()+'.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))

            # Plot the graph in the boxPlot in the GUI
            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)
        
        if self.ids.multiple_choice.text == "Plot Y-Z":

            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint in Y-Z plane
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "yz")

            # Set title and axes names
            axyz.set_xlabel("y")
            axyz.set_ylabel("z")
            axyz.set_title("Evolution on Y-Z plane for multiple body part")

            # Save plot
            if MyLayout.save_plt:
                my_file = 'y_z take_'+getTimestamp()+'.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))

            # Plot the graph in the boxPlot in the GUI
            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)

    # 2D plot x/y/z - multiple file - single joint
    def plot_xyz_sJoint(self, pos_joint, select_joint, take):
        
        if self.ids.multiple_choice.text == "Plot X-Z":

            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected files on plane X-Z
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "xz")

            # Set title and axes names
            axyz_sJoint.set_xlabel("x")
            axyz_sJoint.set_ylabel("z")
            axyz_sJoint.set_title(f"Evolution on X-Z plane for multiple files [{self.ids.spinner_joint.text}]")

            # Save plot
            if MyLayout.save_plt:
                my_file = f'x_z_{select_joint} take_'+ getTimestamp() +'.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
            
            # Plot the graph in the boxPlot in the GUI
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)

        if self.ids.multiple_choice.text == "Plot X-Y" or self.ids.multiple_choice.text == "Choose the plot":

            # Set plane X-Y as defaul if not choosen
            self.ids.multiple_choice.text = "Plot X-Y"

            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected files on plane X-Y
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "xy")

            # Set title and axes names
            axyz_sJoint.set_xlabel("x")
            axyz_sJoint.set_ylabel("y")
            axyz_sJoint.set_title(f"Evolution on X-Y plane for multiple files [{self.ids.spinner_joint.text}]")

            # Save plot
            if MyLayout.save_plt:
                my_file = f'x_y_{select_joint} take_'+ getTimestamp() +'.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))

            # Plot the graph in the boxPlot in the GUI
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)
        
        if self.ids.multiple_choice.text == "Plot Y-Z":

            # Initialize plot
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected files on plane Y-Z
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "yz")

            # Set title and axes names
            axyz_sJoint.set_xlabel("y")
            axyz_sJoint.set_ylabel("z")
            axyz_sJoint.set_title(f"Evolution on Y-Z plane for multiple files [{self.ids.spinner_joint.text}]")

            # Save plot
            if MyLayout.save_plt:
                my_file = f'y_z_{select_joint} take_'+ getTimestamp() +'.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))

            # Plot the graph in the boxPlot in the GUI
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)

    # Manage legend in box plot
    def set_joint_color(self, joints):
        count = 0
        if joints[0]:
            self.ids.hip_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.hip_text.background_color = (1, 237/255, 237/255, 1)
        if joints[1]:
            self.ids.l_thigh_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_thigh_text.background_color = (1, 237/255, 237/255, 1)
        if joints[2]:
            self.ids.l_shin_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_shin_text.background_color = (1, 237/255, 237/255, 1)
        if joints[3]:
            self.ids.l_foot_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_foot_text.background_color = (1, 237/255, 237/255, 1)
        if joints[4]:
            self.ids.r_thigh_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_thigh_text.background_color = (1, 237/255, 237/255, 1)
        if joints[5]:
            self.ids.r_shin_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_shin_text.background_color = (1, 237/255, 237/255, 1)
        if joints[6]:
            self.ids.r_foot_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_foot_text.background_color = (1, 237/255, 237/255, 1)
        if joints[7]:
            self.ids.l_toe_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_toe_text.background_color = (1, 237/255, 237/255, 1)
        if joints[8]:
            self.ids.r_toe_text.background_color = matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_toe_text.background_color = (1, 237/255, 237/255, 1)
    
    # Manage 2D slider
    def slide_it(self, *args):
        MyLayout.set_frame = int(args[1])
        if MyLayout.slider:
            MyLayout.plot_all(self)

    # Enable auto update of the frames
    def auto_update(self):
        if self.ids.auto_update_label.text == "[b]Enable auto-update[/b]":
            self.ids.auto_update_label.text = "[b]Disable auto-update[/b]"
            MyLayout.slider = True
        else:
            self.ids.auto_update_label.text = "[b]Enable auto-update[/b]"
            MyLayout.slider = False

    # Save 2D plot
    def save_plts(self):
        MyLayout.save_plt = True
        MyLayout.plot_all(self)
        MyLayout.save_plt = False

    # Save 3D plot
    def save_plts_3d(self):
        MyLayout.save_plt = True
        MyLayout.plot_all_3d(self)
        MyLayout.save_plt = False

    # Plot 3D graph
    def plot_3d(self, selc_joints, legend, take):
        # Initialize plot
        self.ids.graph_3d.clear_widgets()
        fig_3d = plt.figure(figsize=(8, 4))
        ax = fig_3d.add_subplot(111, projection='3d')
        
        # Plot all selected joint 3d positions
        for i in range(0, len(selc_joints)):
            path_3d, t = get_marker_path(selc_joints, i, take)
            plot_marker_path_3D(path_3d, ax, MyLayout.set_frame)

        # Set title and axes names
        ax.set_title("Evolution in 3D of multiple joint")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        # Save plot
        if MyLayout.save_plt:
            my_file = '3D take_'+ getTimestamp() +'.png'
            fig_3d.savefig(os.path.join(MyLayout.my_path, my_file), 
                            dpi = 300, bbox_inches = 'tight', pad_inches = 1)

        # Plot the graph in the boxPlot in the GUI
        plot_3d_Joint = FigureCanvas(fig_3d)
        graph_3d = self.ids.graph_3d
        graph_3d.add_widget(plot_3d_Joint)
        
    # Manage 3D plot
    def plot_all_3d(self):
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
            color=colors)
        
        # Get choosen file
        MyLayout.text_file_plt(self)

        if MyLayout.data_path:

            # Get choosen joints
            joints = [self.ids.hip_check_3d.active,
                      self.ids.l_thigh_check_3d.active,
                      self.ids.l_shin_check_3d.active,
                      self.ids.l_foot_check_3d.active,
                      self.ids.r_thigh_check_3d.active,
                      self.ids.r_shin_check_3d.active,
                      self.ids.r_foot_check_3d.active,
                      self.ids.l_toe_check_3d.active,
                      self.ids.r_toe_check_3d.active]

            # If no file is selected teake the first one
            if MyLayout.n_file == 0:
                self.ids.f_label_zero.background_color[3] = 0.4

            # Plot legend on check boxes
            MyLayout.set_joint_color_3d(self, joints)

            # Compute position
            take, pos_joint = MyLayout.compute_pos_3d(self)

            # Select joints
            selc_joints, legend = get_joints(pos_joint, joints, MyLayout.legend)

            # Set slider max value
            if MyLayout.set_frame == -1 and True in joints:
                self.ids.slider_3d.max = len(selc_joints[0])
                self.ids.slider_3d.value = len(selc_joints[0])

            # PLOT
            MyLayout.plot_3d(self, selc_joints, legend, take)
        
    # 3D check box
    def select_all_3d(self):
        
        if self.ids.button_sel_3d.text == "[b]Check all[/b]":
            # Select all boxes
            self.ids.hip_check_3d.active = True
            self.ids.l_thigh_check_3d.active = True
            self.ids.l_shin_check_3d.active = True
            self.ids.l_foot_check_3d.active = True
            self.ids.r_thigh_check_3d.active = True
            self.ids.r_shin_check_3d.active = True
            self.ids.r_foot_check_3d.active = True
            self.ids.l_toe_check_3d.active = True
            self.ids.r_toe_check_3d.active = True
            self.ids.button_sel_3d.text = "[b]Uncheck all[/b]"
        else:
            
            # Deselect all boxes
            self.ids.hip_check_3d.active = False
            self.ids.l_thigh_check_3d.active = False
            self.ids.l_shin_check_3d.active = False
            self.ids.l_foot_check_3d.active = False
            self.ids.r_thigh_check_3d.active = False
            self.ids.r_shin_check_3d.active = False
            self.ids.r_foot_check_3d.active = False
            self.ids.l_toe_check_3d.active = False
            self.ids.r_toe_check_3d.active = False
            self.ids.button_sel_3d.text = "[b]Check all[/b]"

    # Manage 3D check bos color for labelling
    def set_joint_color_3d(self, joints):
        count = 0
        if joints[0]:
            self.ids.hip_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.hip_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[1]:
            self.ids.l_thigh_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_thigh_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[2]:
            self.ids.l_shin_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_shin_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[3]:
            self.ids.l_foot_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_foot_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[4]:
            self.ids.r_thigh_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_thigh_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[5]:
            self.ids.r_shin_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_shin_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[6]:
            self.ids.r_foot_text_3d.background_color=  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_foot_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[7]:
            self.ids.l_toe_text_3d.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_toe_text_3d.background_color = (1, 237/255, 237/255, 1)
        if joints[8]:
            self.ids.r_toe_text_3d.background_color=  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_toe_text_3d.background_color = (1, 237/255, 237/255, 1)

    # Manage 3D slider 
    def slide_it_3d(self, *args):
        MyLayout.set_frame = int(args[1])
        if MyLayout.slider:
            MyLayout.plot_all_3d(self)


class App2(App):
    def build(self):
        Window.clearcolor = (1, 237/255, 237/255, 1)
        self.title = 'Gait Analysis'
        return MyLayout()

if __name__ == "__main__":
    App2().run()
    