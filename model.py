import numpy as np
import pygame
import time
import matplotlib.pyplot as plt

# Parameters to vary in the model are N, p, cell_size
class BML_model():

    def __init__(self,N,p,cell_size = 4, initilisation= "random"):
        self.N = N # Grid size
        self.p = p # Total density
        self.cell_size = cell_size # Size of each cell (Change to alter size of display)


        self.p_right = 0.5 * p # Density of right cells
        self.p_up = 0.5 * p # Density of up cells

        self.n_right = int(self.p_right * N**2) # No. of right cells
        self.n_up = int(self.p_up * N**2) # No. of up cells

        self.n_empty = N**2 - self.n_right - self.n_up # No. of empty cells

        # Numerical representations of cells in grid matrix
        self.empty_cell = 0
        self.right_cell = 1
        self.up_cell = 2

        if initilisation == "random":
            # Random initilisation of grid for correct densities.
            self.list_grid = [self.empty_cell] * self.n_empty + [self.right_cell] * self.n_right + [self.up_cell ] * self.n_up
            self.grid = np.array(self.list_grid)
            np.random.shuffle(self.grid)
            self.grid = np.reshape(self.grid,(self.N,self.N))


    def traffic_iteration(self,t):
        """This function iterates over the grid matrix and updates the cells according to the rules of the BML Model. It also calculates the average velocity of the up and right 
        cells for each time step"""

        self.new_grid_list = [self.empty_cell] * (self.N**2)
        self.new_grid = np.array(self.new_grid_list,dtype=int).reshape((self.N,self.N))

        up_velocity_count = 0
        right_velocity_count = 0
        
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i,j] == self.empty_cell:
                    continue
                    
                elif self.grid[i,j] == self.right_cell:
                    
                    if t % 2 == 0:
                        if j < self.N-1:
                            if self.grid[i,j+1] == self.empty_cell:
                                self.new_grid[i,j+1] = self.right_cell
                                right_velocity_count += 1
                            else:
                                self.new_grid[i,j] = self.right_cell
                        elif j == self.N-1:
                            if self.grid[i,0] == self.empty_cell:
                                self.new_grid[i,0] = self.right_cell
                                right_velocity_count += 1
                            else:
                                self.new_grid[i,j] = self.right_cell
                    else:
                        self.new_grid[i,j] = self.right_cell
                            
                    
                elif self.grid[i,j] == self.up_cell:
                    
                    if t % 2 == 1:
                        if i > 0:
                            if self.grid[i-1,j] == self.empty_cell:
                                self.new_grid[i-1,j] = self.up_cell
                                up_velocity_count += 1
                            else:
                                self.new_grid[i,j] = self.up_cell
                        elif i == 0:
                            if self.grid[self.N-1,j] == self.empty_cell:
                                self.new_grid[self.N-1,j] = self.up_cell
                                up_velocity_count += 1
                            else:
                                self.new_grid[i,j] = self.up_cell
                    else:
                        self.new_grid[i,j] = self.up_cell

        avg_up_velocity = up_velocity_count / self.n_up
        avg_right_velocity = right_velocity_count / self.n_right

        self.grid = self.new_grid

        return avg_up_velocity, avg_right_velocity

    def draw_grid(self,array):

        array = np.flip(array)

        # Right cells -> Red
        # Up cells -> Blue
        # Empty cells -> Black

        colours = [(255,255,255),(0,0,255),(255,0,0)]

        for i in range(self.N):
            for j in range(self.N):
                pygame.draw.rect(self.screen_display, colours[array[i][j]], (self.cell_size*i, self.cell_size*j, self.cell_size,self.cell_size))

    def simulate(self,draw= True, velocity_graphs=True,time_limit = 1000):

        run = True
        
        t = 0

        self.up_velocities = []
        self.right_velocities = []

        if draw:
            pygame.init()

            self.screen_display = pygame.display.set_mode((self.cell_size*self.N,self.cell_size*self.N))
            pygame.display.set_caption("BML Traffic Model")

        while run:
            if draw:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run= False

                self.draw_grid(self.grid)
                pygame.display.flip()
            
            t += 1
            avg_up_velocity, avg_right_velocity = self.traffic_iteration(t)     

            if t % 2 == 1:
                self.up_velocities.append(avg_up_velocity)
            elif t % 2 == 0:
                self.right_velocities.append(avg_right_velocity)

            print(f"Iteration {t}")

            if time_limit == t:
                run=False

        if draw:
            pygame.quit()

        if velocity_graphs:
            fig, ax = plt.subplots(figsize = ( 12, 9 ))
            ax.set_xlabel("Time",size = 12)
            ax.set_ylabel("Average velocity",size = 12)
            ax.set_title(f"Average velocity through time, p = {self.p}, N={self.N}") 

            plt.plot(self.up_velocities,label = "North Velocities")
            plt.plot(self.right_velocities, label = "East Velocities")
            plt.legend()
            plt.show()



bml = BML_model(200,0.5)
bml.simulate(draw=False,velocity_graphs=True)