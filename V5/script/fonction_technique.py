import pygame
import random
from .constants import tuile_size

class Maillon:
    def __init__(self, val=None):
        self.val = val
        self.suiv = None
        self.pred = None

class FileC:
    def __init__(self):
        self.tete = None
        self.queue = None

    def file_vide(self):
        return self.tete is None and self.queue is None

    def enfiler(self, v):
        nouveau_maillon = Maillon(v)
        if self.file_vide():
            self.tete = self.queue = nouveau_maillon
        else:
            nouveau_maillon.suiv = self.queue
            self.queue.pred = nouveau_maillon
            self.queue = nouveau_maillon

    def defiler(self):
        if not self.file_vide():
            if self.tete == self.queue:
                valeur = self.tete.val
                self.tete = self.queue = None
            else:
                valeur = self.tete.val
                self.tete = self.tete.pred
                self.tete.suiv = None
            return valeur
        return None

class Tuile:
    def __init__(self, couleur):
        self.couleur = couleur
        self.etat = 0
        # Set the image path based on the couleur
        self.image = pygame.image.load(f"try/{couleur}.png")
        self.image = pygame.transform.scale(self.image, (tuile_size, tuile_size))  # Scale image to fit tile size

    def famille(self):
        if '1' <= self.couleur <= '7':
            return "chiffre"
        elif 'a' <= self.couleur <= 'g':
            return "lettre"
        else:
            return "joker"

def verifier_homogeneite_file(file):
    if not file.file_vide():
        # First, ensure every tile's state is 1.
        m = file.queue
        all_etat_one = True
        while m:
            if m.val.etat != 1:
                all_etat_one = False
                break
            m = m.suiv

        # If all tiles are in state 1, check for homogeneity in color and family.
        if all_etat_one:
            homogene = True
            m = file.queue
            couleur_reference = file.queue.val.couleur
            famille_reference = file.queue.val.famille()

            while m:
                if m.val.couleur != couleur_reference or m.val.famille() != famille_reference:
                    homogene = False
                    break
                m = m.suiv

            return homogene
        else:
            return False
    return False





def victoire_ordinateur(files):
    for file in files:
        if file.file_vide():
            return False
        couleur_reference = file.queue.val.couleur
        m = file.queue
        while m:
            if m.val.etat != 1 or m.val.couleur != couleur_reference:
                return False
            m = m.suiv
    return True

def choix_intelligent_file(plateau, tuile_a_inserer):
    # Stocke les files éligibles avec leur score
    scores_files = []
    for file in plateau:
        if file.file_vide():
            # Haute priorité aux files vides pour favoriser les opportunités de nouveaux départs
            scores_files.append((file, 1000))
        else:
            score = 0
            homogene = True
            couleur_reference = file.queue.val.couleur

            current = file.queue
            while current:
                if current.val.couleur != couleur_reference:
                    homogene = False
                    break
                current = current.pred

            if homogene:
                # Bonus pour homogénéité
                score += 50

            if tuile_a_inserer.couleur == couleur_reference:
                # Bonus si la tuile à insérer correspond à la couleur de la file
                score += 30

            scores_files.append((file, score))

    # Filtrer les files ayant le score le plus élevé
    #en gros une ligne complique qui recupere le deuxieme element dans la liste score_files aka le score(LOL) et le [1] a lexterieur permet de renvoyer uniquement ce dit score sinon cette fonction aurait pour effet de renvoyer la file et le score associer hors ici on en a pas besoin
    #lambda est utilise pour pecho le deuxieme element dans la file
    meilleur_score = max(scores_files, key=lambda x: x[1])[1]
    files_eligibles = [file for file, score in scores_files if score == meilleur_score]

    # Choisir aléatoirement parmi les files éligibles
    meilleure_file = random.choice(files_eligibles)
    return plateau.index(meilleure_file)

def load_sound_effect(effect_path, volume_level):
    """Load and play a single sound effect from the specified file path."""
    sound_effect = pygame.mixer.Sound(effect_path)  # Charger l'effet sonore
    sound_effect.set_volume(volume_level)  # Définir le niveau de volume
    sound_effect.play()  # Jouer l'effet sonore
def play_music(music_file,volume_level):
    volume_level = volume_level*0.8
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume_level)  # Set the volume for the music
    pygame.mixer.music.play(-1)  # Jouer indéfiniment


import numpy as np

def animate_pulse(file, screen, base_x, base_y, tile_size):
    """
    Animates a pulsing effect on all tiles in a given file.

    Args:
    - file (FileC): The file (queue) containing the tiles to animate.
    - screen (pygame.Surface): The Pygame display surface to draw on.
    - base_x (int): The x-coordinate where the first tile of the file is drawn.
    - base_y (int): The y-coordinate where the tiles of the file are drawn.
    - tile_size (int): The size of each tile (both width and height).
    """
    initial_size = int(tile_size)
    max_size = int(tile_size * 1.1)  # Maximum size during pulse
    step_size = 0.5  # How quickly the tile grows and shrinks

    scale_up = np.arange(initial_size, max_size, step_size)
    scale_down = np.arange(max_size, initial_size, -step_size)
    scale_range = np.concatenate([scale_up, scale_down])

    for scale in scale_range:
        scale = int(scale)  # Convert scale to integer for pygame.transform.scale
        m = file.queue
        current_x = base_x
        while m:
            tile_image = pygame.transform.scale(m.val.image, (scale, scale))  # Scale the tile's image
            offset_x = (scale - initial_size) // 2
            offset_y = (scale - initial_size) // 2
            centered_x = current_x - offset_x
            centered_y = base_y - offset_y
            screen.blit(tile_image, (centered_x, centered_y))
            current_x += initial_size + 10
            m = m.suiv
        pygame.display.flip()
        pygame.time.wait(10)

    m = file.queue
    current_x = base_x
    while m:
        screen.blit(m.val.image, (current_x, base_y))
        current_x += initial_size + 10
        m = m.suiv
    pygame.display.flip()

