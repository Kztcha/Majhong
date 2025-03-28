import pygame
import random
import os
pygame.init()
# constants global
w = 900
h = 800
tuile_size = w / (w/70)
screen = pygame.display.set_mode((w, h))
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Rummy Mahjong')
clock = pygame.time.Clock()
BLACK = (0,0,0)
lavender = (150, 131, 236)
color_dark_wood = (101, 67, 33, 128)  # RGB + Alpha for semi-transparency
WHITE = (255, 255, 255)
gold = (255, 215, 0)
RED = (255, 0, 0)
button_color = (255, 160, 122)
button_hover_color = (255, 182, 128)
text_color = (255, 255, 255)

button_width = 300
button_height = 60

# Charger la police
font_path = r"font\Retro_Gaming.ttf"  # Assurez-vous que le chemin est correct
font_size = 40
font = pygame.font.Font(font_path, font_size)
#font bouton
fontbouton_size = 90
fontbouton = pygame.font.Font(font_path, fontbouton_size)
# constants music_menu
background_music_menu = pygame.image.load(r"try\jeu.jpg")
background_music_menu = pygame.transform.scale(background_music_menu, (screen_width, screen_height))
#
background_image = pygame.image.load(r"try\jeu.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
#

background_options = pygame.image.load(r"try\jeu.jpg")
background_options = pygame.transform.scale(background_options, (screen_width, screen_height))


# option menu

image_directory = r"try\imgt"  # Set the path to your image folder
image_files = [img for img in os.listdir(image_directory) if img.endswith(('.png', '.jpg', '.jpeg'))]
images = [pygame.image.load(os.path.join(image_directory, img)) for img in image_files]

images = []
for img in image_files:
    full_path = os.path.join(image_directory, img)
    image = pygame.image.load(full_path)
    scaled_image = pygame.transform.scale(image, (screen_width, screen_height))
    images.append(scaled_image)

aide_button_rect = (screen_width - button_width) // 2, screen_height // 2+20, button_width, button_height

back_button_rect = (screen_width - button_width) // 2, screen_height // 2+button_height*2, button_width, button_height

height_commun = screen_height // 2 - 40
height_commun3 = screen_height - button_height * 2
next_button_rect = pygame.Rect(screen_width // 2 + button_width - fontbouton_size,height_commun3 , fontbouton_size, fontbouton_size)

prev_button_rect = pygame.Rect(screen_width // 2 - button_width, height_commun3, fontbouton_size, fontbouton_size)


backA_button_rect = (screen_width - button_width) // 2, height_commun3 * 1.03, button_width, button_height


incr_volume_button_rect = pygame.Rect(screen_width // 2 + button_width - fontbouton_size,height_commun , fontbouton_size, fontbouton_size)
decr_volume_button_rect = pygame.Rect(screen_width // 2 - button_width, height_commun, fontbouton_size, fontbouton_size)
volume_text_pos = (screen_width // 2, height_commun)


# Setup for the scrolling list
item_height = screen_width / (800/50)
menu_height = screen_height / 4 # We use less than the full height for the menu
visible_items_count = menu_height // item_height  # Number of items that can be visible at once

# constants show_menu
background_show_menu = pygame.image.load(r"try\menu.jpg")
background_show_menu = pygame.transform.scale(background_show_menu, (screen_width, screen_height))
#

# Button positions
vertical_spacing = 20  # Space between buttons

start_rect = (screen_width - button_width) // 2, screen_height // 2 - button_height - vertical_spacing, button_width, button_height
option_rect = (screen_width - button_width) // 2, screen_height // 2, button_width, button_height
quit_rect = (screen_width - button_width) // 2, screen_height // 2 + button_height + vertical_spacing, button_width, button_height


# Préparation des tuiles pour le défilement
tile_images = [pygame.transform.scale(pygame.image.load(f"try/{c}.png"), (tuile_size, tuile_size)) for c in ['1', '2', '3', '4', '5', '6', '7']]
tile_images2 = [pygame.transform.scale(pygame.image.load(f"try/{c}.png"), (tuile_size, tuile_size)) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']]

tile_pos_y = [-i * (tuile_size + 55) for i in range(len(tile_images))]# Positions initiales des tuiles hor7 de l'écran
tile_pos_x = 20  # Position initiale x fixe
tile_pos_x2 = screen_width-(20+tuile_size)  # Position initiale x fixe

amplitude = 15  # Amplitude de l'oscillation en degrés
period = 2000  # Période de l'oscillation en millisecondes
# constants main
background_main = pygame.image.load("try/jeu.jpg")
background_main = pygame.transform.scale(background_main, (screen_width, screen_height))
#
clock = pygame.time.Clock()
# gestion tuiles
espacement_x = 15  # Espacement horizontal entre les tuiles
espacement_y = 15  # Espacement vertical entre les tuiles (ajouté)

num_files = 7
total_width = 4 * tuile_size
total_height = num_files * tuile_size
vertical_padding = screen_height - (screen_height/16)*13.5
player_start_x = screen_width/30
computer_start_x = screen_width - total_width - (screen_width/30) - espacement_x*2.5

# constants show_pause_menu
debut_music = 1

effect_path = r"try\effect\tuileeffect.mp3"

music_dir = r"try\music"
music_list = [os.path.join(music_dir, file) for file in os.listdir(music_dir) if file.endswith('.mp3')]
volume_level = 0.5

pause_surface = pygame.Surface(screen.get_size())
pause_surface.set_alpha(192)  # Semi-transparency
pause_surface.fill((0, 0, 0))  # Black color with semi-transparency

title_text = 'PAUSE'
title_position = (screen.get_width() / 2, screen.get_height() / 4)

middle_x = screen.get_width() / 2 - button_width / 2
continue_button_rect = pygame.Rect(middle_x, screen.get_height() / 2 - 75, button_width, button_height)
playlist_button_rect = pygame.Rect(middle_x, screen.get_height() / 2, button_width, button_height)
options_button_rect = pygame.Rect(middle_x, screen.get_height() / 2 + 75, button_width, button_height)
quit_button_rect = pygame.Rect(middle_x, screen.get_height() / 2 + 150, button_width, button_height)

clock = pygame.time.Clock()

# constants end_game_menu
background_end_game_menu = pygame.image.load(r"try\menu.jpg")
background_end_game_menu = pygame.transform.scale(background_end_game_menu, (screen_width, screen_height))


# Replay button
replay_rect = pygame.Rect(screen_width//2 - 150, screen_height//2 - 30, 300, 60)
# Quit button
quit_rect_end_game_menu = pygame.Rect(screen_width//2 - 150, screen_height//2 + 50, 300, 60)

