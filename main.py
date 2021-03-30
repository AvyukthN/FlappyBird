import pygame
import sys
from PIL import Image
import random

# these are constants like the window width, height etc. It is a standard to create constants with all captial letters
WIDTH = 500
HEIGHT = 800
# we are creating a SIZE variable for the size of the window here.
# We store WIDTH and HEIGHT of the window in a tuple becase tuples are immutable
# tuples function the same way lists do
SIZE = (WIDTH, HEIGHT)

# in pygame we must always have an init function and a quit function (you will learn about this in our python advanced class)
pygame.init()

# this creates the pygame window/display for us to see the game in
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Flappy Bird")

# =====================================COLORS=================================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# =====================================ASSETS=================================================

# this loads the flappy bird image into a variable bird so we it's easier to reference later in our code
bird_img = pygame.image.load('assets/bird.png')
# this finds the dimensions of the flappy bird image using the Image class from the PIL module
bird_image = Image.open('assets/bird.png')
bird_width = bird_image.width
bird_height = bird_image.height

# ==================================GAME FUNCTIONS============================================

"""
What functions do we need?

1. A function to draw our bird
   Parameters
   - position of bird (x, y)
   - the bird image
   
2. A function to draw the pipes
   Parameters
   - position of the pipes (x, y)
   - height of the pipes => h
   - width of the pipes => w
   - space between the pipes (where the bird has to go through)
   
3. A function to show the current score
    Parameters
    - the current score
    
4. A function to put it all together
   Parameters
   - None
"""

def draw_bird(image, x_pos, y_pos):
    # the blit function lets us put images on our display surface which is our window variable
    # the blit function has these parameters (source, dest, *many others we won't be using*)
    # the source parameter is what we're actually putting on the window, and dest is the position of the source
    window.blit(image, (x_pos, y_pos))
def draw_pipes(x_pos, y_pos, pipe_width, pipe_height, gap_size):
    # we will have to draw two rectangles for these pipes for the top and bottom pipe
    # to do this we can use the pygame.draw.rect() function
    # it takes these parameters (surface, color, rect)
    # surface is the window we're drawing it on, color is the color of the rectangle
    # and rect is a list of the position and dimensions of the rectangle in this order
    # => (x_pos, y_pos, width, height)
    pygame.draw.rect(window, GREEN, [x_pos, y_pos, pipe_width, pipe_height])
    # ^ this is the rectangle on the bottom of the screen
    pygame.draw.rect(window, GREEN, [x_pos, y_pos + pipe_height + gap_size, pipe_width, HEIGHT])
    # ^ this is the reactangle on the top of the screen, the y_pos is the sum of the full pipe height
    # plus the height of the gap and the yposition of the pipe
    # the height of the pipe is the height of the surface because the pipe should extend from its starting
    # point at the end of the gap to the highest part of the game window
def show_score(current_score):
    font = pygame.font.Font('font.ttf', 20)
    text = font.render('Current Score - {}'.format(current_score), True, WHITE)
    window.blit(text, [3, 3])
    # the [3, 3] is the area of the text
def main():
    # initialzing the position of the bird at the start of the game
    bird_pos_x = 150
    bird_pos_y = 300
    bird_jump = 0

    # initializing width and height of the pipes
    pipe_pos_x = WIDTH
    pipe_pos_y = 0
    # initialzing pipe widths and heights
    pipe_width = 40
    # the random.randint() function generates a random number from the first paramater to the second parameter
    # we need to generate a pipe height from 0 to 1/2 of our window height to make the game playable
    # the // operator is the same as the / operator (it divides).
    # However when it rounds the quotient up to the highest possible integer
    # This is called floor division
    pipe_height = random.randint(0, HEIGHT // 2)
    gap_size = bird_height + 200

    current_score = 0
    # here we are creating a variable "quitgame" that can be toggled to True in our While loop if we want to quit the game
    quitgame = False

    # initializing speed of the pipes (this is how fast the pipes will come towards the bird in our game
    pipe_speed = 0.65

    """
    we can see that the while loop will not run now if quitGame is = True
    to ensure this, we can create a for loop that loops through all "events" in our pygame program
    for each event we can check if the event is a call to quit pygame (clicking the red x in the upper right corner of the pygame window)
    if the event is a QUIT request (pygame.QUIT) we will "toggle" or set our quitgame variable to True
    this will break the while loop and end the game
    """
    while quitgame == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame = True
                return 0
            # adding to the jump variable based on user key input
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    bird_jump = 0.5

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_jump = -0.5

        # this will make the game window blue
        window.fill(BLUE)
        # this will display the current score on the game window
        show_score(current_score)
        # this will update the bird's position depending on the key pressed
        bird_pos_y += bird_jump

        # this draws the bird and the pipes using the functions we made earlier
        draw_bird(bird_img, bird_pos_x, bird_pos_y)
        draw_pipes(pipe_pos_x, pipe_pos_y, pipe_width, pipe_height, gap_size)
        # this line will update the x coordinate position of the pipe so it looks like it's moving
        # it will show up in the next frame
        pipe_pos_x -= pipe_speed

        # collision logic for bird and pipes
        # window collision logic
        # this checks to see if the bird touches the top or bottom of the game window
        if (bird_pos_y > (HEIGHT - bird_height)) or (bird_pos_y < 0):
            quitgame = True
        # this checks to see if the pipe is not in the window any more (it has flown past bird or vice versa)
        # and then generates a new pipe
        if pipe_pos_x < (pipe_width * -1):
            pipe_pos_x = WIDTH
            pipe_height = random.randint(0, HEIGHT // 2)
        # Pipe and Bird collision logic
        # this checks if the pipe's horizontal position is greater than the bird's position (meaning the bird past it)
        # and if the horizontal position of the pipe added to its width is greater than the bird's x position
        # meaning that the bird has intersected with the pipe
        # if these are true it will move on to the next condition
        if (pipe_pos_x < (bird_pos_x + bird_width)) and ((pipe_pos_x + pipe_width) > bird_pos_x):
            # this checks if the height of the pipe is greater than the y position of the bird
            # or if the height of the pipe and gap between the pipes together are less than the y position of the bird
            # these conditions both mean that the bird has intersected with the pipe
            # if either are true then the bird has actually touched the pipe and the guitgame variable will be
            # set to True quitting the game by breaking the while True game state loop
            if (pipe_height > bird_pos_y) or ((pipe_height + gap_size) < (bird_height + bird_pos_y)):
                quitgame = True

        if (bird_pos_x > (pipe_pos_x + pipe_width)) and (bird_pos_x < (pipe_pos_x + pipe_width + (bird_width / 5))):
            current_score += 1
        # this checks adds a point to the current score if the bird is past

        # this updates the display to the current game state
        pygame.display.update()



# this line of code will completely quit all running processes from our program after breaking the while loop to ensure the game quits
main()
sys.exit()