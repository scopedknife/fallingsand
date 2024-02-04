import pygame, random, math, sys

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
pygame.time.set_timer(UPDATE_CELL_LOCATIONS, 40)
pygame.display.set_caption('Sand?')

grid = [[0 for _ in range(width // cell_size)] for _ in range(height // cell_size)]
print(f"Using a grid of {len(grid)} by {len(grid[0])}")

# generate next grid
def updateCells(previousGrid):
    currentGrid = [[0] * len(previousGrid[0]) for _ in range(len(previousGrid))]
    currentGrid[len(currentGrid)-1] = previousGrid[len(previousGrid)-1] # last row should remain 

    for i in range(len(previousGrid)):
        if i+1 < len(previousGrid):
            for j in range(len(previousGrid[0])):
                if j+1 < len(previousGrid[0]):
                    if previousGrid[i][j] != 0:
                        if previousGrid[i+1][j] == 0:
                            currentGrid[i+1][j] = previousGrid[i][j]
                        elif previousGrid[i+1][j-1] == 0 and previousGrid[i+1][j+1] == 0:
                            currentGrid[i+1][j+random.choice([-1, 1])] = previousGrid[i][j]
                        elif previousGrid[i+1][j-1] == 0:
                            currentGrid[i+1][j-1] = previousGrid[i][j]
                        elif previousGrid[i+1][j+1] == 0:
                            currentGrid[i+1][j+1] = previousGrid[i][j]
                        else: currentGrid[i][j] = previousGrid[i][j]
    return currentGrid

def mouse_pos_cell(x, y):
    return (min(x // cell_size, width // cell_size - 1), 
            min(y // cell_size, height // cell_size - 1))

def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
            if grid[i][j] != 0:
                pygame.draw.rect(screen, color=grid[i][j], rect=rect)
            else:
                pygame.draw.rect(screen, "black", rect)

# yoinked from github lol
scalar = float
def hsv_to_rgb( h:scalar, s:scalar, v:scalar, a:scalar ) -> tuple:
    a = int(255*a)
    if s:
        if h == 1.0: h = 0.0
        i = int(h*6.0); f = h*6.0 - i
        
        w = int(255*( v * (1.0 - s) ))
        q = int(255*( v * (1.0 - s * f) ))
        t = int(255*( v * (1.0 - s * (1.0 - f)) ))
        v = int(255*v)
        
        if i==0: return (v, t, w, a)
        if i==1: return (q, v, w, a)
        if i==2: return (w, v, t, a)
        if i==3: return (w, q, v, a)
        if i==4: return (t, w, v, a)
        if i==5: return (v, w, q, a)
    else: v = int(255*v); return (v, v, v, a)

color_iter = 1
# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            # get cell that matches mouse position
            grid_x, grid_y = mouse_pos_cell(x, y)
            color_iter = (color_iter + 1) % 360
            color = hsv_to_rgb(color_iter/360.0, 1.0, 1.0, 1.0)
            grid[grid_y][grid_x] = color
        if event.type == UPDATE_CELL_LOCATIONS:
            grid = updateCells(grid)

    
    screen.fill("white")
    draw_grid(grid)
    pygame.display.flip()
pygame.quit()
sys.exit()
