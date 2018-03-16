import pygame
import random

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [1000, 1000]
screen = pygame.display.set_mode(size)
# Set the screen background
screen.fill(white)

# Set title of screen
pygame.display.set_caption("Random Maze")

# Create a 2 dimensional array. A two dimensional
# array in our implementation is simply a list of lists.
# Each cell corresponds to a 5 pixel x 5 pixel area of the screen surface.
mazegrid = []
for row in range(200):
    # Add an empty array that will hold each cell in this row
    mazegrid.append([])
    for column in range(200):
        mazegrid[row].append(0)  # Append a cell

# Code to be implemented
# 0 = floor
# 1 = wall
# 2 = door
def GenerateMaze(mazegrid):
    # Places walls around the outside of the maze
    sizeoflist = (len(mazegrid) - 1)
    for i in range(len(mazegrid)):
        mazegrid[i][0] = 1
        mazegrid[i][sizeoflist] = 1
    for j in range(len(mazegrid[0])):
        mazegrid[0][j] = 1
        mazegrid[sizeoflist][j] = 1

    # Places a door in the corner of the room
    mazegrid[0][0] = 0
    mazegrid[0][1] = 0
    mazegrid[1][0] = 0

    AddWalls(mazegrid, [(0, 0), (sizeoflist, sizeoflist)], True)


def AddWalls(mazegrid, roomcoords, cheeseflag):
    # Selecting the corners of the room
    topx = roomcoords[0][0]
    topy = roomcoords[0][1]
    bottomx = roomcoords[1][0]
    bottomy = roomcoords[1][1]

    if ((bottomx - topx) > 5) and ((bottomy - topy) > 5):
        # Randomly selects a spot in between the x and y axis of the room
        # the recursion algorithm is in
        x = random.randrange(topx + 2, bottomx - 1)
        y = random.randrange(topy + 2, bottomy - 1)

        # Adds a wall along x and y axis in list
        for i in range(bottomy - topy):
            mazegrid[topy + i][x] = 1
        for i in range(bottomx - topx):
            mazegrid[y][topx + i] = 1

        # Changes the center point of the newly added wall to floor
        mazegrid[y][x] = 0
        mazegrid[y][x - 1] = 0
        mazegrid[y][x + 1] = 0
        mazegrid[y - 1][x] = 0
        mazegrid[y + 1][x] = 0

        # Places the cheese in the very end room
        if topx >= 195 and topy >= 195:
            cheeseflag = True

        AddWalls(mazegrid, [(topx, topy), (x, y)], False) # Top Left Quadrant
        AddWalls(mazegrid, [(x, topy), (bottomx, y)], False) # Top Right Quadrant
        AddWalls(mazegrid, [(topx, y), (x, bottomy)], False) # Bottom Left Quadrant
        AddWalls(mazegrid, [(x, y), (bottomx, bottomy)], cheeseflag) # Bottom Right Quadrant
    else:
        # Places the cheese
        if cheeseflag == True:
            x = random.randrange(topx + 1, bottomx)
            y = random.randrange(topy + 1, bottomy)

            mazegrid[y][x] = 2


def DrawLine(x, y, colour, screen):
    pygame.draw.rect(screen, colour, [x, y, 5, 5])


# We had to add spacing to each i and j value due to the size of the
# screen. The 200 x 200 list aze need to be blown up to fit
# onto the 1000 x 1000 screen
def DisplayMaze(mazegrid):
    j = 0
    jspacing = 0
    while j < len(mazegrid):
        i = 0
        ispacing = 0
        while i < len(mazegrid):
            var = mazegrid[j][i]
            if var == 1:
                DrawLine(i + ispacing, j + jspacing, black, screen)
            elif var == 2:
                DrawLine(i + ispacing, j + jspacing, green, screen)
            i = i + 1
            ispacing = ispacing + 4
        j = j + 1
        jspacing = jspacing + 4
        pygame.display.flip()


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

######################################
# -------- Main Program Loop -----------
while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:  # If user wants to perform an action
            if event.key == pygame.K_m:
                GenerateMaze(mazegrid)
                DisplayMaze(mazegrid)

    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# If you forget this line, the program will 'hang' on exit.
pygame.quit()
