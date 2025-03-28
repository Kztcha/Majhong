import pygame
import random
import math
import os
import sys

from script.fonction_visuel import *
from script.constants import *
from script.music_menu import *
from script.options_menu import *
from script.fonction_technique import *





def show_pause_menu():
    """
    Affiche le menu de pause avec les boutons 'Continue', 'Playlist', et 'Quit to Menu'.
    """

    paused = True
    while paused:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background_image, (0, 0))
        screen.blit(pause_surface, (0, 0))
        draw_text(screen, title_text, title_position, font, pygame.Color('white'))  # Draw the title using draw_text

        continue_button = create_button(screen, continue_button_rect, button_color, button_hover_color, 'Continue', text_color, font, mouse_pos)
        playlist_button = create_button(screen, playlist_button_rect, button_color, button_hover_color, 'Playlist', text_color, font, mouse_pos)
        options_button = create_button(screen, options_button_rect, button_color, button_hover_color, 'Options', text_color, font, mouse_pos)
        quit_button = create_button(screen, quit_button_rect, button_color, button_hover_color, 'Menu', text_color, font, mouse_pos)

        pygame.display.update()  # Use update instead of flip for partial redraw

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_button.collidepoint(mouse_pos):
                    paused = False
                elif playlist_button.collidepoint(mouse_pos):
                    music_menu(music_list)
                elif options_button.collidepoint(mouse_pos):
                    show_options_menu()
                elif quit_button.collidepoint(mouse_pos):
                    show_menu()

        clock.tick(30)  # Maintain 30 frames per second

    return True  # Continue the game after pause




