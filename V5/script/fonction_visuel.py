import pygame
from .constants import *

def create_button(screen, rect, color, hover_color, text, text_color, font, mouse_pos):

    button_rect = pygame.Rect(rect)
    is_hovered = button_rect.collidepoint(mouse_pos)

    # Choix de la couleur et de l'effet d'enfoncement
    if is_hovered:
        current_color = hover_color
        offset = 2  # Décalage en pixels pour l'effet d'enfoncement
    else:
        current_color = color
        offset = 0

    # Dessin du bouton avec bordures arrondies
    button_rect_with_offset = pygame.Rect(rect[0] + offset, rect[1] + offset, rect[2] - 2*offset, rect[3] - 2*offset)
    pygame.draw.rect(screen, current_color, button_rect_with_offset, border_radius=10)

    # Préparation et dessin du texte avec l'effet d'enfoncement
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(button_rect.centerx + offset, button_rect.centery + offset))
    screen.blit(text_surface, text_rect)

    return button_rect

def draw_text(screen, text, position, font, color = WHITE, center=True):
    """
    Dessine du texte sur un écran Pygame donné, à la position spécifiée.
    """
    text_surface = font.render(text, True, pygame.Color(*color))
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = position
    else:
        text_rect.topleft = position
    screen.blit(text_surface, text_rect)








def draw_tile(x, y, tile, tile_type="square", highlight=False, highlight_color=BLACK):
    if tile.etat == 1:  # Only draw the image if the tile is face up
        screen.blit(tile.image, (x, y))
    else:
        # Draw a grey rectangle for face down tiles
        shape = pygame.Rect(x, y, tuile_size, tuile_size)
        temp_surface = pygame.Surface((shape.width, shape.height), pygame.SRCALPHA)  # Ensure it supports alpha
        temp_surface.fill(color_dark_wood)

        # Blit the temporary surface onto the screen at the position specified in shape
        screen.blit(temp_surface, shape.topleft)

    if highlight:
        pygame.draw.rect(screen, highlight_color, (x, y, tuile_size, tuile_size), 2)  # Draw highlight border with specified color
