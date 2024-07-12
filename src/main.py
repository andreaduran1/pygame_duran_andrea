import pygame
from game import game_loop
from ranking import show_ranking
from settings import *
from modulos import terminar
import json

#cargo json con assets:
try:
    with open("./assets.json", "r") as archivo:
        assets = json.load(archivo)
except:
    print("No se encontró el archivo")


# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Space Defender")
pygame.display.set_icon(pygame.image.load(assets["images"]["icon"]))


# Fuente
font_title = pygame.font.Font(assets["fonts"]["font_title"], 74)
font_text = pygame.font.Font(assets["fonts"]["font_text"], 36)
font_game = pygame.font.Font(assets["fonts"]["font_game"], 28)

# Imagenes
background_menu = pygame.transform.scale(
    pygame.image.load(assets["images"]["background_menu"]), SIZE_SCREEN
)
background_game = pygame.transform.scale(
    pygame.image.load(assets["images"]["background_game"]), SIZE_SCREEN
)
cursor = pygame.transform.scale(
    pygame.image.load(assets["images"]["cursor"]), cursor_size
)
nave = pygame.image.load(assets["images"]["nave"])
nave_enemiga = pygame.image.load(assets["images"]["nave_enemiga"])
powerup_shield = pygame.image.load(assets["images"]["powerup_shield"])
explosion = pygame.transform.scale(
    pygame.image.load(assets["images"]["explosion"]), player_size
)

# Sonido
laser_sound = pygame.mixer.Sound(assets["sounds"]["laser_sound"])
game_over_sound = pygame.mixer.Sound(assets["sounds"]["game_over_sound"])
force_field_sound =pygame.mixer.Sound(assets["sounds"]["force_field_sound"])
force_field_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(assets["sounds"]["explosion_sound"])
explosion_sound.set_volume(0.2)
impact_sound =pygame.mixer.Sound(assets["sounds"]["impact_sound"])
impact_sound.set_volume(0.2)

# Musica
pygame.mixer.music.load(assets["music"]["musica_fondo"])
pygame.mixer.music.set_volume(0.02)

# cargo datos

try:
    with open('high_score.csv', "r", encoding="utf-8") as archivo:
        linea = archivo.readline()

        high_score = int(linea)

except FileNotFoundError:
    high_score = 0


def main_menu():
    while True:
        pygame.mixer.music.play()
        pygame.mouse.set_visible(True)
        screen.blit(background_menu, ORIGIN)

        title = font_title.render("Space Defender", True, WHITE)
        play_button = font_text.render("Play", True, WHITE)
        ranking_button = font_text.render("Ranking", True, WHITE)
        

        screen.blit(title, (MID_WIDTH_SCREEN - title.get_width() // 2, 100))
        screen.blit(play_button, (MID_WIDTH_SCREEN - play_button.get_width() // 2, 250))
        screen.blit(
            ranking_button, (MID_WIDTH_SCREEN - ranking_button.get_width() // 2, 350)
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 250 < event.pos[1] < 250 + play_button.get_height():
                    game_loop(
                        screen,
                        font_game,
                        font_title,
                        background_game,
                        cursor,
                        nave,
                        nave_enemiga,
                        powerup_shield,
                        explosion,
                        laser_sound,
                        force_field_sound,
                        explosion_sound,
                        game_over_sound,
                        impact_sound,
                        high_score
                    )
                elif 350 < event.pos[1] < 350 + ranking_button.get_height():
                    show_ranking(screen)
                    


if __name__ == "__main__":
    main_menu()
