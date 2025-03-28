import pygame
from script.constants import *
from script.fonction_visuel import *
import sys
import os

def aide():

    current_image_index = 0

    if not image_files:
        print("No images found in the specified directory.")
        return

    images_menu_running = True

    while images_menu_running:
        mx, my = pygame.mouse.get_pos()
        screen.blit(images[current_image_index], (0, 0))  # Display the current image

        next_button = create_button(screen, next_button_rect, button_color, button_hover_color, '>', text_color, fontbouton, (mx, my))
        prev_button = create_button(screen, prev_button_rect, button_color, button_hover_color, '<', text_color, fontbouton, (mx, my))
        backA_button = create_button(screen, backA_button_rect, button_color, button_hover_color, 'Retour', text_color, font, (mx, my))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if backA_button.collidepoint((mx, my)):
                    images_menu_running = False
                elif next_button.collidepoint((mx, my)):
                    current_image_index = (current_image_index + 1) % len(images)
                elif prev_button.collidepoint((mx, my)):
                    current_image_index = (current_image_index - 1) % len(images)

        clock.tick(30)

# Remember to define the necessary variables such as:
# - next_button_rect, prev_button_rect, and back_button_rect for positioning buttons
# - button_color, button_hover_color, text_color for styling buttons
# - fontbouton and font for text rendering
# - screen and clock should already be initialized in your main script
