import pygame
from script.constants import *
from script.fonction_visuel import *
from script.fonction_technique import *
import sys


def music_menu(music_list):
    global volume_level
    running_music_menu = True
    selected_index = 0

    while running_music_menu:
        screen.blit(background_music_menu, (0, 0))
        total_items_height = min(visible_items_count, len(music_list)) * item_height
        start_y = (screen_height - total_items_height) // 2

        for i in range(len(music_list)):
            if i >= selected_index - visible_items_count // 2 and i <= selected_index + visible_items_count // 2:
                text_color = RED if i == selected_index else WHITE
                music_name = os.path.basename(music_list[i])
                text = font.render(music_name, True, text_color)
                text_rect = text.get_rect(center=(screen_width // 2, start_y + (i - (selected_index - visible_items_count // 2)) * item_height))
                screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_music_menu = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(music_list)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1 + len(music_list)) % len(music_list)
                elif event.key == pygame.K_RETURN:
                    play_music(music_list[selected_index], volume_level)
                    running_music_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    selected_index = (selected_index - 1 + len(music_list)) % len(music_list)
                elif event.button == 5:
                    selected_index = (selected_index + 1) % len(music_list)
                elif event.button == 1:
                    play_music(music_list[selected_index], volume_level)
                    running_music_menu = False
