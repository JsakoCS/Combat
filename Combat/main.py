# Imports ...
import pygame
from pygame import mixer
from combatant import Combatant

# Initialize pygame and mixer ...
mixer.init()
pygame.init()

# Set the game window size ...
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
# Create the game window ...
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Give the game window a title ...
pygame.display.set_caption("C o m b a t")

# Set the frame rate ...
clock = pygame.time.Clock()
FPS = 60

# Define colors ...
RED = (136, 8, 8)
GREEN = (155, 229, 170)
BLACK = (0, 0, 0)

# Define game variables ...
start_count = 3
finish_count = pygame.time.get_ticks()
score = [0, 0]   # [ Player1 , Player2 ] .
round_over = False
round_over_cooldown = 2500

# Define combatant variables ...
combatant1_size = 250
combatant1_scale = 3.29
combatant1_offset = [114, 114]
combatant1_data = [combatant1_size, combatant1_scale, combatant1_offset]
combatant2_size = 162
combatant2_scale = 3.9
combatant2_offset = [74, 56]
combatant2_data = [combatant2_size, combatant2_scale, combatant2_offset]

# Load music and sounds ...
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1, 0.0, 5000)
magic_staff_audio = pygame.mixer.Sound("assets/audio/magic_staff.wav")
magic_staff_audio.set_volume(0.5)
sword_audio = pygame.mixer.Sound("assets/audio/sword.wav")
sword_audio.set_volume(0.5)
# Load background image ...
background = pygame.image.load("assets/images/background/background.png").convert_alpha()
# Load sprite sheets ...
combatant1_sheet = pygame.image.load("assets/images/combatant1/sprites/spritesheet1.png").convert_alpha()
combatant2_sheet = pygame.image.load("assets/images/combatant2/sprites/spritesheet2.png").convert_alpha()
# Load victory image ...
victory_image = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define the animations ...
combatant1_animations = [8, 8, 1, 8, 8, 3, 7]
combatant2_animations = [10, 8, 1, 7, 7, 3, 7]

# Define font ...
count_font = pygame.font.Font("assets/fonts/abyssal_horrors.ttf", 50)
score_font = pygame.font.Font("assets/fonts/abyssal_horrors.ttf", 25)

# Function for drawing the text ...
def draw_text(text, font, text_color, x, y):
    text_image = font.render(text, True, text_color)
    game_window.blit(text_image, (x, y))

# Function for drawing the background ...
def draw_background():
    scaled_background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    game_window.blit(scaled_background, (0, 0))

# Function for drawing the health bars ...
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(game_window, BLACK, (x - 3, y - 3, 406, 39))
    pygame.draw.rect(game_window, RED, (x, y, 400, 33))
    pygame.draw.rect(game_window, GREEN, (x, y, 400 * ratio, 33))

# Create two instances of combatants ...
combatant_1 = Combatant(1, 0, 265, False, combatant1_data, combatant1_sheet, combatant1_animations, magic_staff_audio)
combatant_2 = Combatant(2, 0, 265, True, combatant2_data, combatant2_sheet, combatant2_animations, sword_audio)

# Position the combatants evenly on the game window ...
offset = 0   # The distance away from the game window border (shown visually as offset plus combatant width) .
# Calculate the x position for the first combatant ...
combatant1_width = combatant_1.rect.width
combatant1_x = offset + combatant1_width
# Calculate the x position for the second combatant ...
combatant2_width = combatant_2.rect.width
combatant2_x = WINDOW_WIDTH - offset - combatant2_width - combatant1_width
# Update the x position of the combatant instances ...
combatant_1.rect.x = combatant1_x
combatant_2.rect.x = combatant2_x
# Print the combatant positions ...
# print("Combatant 1 x position:", combatant1_x)
# print("Combatant 2 x position:", combatant2_x)

# Game loop ...
run = True
while run:
    # Set the frame rate ...
    clock.tick(FPS)

    # Draw the background ...
    draw_background()

    # Draw the health bars ...
    draw_health_bar(combatant_1.health, 20, 20)
    draw_health_bar(combatant_2.health, 580, 20)

    # Show player stats ...
    draw_text("Player1   :   " + str(score[0]), score_font, BLACK, 20, 60)
    draw_text("Player2   :   " + str(score[1]), score_font, BLACK, 580, 60)

    # Update the countdown ...
    if start_count <= 0:
        # Provide actions for the combatants ...
        combatant_1.action(WINDOW_WIDTH, WINDOW_HEIGHT, game_window, combatant_2, round_over)
        combatant_2.action(WINDOW_WIDTH, WINDOW_HEIGHT, game_window, combatant_1, round_over)
    else:
        # Display the count timer ...
        draw_text(str(start_count), count_font, BLACK, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3)
        # Update the count timer ...
        if (pygame.time.get_ticks() - finish_count) >= 1000:
            start_count -= 1
            finish_count = pygame.time.get_ticks()

    # Update the combatants ...
    combatant_1.update()
    combatant_2.update()

    # Draw the combatants ...
    combatant_1.draw(game_window)
    combatant_2.draw(game_window)

    # Check for defeat ...
    if round_over is False:
        if combatant_1.alive is False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif combatant_2.alive is False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Victory ...
        game_window.blit(victory_image, (226.5, 100))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            start_count = 3
            # Create two instances of combatants ...
            combatant_1 = Combatant(1, 0, 265, False, combatant1_data, combatant1_sheet, combatant1_animations, magic_staff_audio)
            combatant_2 = Combatant(2, 0, 265, True, combatant2_data, combatant2_sheet, combatant2_animations, sword_audio)
            # Position the combatants evenly on the game window ...
            offset = 0   # The distance away from the game window border (shown visually as offset plus combatant width) .
            # Calculate the x position for the first combatant ...
            combatant1_width = combatant_1.rect.width
            combatant1_x = offset + combatant1_width
            # Calculate the x position for the second combatant ...
            combatant2_width = combatant_2.rect.width
            combatant2_x = WINDOW_WIDTH - offset - combatant2_width - combatant1_width
            # Update the x position of the combatant instances ...
            combatant_1.rect.x = combatant1_x
            combatant_2.rect.x = combatant2_x

    # Event handler ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the display ...
    pygame.display.update()

# Exit pygame ...
pygame.quit()