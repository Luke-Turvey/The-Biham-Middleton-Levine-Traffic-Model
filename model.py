import numpy as np
import pygame
import time
import matplotlib.pyplot as plt

# Parameters to vary in the model are N, p, cell_size

N = 50 # Grid size
p = 0.6 # Total density
cell_size = 10 # Size of each cell (Change to alter size of display)


p_right = 0.5 * p # Density of right cells
p_up = 0.5 * p # Density of up cells

n_right = int(p_right * N**2) # No. of right cells
n_up = int(p_up * N**2) # No. of up cells

n_empty = N**2 - n_right - n_up # No. of empty cells

# Numerical representations of cells in grid matrix
empty_cell = 0
right_cell = 1
up_cell = 2


# Random initilisation of grid for correct densities.
list_grid = [empty_cell] * n_empty + [right_cell] * n_right + [up_cell ] * n_up
grid = np.array(list_grid)
np.random.shuffle(grid)
grid = np.reshape(grid,(N,N))


def traffic_iteration(grid,t,N):
    """This function iterates over the grid matrix and updates the cells according to the rules of the BML Model. It also calculates the average velocity of the up and right 
    cells for each time step"""

    new_grid_list = [empty_cell] * (N**2)
    new_grid = np.array(new_grid_list,dtype=int).reshape((N,N))

    up_velocity_count = 0
    right_velocity_count = 0
    
    for i in range(N):
        for j in range(N):
            if grid[i,j] == empty_cell:
                continue
                
            elif grid[i,j] == right_cell:
                
                if t % 2 == 0:
                    if j < N-1:
                        if grid[i,j+1] == empty_cell:
                            new_grid[i,j+1] = right_cell
                            right_velocity_count += 1
                        else:
                            new_grid[i,j] = right_cell
                    elif j == N-1:
                        if grid[i,0] == empty_cell:
                            new_grid[i,0] = right_cell
                            right_velocity_count += 1
                        else:
                            new_grid[i,j] = right_cell
                else:
                    new_grid[i,j] = right_cell
                        
                
            elif grid[i,j] == up_cell:
                
                if t % 2 == 1:
                    if i > 0:
                        if grid[i-1,j] == empty_cell:
                            new_grid[i-1,j] = up_cell
                            up_velocity_count += 1
                        else:
                            new_grid[i,j] = up_cell
                    elif i == 0:
                        if grid[N-1,j] == empty_cell:
                            new_grid[N-1,j] = up_cell
                            up_velocity_count += 1
                        else:
                            new_grid[i,j] = up_cell
                else:
                    new_grid[i,j] = up_cell

    avg_up_velocity = up_velocity_count / n_up
    avg_right_velocity = right_velocity_count / n_right

    return new_grid, avg_up_velocity, avg_right_velocity


pygame.init()

screen_display = pygame.display.set_mode((cell_size*N,cell_size*N))
clock = pygame.time.Clock()
pygame.display.set_caption("BML Traffic Model")

def draw_grid(array):

    array = np.flip(array)

    # Right cells -> Red
    # Up cells -> Blue
    # Empty cells -> Black

    colours = [(255,255,255),(0,0,255),(255,0,0)]

    for i in range(N):
        for j in range(N):
            pygame.draw.rect(screen_display, colours[array[i][j]], (cell_size*i, cell_size*j, cell_size,cell_size))

iter_grid = grid
t=0

run = True

up_velocities = []
right_velocities = []

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False

    draw_grid(iter_grid)
    pygame.display.flip()
    
    t += 1
    iter_grid, avg_up_velocity, avg_right_velocity = traffic_iteration(iter_grid,t,N)

    if t % 2 == 1:
        up_velocities.append(avg_up_velocity)
    elif t % 2 == 0:
        right_velocities.append(avg_right_velocity)

    clock.tick(10)


pygame.quit()

fig, ax = plt.subplots(figsize = ( 12, 9 ))
ax.set_xlabel("Time",size = 12)
ax.set_ylabel("Average velocity",size = 12)
ax.set_title(f"Average velocity through time, p = {p}, N={N}") 

plt.plot(up_velocities,label = "North Velocities")
plt.plot(right_velocities, label = "East Velocities")
plt.legend()
plt.show()

