import pygame
import random
import sys

width = 800
height = 600

cell_size = 5

# i+1 is down
# j+1 is right


# Setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
UPDATE_CELL_LOCATIONS = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_CELL_LOCATIONS, 20)
pygame.display.set_caption('Sand?')

grid = [[0 for _ in range(width // cell_size)] for _ in range(height // cell_size)]
print(f"Using a grid of {len(grid)} by {len(grid[0])}")

# generate next grid
def updateCells(previousGrid):
    currentGrid = [[0] * len(previousGrid[0]) for _ in range(len(previousGrid))]
    currentGrid[len(currentGrid)-1] = previousGrid[len(previousGrid)-1]

    for i in range(len(previousGrid)):
        if i+1 < len(previousGrid):
            for j in range(len(previousGrid[0])):
                if j+1 < len(previousGrid[0]): # not using j+1 lets me use strange cell sizes
                    if previousGrid[i][j] == 1:
                        if previousGrid[i+1][j] == 0: # down gets flipped
                            currentGrid[i+1][j] = 1
                        elif previousGrid[i+1][j-1] == 0 and previousGrid[i+1][j+1] == 0:
                            currentGrid[i+1][j+random.choice([0, 1])] = 1
                        elif previousGrid[i+1][j-1] == 0:
                            currentGrid[i+1][j-1] = 1
                        elif previousGrid[i+1][j+1] == 0:
                            currentGrid[i+1][j+1] = 1
                        else: currentGrid[i][j] = 1

    return currentGrid

def mouse_pos_cell(x, y):
    return (min(x // cell_size, width // cell_size - 1), 
            min(y // cell_size, height // cell_size - 1))

def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
            if grid[i][j] == 1:
                pygame.draw.rect(screen, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), rect=rect)
            else:
                pygame.draw.rect(screen, "black", rect)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0]):
            x, y = pygame.mouse.get_pos()
            # get cell that matches mouse position
            grid_x, grid_y = mouse_pos_cell(x, y)
            grid[grid_y][grid_x] = 1
        if event.type == UPDATE_CELL_LOCATIONS:
            grid = updateCells(grid)

    
    screen.fill("white")
    draw_grid(grid)
    pygame.display.flip()
pygame.quit()
sys.exit()
