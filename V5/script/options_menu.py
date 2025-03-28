import pygame
from script.constants import *
from script.fonction_visuel import *
import sys
from script.aide import *


def show_options_menu():
    global volume_level
    options_running = True

    while options_running:
        mx, my = pygame.mouse.get_pos()
        screen.blit(background_options, (0, 0))

        volume_text = f"Volume: {int(volume_level * 100)}%"
        draw_text(screen, volume_text, volume_text_pos, font, pygame.Color('white'))

        # Boutons pour incrémenter et décrémenter le volume
        incr_volume_button = create_button(screen, incr_volume_button_rect, button_color, button_hover_color, '+', text_color, fontbouton, (mx, my))
        decr_volume_button = create_button(screen, decr_volume_button_rect, button_color, button_hover_color, '-', text_color, fontbouton, (mx, my))

        aide_button = create_button(screen, aide_button_rect, button_color, button_hover_color, 'Aide', text_color, font, (mx, my))

        back_button = create_button(screen, back_button_rect, button_color, button_hover_color, 'Retour', text_color, font, (mx, my))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint((mx, my)):
                    options_running = False
                elif aide_button.collidepoint((mx, my)):
                    aide()
                elif incr_volume_button.collidepoint((mx, my)):
                    volume_level = min(1.0, volume_level + 0.1)
                    pygame.mixer.music.set_volume(volume_level)
                elif decr_volume_button.collidepoint((mx, my)):
                    volume_level = max(0.0, volume_level - 0.1)
                    pygame.mixer.music.set_volume(volume_level)

        clock.tick(30)
