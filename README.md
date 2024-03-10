# A-Star Algo Differential Drive main

[Output_part1.webm](https://github.com/nisarg15/A_Star_Differential_Drive/assets/89348092/e3abe392-ad2a-49a4-9aeb-df014614bca1)

The folder contains only one code file named A_star_3.py

The above code file implements A* algorithm on a maze hurdle provided in the assignment

The code accepts start and end goal points from the user listed below, it also accepts starting angle.
The code accepts left RPM,right RPM and clearance

Kindly keep the x start and goal coordinates within 0-400

Kindly keep the y start and goal coordinates within 0-250



With the help of the RPM it generates 8 action set using the below syntax

1. [0, RPM1]
2. [RPM1, 0]
3. [RPM1, RPM1]
4. [0, RPM2]
5. [RPM2, 0]
6. [RPM2, RPM2]
7. [RPM1, RPM2]
8. [RPM2, RPM1]

The radius and length is taken in accordance with Burger Turtle bot

A clearance of 5 pixels have been taken into the consideration

Below are the libraries used

1. Numpy
2. Opencv
3. math
4. Heapq
5. Mathplotlib
6. Copy

Inorder to execute the program, kindly enter the below statement in the terminal

=>python A_star_3.py


#####################################################################

To see the output kindly access the below link

https://drive.google.com/file/d/1PvL2lgPIpWwciS4nJBu1x5MwopwPtT1C/view?usp=sharing
