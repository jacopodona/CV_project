# CV_project
The repository contains the Computer Vision project done by Jacopo Donà and Leonardo Fornalè
The following repository contains two separate projects:
 -	guy.py
	 - Displays a graphical user interface with plots of 2D and 3D trajectories of takes
 - skeleton_matplotlib.py
	 - Console script that allows the visualization and animation of motion capture takes using 3D matplotlib
	 
Mocap takes are taken from the `data` directory, additional takes can be inserted and analyzed by the programs, the only supported format is .csv and the takes must be inserted inside the directory for a correct analisys by the programs.

## Required libraries
In order to execute the two programs, the following libraries are necessary:
 - Kivy
	 - Library for the gui development
	 - `pip install kivy`
 - Kivy-garden
	 - Library for the addon management for kivy
	 - `pip install kivy-garden`
 - Matplolib addon for kivy
	 - `garden install matplotlib`
 - Matplotlib
	 - Library used for the visualization of graphical plots
	 -  During our installation, we had troubles understanding how matplolib interacts with the kivy-garden addon
	 - If you are having trouble running the gui having matplotlib already installed, we recommend uninstalling and reinstalling matplotlib **after** having installed the garden addon
	 - `pip uninstall matplotlib` if already installed
	 - `pip install matplotlib`


