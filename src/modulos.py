import pygame
import random
from settings import *


def create_nave(imagen:pygame.Surface = None, left=MID_WIDTH_SCREEN, top=MID_HEIGHT_SCREEN, width= player_width, height=player_hight, color=WHITE):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {
        "rect": pygame.Rect(left, top, width, height),
        "color": color,
        "lives": 3,
        "shield": False,
        "shield_powerups": 0,
        "shield_active": False,  
        "shield_timer": 0,
        "img": imagen,
    }

def create_laser(pos, direction, width=laser_width, height=laser_height, speed=laser_speed, color=BLUE):

    return {
        "rect": pygame.Rect(pos[0], pos[1], width, height),
        "color": color,
        "direction": direction,
        "speed": speed,
    }

def create_enemy(imagen:pygame.Surface = None, top=0, width=enemy_width, height=enemy_hight, color=GREEN, speed=enemy_speed):
    direction = random.choice([-1, 1])  # Dirección inicial aleatoria (-1 para izquierda, 1 para derecha)
    left = random.randint(0, screen_width - width)
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {
        "rect": pygame.Rect(left, top, width, height),
        "color": color,
        "speed": speed,
        "last_shot_time": 0,  # Tiempo del último disparo
        "target_y": random.randint(50, 150),  # Altura objetivo aleatoria
        "direction": direction,
        "hit": False,  # Estado de golpeado
        "hit_time": 0,  # Tiempo en que fue golpeado
        "img": imagen
    }

def create_enemy_laser(pos, width=laser_width, height=laser_height, color=RED, speed=laser_speed):
    return {
        "rect": pygame.Rect(pos[0], pos[1], width, height),
        "color": color,
        "speed": speed,
    }

def create_powerup(imagen:pygame.Surface = None, width=powerup_width, height=powerup_height, color=YELLOW):
    left = random.randint(0, screen_width - width)
    top = random.randint(0, screen_height - height)
    
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
        
    return {
        "rect": pygame.Rect(left, top, width, height),
        "color": color,
        "img":imagen
    }

def move_nave(nave):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        nave["rect"].x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        nave["rect"].x += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        nave["rect"].y -= 5 
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        nave["rect"].y += 5

    # Evitar que la nave salga de la pantalla
    if nave["rect"].top < 0:
        nave["rect"].top = 0
    if nave["rect"].bottom > screen_height:
        nave["rect"].bottom = screen_height

    if nave["rect"].left < 0:
        nave["rect"].left = 0
    if nave["rect"].right > screen_width:
        nave["rect"].right = screen_width

def move_laser(laser):
    laser["rect"].x += laser["direction"][0] * laser["speed"]
    laser["rect"].y += laser["direction"][1] * laser["speed"]

def move_enemy_laser(laser):
    laser["rect"].y += laser["speed"]

def calculate_direction(start_pos, end_pos):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance == 0:
        return (0, 0)
    return (dx / distance, dy / distance)

def move_enemies(enemies):
    for enemy in enemies:
        if enemy["rect"].y < enemy["target_y"]:
            enemy["rect"].y += enemy["speed"]
        else:
            enemy["rect"].y = enemy["target_y"]
            enemy["rect"].x += enemy["direction"] * enemy["speed"]

        # Cambiar de dirección al alcanzar los bordes
        if enemy["rect"].left <= 0 or enemy["rect"].right >= screen_width:
            enemy["direction"] *= -1


def detectar_colision(rect_1, rect_2) -> bool:

    return (
        punto_en_rectangulo(rect_1.topleft, rect_2)
        or punto_en_rectangulo(rect_1.topright, rect_2)
        or punto_en_rectangulo(rect_1.bottomleft, rect_2)
        or punto_en_rectangulo(rect_1.bottomright, rect_2)
        or punto_en_rectangulo(rect_2.topleft, rect_1)
        or punto_en_rectangulo(rect_2.topright, rect_1)
        or punto_en_rectangulo(rect_2.bottomleft, rect_1)
        or punto_en_rectangulo(rect_2.bottomright, rect_1)
    )


def punto_en_rectangulo(punto, rect) -> bool:
    x, y = punto

    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def distancia_entre_puntos(punto_1: tuple[int, int], punto_2: tuple[int, int]) -> float:
    return ((punto_1[0] - punto_2[0]) ** 2 + (punto_1[1] - punto_2[1]) ** 2) ** 0.5

def calcular_radio(rect):
    return rect.width // 2

def detectar_colision_circulos(rect_1, rect_2) -> bool:
    r1 =calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2


def terminar():
    pygame.quit()
    exit()


def wait_user(tecla):
    flag_start = True

    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            if event.type == pygame.KEYDOWN:
                if event.key == tecla:
                    flag_start = False


def mostrar_texto(
    superficie: pygame.Surface,
    coordenada: tuple[int, int],
    texto: str,
    fuente: pygame.font.Font,
    color: tuple[int, int, int] = WHITE,
    background_color: tuple[int, int, int] = None,
):
    sup_text = fuente.render(texto, True, color, background_color)
    rect_texto = sup_text.get_rect(center=coordenada)

    superficie.blit(sup_text, rect_texto)
    pygame.display.flip()