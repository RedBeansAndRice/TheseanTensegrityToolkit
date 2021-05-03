# TheseanTensegrityToolkit
 
The Thesean Tensegrity Toolkit is a basic toolkit for procedurally generating tensegrity structures and evolving corresponding policies for actuation of the tensile members which simulate the behavior of this category of soft-bodied robots with the goal of producing structures of embodied intelligence with an effective framework for autonomous navigation.

It currently consists of four python scripts, two houdini files(one as a permanent backup), three csv's for logging evolutionary data and three folders, one for saving results to, which contains another for saving graphs(which can be automated), and the last for replacing the simulated file to get around a known bug in Houdini's cache maintenance protocol.

To start an evolutionary run, navigate into the toolkit folder with command prompt(et al.) and enter "python theseus9000.py".

That's it!

The fitness values of the evaluated individuals will be output to the "fitnessValues" csv, their genes to the "Tensegrigene" csv and information about the lineage of the selected parent to the "LineageTree" csv.

To change the simulation settings, open the "TesterTesnegrities2" Houdini file, navigate to the node network display in the bottom right and locate the red and black control node. Clicking on this node should cause the main adjustable parameters of the simulation to appear in the Parameters pane. Currently, the options for models are 0 and 1, corresponding to the spherical icosahderon and the modified tensegrity pelvis respectively. The parameters for environment include: 0, a height map constructed from satelite data of the topology of Western Massachussetts; 1, a flat ground plane(be sure to re-check ground position on the vellum solver when using this setting); 2, a basic procedural maze generator.
When changing the evaluation frame, make sure to change the evaluation frame variable in the theseus9000 script as well. 

A custom seeded policy can be implemented in the theseus9000 script, but there is no currently implemented function to turn an expression into a genome so this process must be done first by hand.
