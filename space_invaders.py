import pygame
import random
import math

# Initialize pygame
pygame.init()

# Title and icon of the window
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)
# Background music of the window
pygame.mixer.music.load('sound/music.wav')
pygame.mixer.music.play(-1)
# Create the screen and set the background
screen = pygame.display.set_mode((800,800))
background = pygame.image.load('img/background.jpg')

class Score():
    # Class to store the scoreboard 
    def __init__(self):
        # Create a scoreboard located at x,y with value 0 and the given font 
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.x = 340
        self.y = 10

    def update(self):
        # Refresh the scoreboard
        self.display = self.font.render("Score: " + str(self.value), True, (255,255,255))
        screen.blit(self.display, (self.x,self.y))

class GameOver():
    # Class to store the 'Game Over' message
    def __init__(self):
        # Constructor
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.x = 200
        self.y = 250
    
    def show(self):
        # Display the 'Game Over' message
        self.display = self.font.render("GAME OVER!", True, (255, 255, 255))
        screen.blit(self.display, (self.x,self.y))

class Player():
    # Class to store the player
    img = pygame.image.load('img/player.png')

    def __init__(self):
        # Constructor
        self.x = 370
        self.y = 700
        self.x_movement = 0
    
    def move_right(self):
        # Sets self.x_movement to continuously move right
        self.x_movement = 4
    
    def move_left(self):
        # Sets self.x_movement to continuously move left
        self.x_movement = -4
    
    def stop_moving(self):
        # Sets self.x_movement to stop moving
        self.x_movement = 0

    def update(self):
        # Make any necessary movements and show the new player
        self.x += self.x_movement
        self.boundary_check()
        self.show()
    
    def boundary_check(self):
        # Ensures the player stays within the left/right bounds of the screen
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736
    
    def show(self):
        # Displays the player at its current position on the screen
        screen.blit(self.img, (self.x, self.y))

class Invader():
    # Class to store the alien invader object
    img = pygame.image.load('img/invader.png')
    y_shift = 40

    def __init__(self):
        # Constructor simply resets the invader
        self.reset()
    
    def reset(self):
        # Randomize x and y position to respawn within a range
        self.x = random.randint(0,736)
        self.y = random.randint(50,200)
        self.x_movement = 3

    def update(self):
        # Moves the invader in the given direction and updates the position on the screen
        self.x += self.x_movement
        self.boundary_check()
        self.show()

    def boundary_check(self):
        # Moves the invader down and changes horizontal direction when it touches the bounds of the screen
        if self.x <= 0:
            self.x_movement = 3
            self.y += self.y_shift
        elif self.x >= 736:
            self.x_movement = -3
            self.y += self.y_shift
    
    def show(self):
        # Displays the invader at its current position on the screen
        screen.blit(self.img, (self.x, self.y))
    
    def game_over_check(self):
        # Checks if the invader has reached too close to the bottom of the screen
        if self.y > 660:
            return True
        else:
            return False

class Bullet():
    # Class to store the bullet object
    img = pygame.image.load('img/bullet.png')
    fire_sound = pygame.mixer.Sound('sound/fire.wav')
    explode_sound = pygame.mixer.Sound('sound/explode.wav')
    y_shift = 4

    def __init__(self):
        # Constructor
        self.x = 370
        self.reset()
    
    def reset(self):
        # Resets the bullet state and moves it to the bottom of the screen
        self.state = "loaded"
        self.y = 700

    def did_hit(self, invader):
        # Checks if the bullet collided with an invader
        distance = math.sqrt(((invader.x-self.x)**2) + ((invader.y-self.y)**2))
        if distance < 27:
            self.explode_sound.play()
            return True
        else:
            return False
    
    def fire(self, player):
        # Fires the bullet if it is available to fire
        if self.state is "loaded":
            self.fire_sound.play()
            self.x = player.x
            self.y = player.y
            self.state = "fired"
    
    def update(self):
        # Updates the bullet's position on the screen
        if self.state is "fired":
            if self.y <= 0:
                self.reset()
            else:
                self.show()
                self.y -= self.y_shift

    def show(self):
        # Displays the bullet at its given position on the screen
        screen.blit(self.img, (self.x+16, self.y+10))

# Game variables
player = Player()
num_invaders = 6
invaders = [Invader() for i in range(num_invaders)]
bullet = Bullet()
score = Score()

loop = True

# Game loop
while loop:

    screen.fill((0,0,0))                # Reset the screen to black
    screen.blit(background, (0,0))      # Place the background on the black screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Exit the game on close
            loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Move the player left on left key press
                player.move_left()
            if event.key == pygame.K_RIGHT: # Move the player right on right key press
                player.move_right()
            if event.key == pygame.K_SPACE: # Fire the bullet on space key press
                bullet.fire(player)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   # When key lifted, stop moving player
                player.stop_moving()

    # Update and refresh game variables on the screen
    player.update()
    bullet.update()
    for invader in invaders:
        # Check if game over
        game_over = invader.game_over_check()
        if game_over:
            for invader in invaders:
                invader.y = 2000
            message = GameOver()
            message.show()
            break
        # Else, check if invader was hit
        was_hit = bullet.did_hit(invader)
        if was_hit:
            invader.reset()
            bullet.reset()
            score.value += 1
        # Update invader
        invader.update()
    score.update()

    pygame.display.update()