def show_menu():
    menu_running = True
    global debut_music
    while menu_running:
        if debut_music == 1:
            play_music(music_list[0], volume_level)
            debut_music = 0

        mx, my = pygame.mouse.get_pos()
        screen.blit(background_show_menu, (0, 0))
        current_time = pygame.time.get_ticks()  # Temps actuel en millisecondes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint((mx, my)):
                        main()
                    elif option_button.collidepoint((mx, my)):
                        show_options_menu()  # Ouvre le menu des options
                    elif quit_button.collidepoint((mx, my)):
                        sys.exit()

        # Mise à jour et dessin des tuiles défilantes avec rotation

        for i, img in enumerate(tile_images):
            angle = amplitude * math.sin(2 * math.pi * (current_time % period) / period)  # Calcul de l'angle actuel
            rotated_image = pygame.transform.rotate(img, angle)  # Rotation de l'image
            img_rect = rotated_image.get_rect(center=(tile_pos_x + img.get_width() // 2,
                                                      (tile_pos_y[i] % (screen_height + img.get_height())) - img.get_height() // 2))
            tile_pos_y[i] +=1  # Vitesse de défilement des tuiles
            screen.blit(rotated_image, img_rect.topleft)  # Positionnement de l'image rotative

        # Mise à jour et dessin des tuiles défilantes avec rotation 2
        for i, img in enumerate(tile_images2):
            rotated_image2 = pygame.transform.rotate(img, angle)  # Rotation de l'image
            img_rect = rotated_image.get_rect(center=(tile_pos_x2 + img.get_width() // 2,
                                                      (tile_pos_y[i] % (screen_height + img.get_height())) - img.get_height() // 2))
            screen.blit(rotated_image2, img_rect.topleft)  # Positionnement de l'image rotative

        # Update button states
        start_button = create_button(screen, start_rect, button_color, button_hover_color, 'Commencer', text_color, font, (mx, my))

        option_button = create_button(screen, option_rect, button_color,button_hover_color, 'Option', text_color, font, (mx, my))

        quit_button = create_button(screen, quit_rect, button_color, button_hover_color, 'Quitter', text_color, font, (mx, my))

        pygame.display.flip()
        clock.tick(90)



def main():

    pygame.display.set_caption('Rummy Mahjong')
    pieces = ['a', 'b', 'c', 'd', 'e', 'f', 'g', '1', '2', '3', '4', '5', '6', '7'] * 4
    random.shuffle(pieces)
    #
    # if not show_menu(screen, font):
    #     return

    Joueur = [FileC() for _ in range(7)]
    Ordinateur = [FileC() for _ in range(7)]

    for i in range(7):
        for j in range(4):
            Joueur[i].enfiler(Tuile(pieces.pop()))
            Ordinateur[i].enfiler(Tuile(pieces.pop()))

    joker = Tuile('W')
    joker.etat = 1  # Joker is always face up
    running = True
    pause = False
    sortie = joker  # Start with the joker as the initial tile to be played
    player_turn = random.choice([True, False])
    while running:
        if victoire_ordinateur(Joueur):
            for index, file in enumerate(Joueur):
                # Calculate the y-coordinate for the current file based on its index
                start_x = player_start_x
                start_y = vertical_padding + index * (tuile_size + espacement_y)
                # Call animate_pulse on each file
                animate_pulse(file, screen, start_x, start_y, tuile_size)
            if not end_game_menu("Joueur"):
                player_turn = None
                return

        if victoire_ordinateur(Ordinateur):
            for index, file in enumerate(Ordinateur):
                start_x = computer_start_x
                # Calculate the y-coordinate for the current file based on its index
                start_y = vertical_padding + index * (tuile_size + espacement_y)
                # Call animate_pulse on each file
                animate_pulse(file, screen, start_x, start_y, tuile_size)
            if not end_game_menu("Ordinateur"):
                player_turn = None
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if player_turn and not pause:
                    for index, file in enumerate(Joueur):
                        if player_start_x <= mx <= player_start_x + 7 * tuile_size and vertical_padding + index * (tuile_size + espacement_y) <= my <= vertical_padding + (index + 1) * tuile_size + index * espacement_y:
                            if not verifier_homogeneite_file(Joueur[index]):  # Vérification avant d'enfiler
                                Joueur[index].enfiler(sortie)
                                load_sound_effect(effect_path,volume_level)
                                sortie = Joueur[index].defiler()
                                sortie.etat = 1
                            if verifier_homogeneite_file(Joueur[index]):
                                # Coordinates where the file starts on the screen
                                start_x = player_start_x
                                start_y = vertical_padding + index * (tuile_size + espacement_y)

                                # Call the animation function
                                animate_pulse(Joueur[index], screen, start_x, start_y, tuile_size)

                            if sortie.famille() == "chiffre":
                                player_turn = True
                            elif sortie.famille() == "lettre" or sortie.famille() == "joker":
                                player_turn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                    if pause:
                        if not show_pause_menu():
                            return  # sys.exit to menu
                        pause = False  # Unpause if continued

        if not pause:
            if not player_turn:
                comp_index = choix_intelligent_file(Ordinateur, sortie)
                # if not verifier_homogeneite_file(Ordinateur[comp_index]):  # Vérification avant d'enfiler
                Ordinateur[comp_index].enfiler(sortie)
                sortie = Ordinateur[comp_index].defiler()
                sortie.etat = 1



                if sortie.famille() == "lettre":
                    player_turn = False
                elif sortie.famille() == "chiffre" or sortie.famille() == "joker":
                    player_turn = True

            screen.blit(background_main, (0, 0))
            for i, file in enumerate(Joueur + Ordinateur):
                x = player_start_x if i < 7 else computer_start_x
                y = vertical_padding + (i % 7) * (tuile_size + espacement_y)  # Adjusted Y position
                m = file.queue
                compteur_tuile = 0
                while m:
                    if compteur_tuile > 0:
                        x += espacement_x + tuile_size  # Adjusted for horizontal spacing
                    else:
                        x += compteur_tuile * espacement_x  # No extra spacing for the first tile
                    draw_tile(x, y, m.val, "square", i < 7)
                    m = m.suiv
                    compteur_tuile += 1

            if sortie:
                center_x = screen_width / 2 - tuile_size / 2
                center_y = vertical_padding + 3.5 * (tuile_size + espacement_y*0.2)  # Centering the sortie tile
                draw_tile(center_x, center_y, sortie, "square", True,lavender)

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()




def end_game_menu(winner):
    menu_runningend = True

    # Text indicating who won
    winner_text = font.render(f'{winner} a gagné!', True,gold, None)
    winner_rect = winner_text.get_rect(center=(screen_width//2, screen_height//3))


    while menu_runningend:
        mx, my = pygame.mouse.get_pos()
        screen.blit(background_end_game_menu, (0, 0))
        screen.blit(winner_text, winner_rect)

        # Update button states
        replay_button = create_button(screen, replay_rect, button_color, button_hover_color, 'Rejouer', text_color, font, (mx, my))
        quit_button = create_button(screen, quit_rect_end_game_menu, button_color, button_hover_color, 'Quitter', text_color, font, (mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if replay_button.collidepoint((mx, my)):
                        main()  # Restart the game
                        return True
                    elif quit_button.collidepoint((mx, my)):
                        show_menu()

if __name__ == "__main__":
    show_menu()