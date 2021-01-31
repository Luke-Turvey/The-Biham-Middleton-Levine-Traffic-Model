# The Biham Middleton Levine Traffic Model
The BML Traffic Model is an extremely simple cellular automaton rule involving deterministic motion in discrete time of "cars" located on the cells of a square grid. Despite its simplicity and popularity, very little is known rigorously. Particularly mysterious are the phenomena of phase transition and self-organization on the infinite grid.

#### How does the BML Traffic Model traffic model work?

Each intersection of a square grid of streets contains either an East-facing car, a North-facing car, or an empty space. At each odd-numbered time step, all the North-facing cars simultaneously attempt to move one unit North; a car succeeds if there is already an empty space for it to move into. At each even-numbered time step, the East-facing cars attempt to move East in the same way.

Initially, cars are distributed at random: each intersection is independently assigned a car with probability p, or an empty space with probability 1 - p. Each is car is independently equally likely to be East-facing or North-facing.

#### How does my model simulate this?

In my model the grid of streets is a matrix with integer elements (0,1 or 2). 

0 signifies an empty space, 1 signifies an East-facing car, 2 signifies a North-facing car

The model then runs through each element of the matrix and checks if the the cell above it or to the right of it is clear (depending on what the element contains) and then updates a new matrix to the new positions of the cars after 1 iteration. This new matrix is then copied over the old matrix and the process repeats.

When initialising the model you can choose a boundary condition (periodic or non-periodic). A periodic boundary condition means cars who go off the right and top edges of the grid come back in on the bottom of the grid. Non-periodic boundary conditions means cars who go off the right and top edges of the grid disappear.

