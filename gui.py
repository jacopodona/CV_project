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
from optitrack.geometry import *


# Initialization
Window.maximize()
Builder.load_file('gui.kv')

colors = ["indianred", "forestgreen", "royalblue", 
            "darkorange", "aqua", "hotpink", 
            "gold", "darkorchid", "chocolate"]

matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=colors)


class MyLayout(TabbedPanel):
    legend = ['Hip','Left thigh','Left shin','Left foot','Right thigh','Right shin','Right foot','Left toe','Right toe'] 
    set_frame = -1
    slider = False
    save_plt = False
    file_name = ""
    file_name_array = []
    data_path = []
    data_path_sel = []
    my_path = os.path.dirname(__file__)
    color_count = 0
    n_file = 0
    animate = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.spinner_joint.values = MyLayout.legend
        self.ids.filechooser.path = MyLayout.my_path
        

    def selected(self, file_path):
        if file_path:
            MyLayout.file_name = file_path[0]


    def choose_file(self, number):
        if MyLayout.data_path:
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


    def load_data(self):
        if MyLayout.file_name not in MyLayout.data_path and ".csv" in MyLayout.file_name:
            self.ids.load_data_label.add_widget(Label(text =  os.path.basename(MyLayout.file_name),
                                                        font_size = 20))
            MyLayout.data_path.append(MyLayout.file_name)
            
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

            MyLayout.color_count += 1             


    def clear_data(self):
        self.ids.load_data_label.clear_widgets()
        del MyLayout.data_path[:]
        self.ids.graph_x.clear_widgets()
        self.ids.graph_y.clear_widgets()
        self.ids.graph_z.clear_widgets()
        self.ids.graph_xyz.clear_widgets()

        # self.ids.file_manager.clear_widgets()
        MyLayout.color_count = 0

        self.ids.f_label_zero.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_one.background_color = (1, 237/255, 237/255, 1)       
        self.ids.f_label_two.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_three.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_four.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_five.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_six.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_sev.background_color = (1, 237/255, 237/255, 1)
        self.ids.f_label_eigth.background_color = (1, 237/255, 237/255, 1)
        
        self.ids.f_label_zero.text = " "
        self.ids.f_label_one.text = " "
        self.ids.f_label_two.text = " "
        self.ids.f_label_three.text = " "
        self.ids.f_label_four.text = " "
        self.ids.f_label_five.text = " "
        self.ids.f_label_six.text = " "
        self.ids.f_label_sev.text = " "
        self.ids.f_label_eigth.text = " "
        
        self.ids.f_label_zero.disabled = True
        self.ids.f_label_one.disabled = True
        self.ids.f_label_two.disabled = True
        self.ids.f_label_three.disabled = True
        self.ids.f_label_four.disabled = True
        self.ids.f_label_five.disabled = True
        self.ids.f_label_six.disabled = True
        self.ids.f_label_sev.disabled = True
        self.ids.f_label_eigth.disabled = True
        

    def select_all(self):
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


    def select_data_path_from_file(self):
        count = 0
        color = []
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
        
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=color)
            

    def plot_all(self):
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
                                    color=colors)
        if MyLayout.data_path:
            if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":

                joints = [self.ids.hip_check.active,
                        self.ids.l_thigh_check.active,
                        self.ids.l_shin_check.active,
                        self.ids.l_foot_check.active,
                        self.ids.r_thigh_check.active,
                        self.ids.r_shin_check.active,
                        self.ids.r_foot_check.active,
                        self.ids.l_toe_check.active,
                        self.ids.r_toe_check.active]

                if MyLayout.n_file == 0:
                    self.ids.f_label_zero.background_color[3] = 0.4

                # Plot legend
                MyLayout.set_joint_color(self, joints)
        
                # Compute position
                take, pos_joint = MyLayout.compute_pos(self)

                #Select joints
                selc_joints, legend = get_joints(pos_joint, joints, MyLayout.legend)

                # Set slider
                if MyLayout.set_frame == -1 and True in joints:
                    self.ids.slider.max = len(selc_joints[0])
                    self.ids.slider.value = len(selc_joints[0])

                # PLOTS
                MyLayout.plot_x_t(self, selc_joints, legend, take)
                MyLayout.plot_y_t(self, selc_joints, legend, take)
                MyLayout.plot_z_t(self, selc_joints, legend, take)
                MyLayout.plot_xyz(self, selc_joints, legend, take)
            else:
                # MyLayout.data_path.clear()
                MyLayout.data_path_sel.clear()
                joints = []
                take = []
                pos_joint = []
                select_joint = ""
                if self.ids.spinner_joint.text == "Joint":
                    self.ids.spinner_joint.text = MyLayout.legend[0]
            
                # Select joint
                for i in MyLayout.legend:
                    if self.ids.spinner_joint.text == i:
                        joints.append(True)
                        select_joint = i
                    else:
                        joints.append(False)

                if not True in joints and joints:
                    joints[0] = True
                    self.ids.spinner_joint.text = "Hip"

                MyLayout.select_data_path_from_file(self)

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

    
    def compute_pos(self):
        # if MyLayout.data_path
        if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":
            take = csv.Take().readCSV(MyLayout.data_path[MyLayout.n_file])
        else:
            take = csv.Take().readCSV(MyLayout.file_name)
        body = take.rigid_bodies
        pos = get_bone_pos(body, take)
        return take, pos


    def plot_x_t(self, selc_joints, legend, take):
        self.ids.graph_x.clear_widgets()
        fig_x, ax = plt.subplots()

        # Plot all selected joint time vs x 
        for i in range(0, len(selc_joints)):
            path_x, t_x = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_x, t_x, ax, MyLayout.set_frame, "x")
        
        #Plot options
        ax.set_xlabel("t")
        ax.set_ylabel("x")
        if MyLayout.save_plt:
            my_file = 'x_t take.png'
            fig_x.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_x_t = FigureCanvas(fig_x)
        graph_x = self.ids.graph_x
        graph_x.add_widget(plot_x_t)
        

    def plot_x_t_sJoint(self, pos_joint, select_joint, take):
        self.ids.graph_x.clear_widgets()
        fig_x_sJoint, ax_sJoint = plt.subplots()
        for pos_sJoint, take_sJoint in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_x_sJoint, t_x_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_x_sJoint, t_x_sJoint, ax_sJoint, MyLayout.set_frame, "x")

        #Plot options
        ax_sJoint.set_xlabel("t")
        ax_sJoint.set_ylabel("x")
        if MyLayout.save_plt:
            my_file = f'x_t_{select_joint} take.png'
            fig_x_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_x_t_sJoint = FigureCanvas(fig_x_sJoint)
        graph_x = self.ids.graph_x
        graph_x.add_widget(plot_x_t_sJoint)

        
    def plot_y_t(self, selc_joints, legend, take):
        self.ids.graph_y.clear_widgets()
        fig_y, ay=plt.subplots(figsize=plt.rcParams["figure.figsize"][::-1])
        fig_y.subplots_adjust(left=0.1, right=0.875, top=0.9,bottom=0.125)

        # Plot all selected joint time vs y, and rotate the axis
        for i in range(0, len(selc_joints)):
            path_y, t_y = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_y, t_y, ay, MyLayout.set_frame, "y", reverse_axis = True)

        #Plot options
        ay.set_ylabel("t", rotation=90)
        ay.yaxis.tick_right()
        ay.yaxis.set_label_position("right")    
        ay.set_xlabel("y")
        ay.invert_xaxis()
        ay.invert_yaxis()
        if MyLayout.save_plt:
            my_file = 'y_t take.png'
            fig_y.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_y_t = FigureCanvas(fig_y)
        graph_y = self.ids.graph_y
        graph_y.add_widget(plot_y_t)


    def plot_y_t_sJoint(self, pos_joint, select_joint, take):
        self.ids.graph_y.clear_widgets()
        fig_y_sJoint, ay_sJoint = plt.subplots()
        for pos_sJoint, take_sJoint in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_y_sJoint, t_y_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_y_sJoint, t_y_sJoint, ay_sJoint, MyLayout.set_frame, "y", reverse_axis = True)

        #Plot options
        ay_sJoint.set_ylabel("t", rotation=90)
        ay_sJoint.yaxis.tick_right()
        ay_sJoint.yaxis.set_label_position("right")    
        ay_sJoint.set_xlabel("y")
        ay_sJoint.invert_xaxis()
        ay_sJoint.invert_yaxis()
        if MyLayout.save_plt:
            my_file = f'y_t_{select_joint} take.png'
            fig_y_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_y_t_sJoint = FigureCanvas(fig_y_sJoint)
        graph_y = self.ids.graph_y
        graph_y.add_widget(plot_y_t_sJoint)


    def plot_z_t(self, selc_joints, legend, take):
        self.ids.graph_z.clear_widgets()
        fig_z, az = plt.subplots()

        # Plot all selected joint time vs z 
        for i in range(0, len(selc_joints)):
            path_z, t_z = get_marker_path(selc_joints, i, take)
            plot_marker_traj(path_z, t_z, az, MyLayout.set_frame, "z")

        #Plot options
        az.set_xlabel("t")
        az.set_ylabel("z")
        if MyLayout.save_plt:
            my_file = 'z_t take.png'
            fig_z.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_z_t = FigureCanvas(fig_z)
        graph_z = self.ids.graph_z
        graph_z.add_widget(plot_z_t)
       

    def plot_z_t_sJoint(self, pos_joint, select_joint, take):
        self.ids.graph_z.clear_widgets()
        fig_z_sJoint, az_sJoint = plt.subplots()
        for pos_sJoint, take_sJoint  in zip(pos_joint, take):
            for i in range(0, len(pos_sJoint)):
                path_z_sJoint, t_z_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                plot_marker_traj(path_z_sJoint, t_z_sJoint, az_sJoint, MyLayout.set_frame, "z")

        #Plot options
        az_sJoint.set_xlabel("t")
        az_sJoint.set_ylabel("z")
        if MyLayout.save_plt:
            my_file = f'z_t_{select_joint} take.png'
            fig_z_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
        plot_z_t_sJoint = FigureCanvas(fig_z_sJoint)
        graph_z = self.ids.graph_z
        graph_z.add_widget(plot_z_t_sJoint)


    def plot_xyz(self, selc_joints, legend, take):

        if self.ids.multiple_choice.text == "Plot X-Z":
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint time vs z 
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "xz")

            #Plot options
            axyz.set_xlabel("x")
            axyz.set_ylabel("z")
            if MyLayout.save_plt:
                my_file = 'x_z take.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))

            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)

        if self.ids.multiple_choice.text == "Plot X-Y" or self.ids.multiple_choice.text == "Choose the plot":
            self.ids.multiple_choice.text = "Plot X-Y"
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint time vs z 
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "xy")

            #Plot options
            axyz.set_xlabel("x")
            axyz.set_ylabel("y")
            if MyLayout.save_plt:
                my_file = 'x_y take.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))
            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)
        
        if self.ids.multiple_choice.text == "Plot Y-Z":
            self.ids.graph_xyz.clear_widgets()
            fig_xyz, axyz = plt.subplots()

            # Plot all selected joint time vs z 
            for i in range(0, len(selc_joints)):
                path_xyz, t_xyz = get_marker_path(selc_joints, i, take)
                plot_marker_path_2D(path_xyz, axyz, MyLayout.set_frame, "yz")

            #Plot options
            axyz.set_xlabel("y")
            axyz.set_ylabel("z")
            if MyLayout.save_plt:
                my_file = 'y_z take.png'
                fig_xyz.savefig(os.path.join(MyLayout.my_path, my_file))
            plot_xyz = FigureCanvas(fig_xyz)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz)


    def plot_xyz_sJoint(self, pos_joint, select_joint, take):
        
        if self.ids.multiple_choice.text == "Plot X-Z":
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected joint time vs z 
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "xz")

            #Plot options
            axyz_sJoint.set_xlabel("x")
            axyz_sJoint.set_ylabel("z")
            if MyLayout.save_plt:
                my_file = f'x_z_{select_joint} take.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)

        if self.ids.multiple_choice.text == "Plot X-Y" or self.ids.multiple_choice.text == "Choose the plot":
            self.ids.multiple_choice.text = "Plot X-Y"
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected joint time vs z 
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "xy")

            #Plot options
            axyz_sJoint.set_xlabel("x")
            axyz_sJoint.set_ylabel("y")
            if MyLayout.save_plt:
                my_file = f'x_y_{select_joint} take.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)
        
        if self.ids.multiple_choice.text == "Plot Y-Z":
            self.ids.graph_xyz.clear_widgets()
            fig_xyz_sJoint, axyz_sJoint = plt.subplots()

            # Plot all selected joint time vs z 
            for pos_sJoint, take_sJoint  in zip(pos_joint, take):
                for i in range(0, len(pos_sJoint)):
                    path_xyz_sJoint, t_xyz_sJoint = get_marker_path(pos_sJoint, i, take_sJoint)
                    plot_marker_path_2D(path_xyz_sJoint, axyz_sJoint, MyLayout.set_frame, "yz")

            #Plot options
            axyz_sJoint.set_xlabel("y")
            axyz_sJoint.set_ylabel("z")
            if MyLayout.save_plt:
                my_file = f'y_z_{select_joint} take.png'
                fig_xyz_sJoint.savefig(os.path.join(MyLayout.my_path, my_file))
            plot_xyz_sJoint = FigureCanvas(fig_xyz_sJoint)
            graph_xyz = self.ids.graph_xyz
            graph_xyz.add_widget(plot_xyz_sJoint)


    def set_joint_color(self, joints):
        count = 0
        if joints[0]:
            self.ids.hip_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.hip_text.background_color = (1, 237/255, 237/255, 1)
        if joints[1]:
            self.ids.l_thigh_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_thigh_text.background_color = (1, 237/255, 237/255, 1)
        if joints[2]:
            self.ids.l_shin_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_shin_text.background_color = (1, 237/255, 237/255, 1)
        if joints[3]:
            self.ids.l_foot_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_foot_text.background_color = (1, 237/255, 237/255, 1)
        if joints[4]:
            self.ids.r_thigh_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_thigh_text.background_color = (1, 237/255, 237/255, 1)
        if joints[5]:
            self.ids.r_shin_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_shin_text.background_color = (1, 237/255, 237/255, 1)
        if joints[6]:
            self.ids.r_foot_text.background_color=  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_foot_text.background_color = (1, 237/255, 237/255, 1)
        if joints[7]:
            self.ids.l_toe_text.background_color =  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.l_toe_text.background_color = (1, 237/255, 237/255, 1)
        if joints[8]:
            self.ids.r_toe_text.background_color=  matplotlib.colors.to_rgba(colors[count], alpha=None)
            count += 1
        else:
            self.ids.r_toe_text.background_color = (1, 237/255, 237/255, 1)
    

    def slide_it(self, *args):
        MyLayout.set_frame = int(args[1])
        if MyLayout.slider:
            MyLayout.plot_all(self)


    def auto_update(self):
        if self.ids.auto_update_label.text == "[b]Enable auto-update[/b]":
            self.ids.auto_update_label.text = "[b]Disable auto-update[/b]"
            MyLayout.slider = True
        else:
            self.ids.auto_update_label.text = "[b]Enable auto-update[/b]"
            MyLayout.slider = False


    def save_plts(self):
        MyLayout.save_plt = True
        MyLayout.plot_all(self)
        MyLayout.save_plt = False


    def plot_3d(self, selc_joints, legend, take):
        print("Selected joints:",len(selc_joints))
        fig_3d = self.ids.graph_3d.clear_widgets()

        #fig_3d, ax = plt.subplots()

        fig_3d = plt.figure(figsize=(8, 4))
        ax = fig_3d.add_subplot(111, projection='3d')

        
        if not MyLayout.animate:
            # Plot all selected joint 3d positions
            for i in range(0, len(selc_joints)):
                path_3d, t = get_marker_path(selc_joints, i, take)
                plot_marker_path_3D(path_3d, ax, MyLayout.set_frame)
            
            plot_3d_Joint = FigureCanvas(fig_3d)
            graph_3d = self.ids.graph_3d
            graph_3d.add_widget(plot_3d_Joint)
        else:
            pass
            # 
            # path_tmp = []
            # # Plot all selected joint 3d position Aniamtion
            # for i in range(0, len(selc_joints)):
            #     path_3d, t = get_marker_path(selc_joints, i, take)
            #     path_tmp.append(path_3d)

            # for j in range(0, MyLayout.set_frame, 1000):
            #     self.ids.graph_3d.clear_widgets()
            #     for path in path_tmp:
            #         plot_marker_path_3D(path, ax, j)
            #     plot_3d_Joint = FigureCanvas(fig_3d)
            #     graph_3d = self.ids.graph_3d
            #     graph_3d.add_widget(plot_3d_Joint)
            #     time.sleep(1)

        


    def plot_all_3d(self):
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(
            color=colors)
        if MyLayout.data_path:
            #if self.ids.multi_graph.text == "[b]Enable multiple\nfile joint[/b]":
            joints = [self.ids.hip_check_3d.active,
                      self.ids.l_thigh_check_3d.active,
                      self.ids.l_shin_check_3d.active,
                      self.ids.l_foot_check_3d.active,
                      self.ids.r_thigh_check_3d.active,
                      self.ids.r_shin_check_3d.active,
                      self.ids.r_foot_check_3d.active,
                      self.ids.l_toe_check_3d.active,
                      self.ids.r_toe_check_3d.active]

            if MyLayout.n_file == 0:
                self.ids.f_label_zero.background_color[3] = 0.4

            # Plot legend
            MyLayout.set_joint_color_3d(self, joints)

            # Compute position
            take, pos_joint = MyLayout.compute_pos(self)

            # Select joints
            selc_joints, legend = get_joints(pos_joint, joints, MyLayout.legend)

            # Set slider
            if MyLayout.set_frame == -1 and True in joints:
                self.ids.slider_3d.max = len(selc_joints[0])
                self.ids.slider_3d.value = len(selc_joints[0])

            # PLOTS
            MyLayout.plot_3d(self, selc_joints, legend, take)
            """else:
                print("Route 2")
                # MyLayout.data_path.clear()
                MyLayout.data_path_sel.clear()
                joints = []
                take = []
                pos_joint = []
                select_joint = ""
                if self.ids.spinner_joint.text == "Joint":
                    self.ids.spinner_joint.text = MyLayout.legend[0]

                # Select joint
                for i in MyLayout.legend:
                    if self.ids.spinner_joint.text == i:
                        joints.append(True)
                        select_joint = i
                    else:
                        joints.append(False)

                if not True in joints and joints:
                    joints[0] = True
                    self.ids.spinner_joint.text = "Hip"

                MyLayout.select_data_path_from_file(self)

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
                        if len(i[0]) < self.ids.slider_3d.max or first == True:
                            self.ids.slider_3d.max = len(i[0])
                            self.ids.slider_3d.value = len(i[0])
                            first = False

                # PLOTS
                MyLayout.plot_3d(self, pos_joint, select_joint, take)"""


    def select_all_3d(self):
        if self.ids.button_sel_3d.text == "[b]Check all[/b]":
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


    def slide_it_3d(self, *args):
        MyLayout.set_frame = int(args[1])
        if MyLayout.slider:
            MyLayout.plot_all_3d(self)


    def animation(self):
        if self.ids.button_animate_3d.text == "[b]Activate animation[/b]":
            MyLayout.animate = True
            self.ids.button_animate_3d.text = "[b]Deactivate animation[/b]"
        else:
            MyLayout.animate = False
            self.ids.button_animate_3d.text = "[b]Activate animation[/b]"

class App2(App):
    def build(self):
        Window.clearcolor = (1, 237/255, 237/255, 1)
        return MyLayout()

if __name__ == "__main__":
    App2().run()