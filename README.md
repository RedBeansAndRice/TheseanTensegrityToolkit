# TheseanTensegrityToolkit
 

 
The Thesean Tensegrity Toolkit is a basic toolkit for procedurally generating tensegrity structures and evolving corresponding policies for actuation of the tensile members which simulate the behavior of this category of soft-bodied robots with the goal of producing structures of embodied intelligence with an effective framework for autonomous navigation.

It currently consists of four python scripts, two houdini files(one as a permanent backup), three csv's for logging evolutionary data and three folders: one for saving results to, which contains another for saving graphs(which can be automated), and the last for replacing the simulated file to get around a known bug in Houdini's cache maintenance protocol.

# Motivations

A key goal of the Thesean Tensegrity Toolkit is to highlight some of the potential benefits of simulated robotic tensegrity actuation research using leading VFX industry procedural simulation pipeline production software. The ability to easily reconfigure any of the many complex node structures such as solvers for wind, fluids or combustion is specifically designed for the purpose of leveraging a wealth of carefully configured and constantly evolving procedural modeling and simulation tools built with an eye towards generating useful performance profiles applicable to a wide variety of use cases without getting in the way of stringent customization needs. This makes it easy to generate prototypes and focus on the key scope of a given implementation goal, leaving the tuning of components free to fit the users discretion.

# Getting Started

To start an evolutionary run, navigate into the toolkit folder with command prompt(et al.) and enter "python theseus9000.py".*

That's it!

The fitness values of the evaluated individuals will be output to the "fitnessValues" csv, their genes to the "Tensegrigene" csv and information about the lineage of the selected parent to the "LineageTree" csv.

# Configuring Simulation Settings

To change the simulation settings, open the "TesterTesnegrities2" Houdini file, navigate to the node network display in the bottom right and locate the red and black control node. Clicking on this node should cause the main adjustable parameters of the simulation to appear in the Parameters pane. Currently, the options for models are 0 and 1, corresponding to the spherical icosahderon and the modified tensegrity pelvis respectively. 



The parameters for environment include: 

0- a height map constructed from satelite data of the topology of Western Massachussetts;

1- a flat ground plane;

2- a basic procedural maze generator;

3- a basic stair generator combined with a flat ground plane.

---------------------------------------

When changing the evaluation frame, make sure to change the evaluation frame variable in the theseus9000 script as well. 

Implementing new variable is as easy as making sure they are available to the constraint geometry in the Houdini simulation and adding their name to the list of variables at the beginning of the Genomics script. If the variable implementation is reference in the vellum constraints property node, make sure to update the corresponding code in the HoudiniExpressionizer script so that it isnt replaced by the previous settings when the simulation is generated.

Evolutionary settings, such as number of generations, individuals per generation, genome initialization length range and mutation, addition and deletion rates, can be accessed at the top of the Theseus9000 script. If the program crashes or the program loses track of an evolutionary lineage, remove all incorrectly generated data, set the crash variable in the Theseus9000 script to 1 and run again. Make sure there is no new line at the end of the Tesnegrigene file to ensure correct data processing across available toolkit functionalities.

# Considerations

Houdini defaults to a framerate of 24 fps and the standard meter for the basic distance unit. 

A custom seeded policy can be implemented in the theseus9000 script, but there is no currently implemented function to turn an expression into a genome so this process must be done first by hand.

Due to cache constraints inherent to my hardware and the nature of the project, the active version of the maze generation algorithm is a much "cheaper" knockoff of the original, but uses incomplete maze generation logic so care must be taken to ensure the seed provided produces an effectively equivalent model despite this short-coming. Finding a better compromise between these approaches is a key goal of future work.

*Make sure you've downloaded Houdini and that the Hrender path in the Theseus9000 script matches yours. Python module configurations may be necessary as well.

Special thanks to Junichiro Horikawa for providing the following tutorials which were essential to the creation of this project as well as Ka??a Bradonji?? and Lee Spector for providing academic support.

Tensegrity tutorial:
www.youtube.com/watch?v=BbB82GQjqyU

Maze-Generation tutorial:
www.youtube.com/watch?v=4Za_ROLNrLo
