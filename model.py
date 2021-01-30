import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clt


N = 200 # Grid size

total_time = 500

p_right = 0.3
p_up = 0.3

n_right = int(p_right * N**2) # No. of right cells
n_up = int(p_up * N**2) # No. of up cells

n_empty = N**2 - n_right - n_up # No. of empty cells

p = p_right + p_up # Total density


empty_cell = 0
up_cell = -1
right_cell = 1

list_grid = [empty_cell] * n_empty + [right_cell] * n_right + [up_cell ] * n_up
grid = np.array(list_grid)
np.random.shuffle(grid)
grid = np.reshape(grid,(N,N))


def traffic_iteration(grid,t,N):
    new_grid_list = [empty_cell] * (N**2)
    new_grid = np.array(new_grid_list,dtype=int).reshape((N,N))
    
    
    for i in range(N):
        for j in range(N):
            if grid[i,j] == empty_cell:
                continue
                
            elif grid[i,j] == right_cell:
                
                if t % 2 == 0:
                    if j < N-1:
                        if grid[i,j+1] == empty_cell:
                            new_grid[i,j+1] = right_cell
                        else:
                            new_grid[i,j] = right_cell
                    elif j == N-1:
                        if grid[i,0] == empty_cell:
                            new_grid[i,0] = right_cell
                        else:
                            new_grid[i,j] = right_cell
                else:
                    new_grid[i,j] = right_cell
                        
                
            elif grid[i,j] == up_cell:
                
                if t % 2 == 1:
                    if i > 0:
                        if grid[i-1,j] == empty_cell:
                            new_grid[i-1,j] = up_cell
                        else:
                            new_grid[i,j] = up_cell
                    elif i == 0:
                        if grid[N-1,j] == empty_cell:
                            new_grid[N-1,j] = up_cell
                        else:
                            new_grid[i,j] = up_cell
                else:
                    new_grid[i,j] = up_cell
                    
    return new_grid



# In this colourmap:
# Right cells -> Red
# Up cells -> Blue
# Empty cells -> White

fig=plt.figure(figsize=(12,8), dpi= 100, facecolor='w', edgecolor='k')

iter_grid = grid

for t in range(1,total_time):
    iter_grid = traffic_iteration(iter_grid,t,N)

plt.imshow(iter_grid,cmap = 'coolwarm')

plt.show()