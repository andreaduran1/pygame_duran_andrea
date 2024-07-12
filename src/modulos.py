import pygame
import random
from settings import *


def create_nave(
    imagen: pygame.Surface = None,
    left: int = MID_WIDTH_SCREEN,
    top: int = MID_HEIGHT_SCREEN,
    width: int = player_width,
    height: int = player_hight,
    color: tuple = WHITE,
) -> dict:
    """
    Crea un objeto de tipo nave.

    Args:
        imagen (pygame.Surface): Imagen de la nave. Por defecto es None.
        left (int): Posición inicial en el eje x. Por defecto es MID_WIDTH_SCREEN.
        top (int): Posición inicial en el eje y. Por defecto es MID_HEIGHT_SCREEN.
        width (int): Ancho de la nave. Por defecto es player_width.
        height (int): Altura de la nave. Por defecto es player_hight.
        color (tuple): Color de la nave. Por defecto es WHITE.

    Returns:
        dict: Diccionario con las propiedades de la nave.
    """

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


def create_laser(
    pos:tuple,
    direction:tuple,
    width:int=laser_width,
    height:int=laser_height,
    speed:int=laser_speed,
    color:tuple=BLUE,
)->dict:
    """
    Crea un objeto de tipo láser.

    Args:
        pos (tuple): Posición inicial del láser (x, y).
        direction (tuple): Dirección del láser (dx, dy).
        width (int): Ancho del láser. Por defecto es laser_width.
        height (int): Altura del láser. Por defecto es laser_height.
        speed (int): Velocidad del láser. Por defecto es laser_speed.
        color (tuple): Color del láser. Por defecto es BLUE.

    Returns:
        dict: Diccionario con las propiedades del láser.
    """
    return {
        "rect": pygame.Rect(pos[0], pos[1], width, height),
        "color": color,
        "direction": direction,
        "speed": speed,
    }


def create_enemy(
    imagen: pygame.Surface = None,
    top:int=0,
    width:int=enemy_width,
    height:int=enemy_hight,
    color:tuple=GREEN,
    speed:int=enemy_speed,
)->dict:
    """
    Crea un objeto de tipo enemigo.

    Args:
        imagen (pygame.Surface): Imagen del enemigo. Por defecto es None.
        top (int): Posición inicial en el eje y. Por defecto es 0.
        width (int): Ancho del enemigo. Por defecto es enemy_width.
        height (int): Altura del enemigo. Por defecto es enemy_hight.
        color (tuple): Color del enemigo. Por defecto es GREEN.
        speed (int): Velocidad del enemigo. Por defecto es enemy_speed.

    Returns:
        dict: Diccionario con las propiedades del enemigo.
    """
    direction = random.choice(
        [-1, 1]
    )  # Dirección inicial aleatoria (-1 para izquierda, 1 para derecha)
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
        "img": imagen,
    }


def create_enemy_laser(
    pos:tuple, width:int=laser_width, height:int=laser_height, color:tuple=RED, speed:int=laser_speed
)->dict:
    """
    Crea un objeto de tipo láser de enemigo.

    Args:
        pos (tuple): Posición inicial del láser (x, y).
        width (int): Ancho del láser. Por defecto es laser_width.
        height (int): Altura del láser. Por defecto es laser_height.
        color (tuple): Color del láser. Por defecto es RED.
        speed (int): Velocidad del láser. Por defecto es laser_speed.

    Returns:
        dict: Diccionario con las propiedades del láser.
    """
    return {
        "rect": pygame.Rect(pos[0], pos[1], width, height),
        "color": color,
        "speed": speed,
    }


def create_powerup(
    imagen: pygame.Surface = None,
    width: int=powerup_width,
    height:int=powerup_height,
    color:tuple=YELLOW,
)->dict:
    """
    Crea un objeto de tipo power-up.

    Args:
        imagen (pygame.Surface): Imagen del power-up. Por defecto es None.
        width (int): Ancho del power-up. Por defecto es powerup_width.
        height (int): Altura del power-up. Por defecto es powerup_height.
        color (tuple): Color del power-up. Por defecto es YELLOW.

    Returns:
        dict: Diccionario con las propiedades del power-up.
    """
    left = random.randint(0, screen_width - width)
    top = random.randint(0, screen_height - height)

    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))

    return {
        "rect": pygame.Rect(left, top, width, height),
        "color": color,
        "img": imagen,
    }


def move_nave(nave:dict):
    """
    Mueve la nave según la entrada del usuario.

    Args:
        nave (dict): Diccionario con las propiedades de la nave.
    """
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


def move_laser(laser:dict):
    """
    Mueve el láser en la dirección especificada.

    Args:
        laser (dict): Diccionario con las propiedades del láser.
    """
    laser["rect"].x += laser["direction"][0] * laser["speed"]
    laser["rect"].y += laser["direction"][1] * laser["speed"]


def move_enemy_laser(laser:dict):
    """
    Mueve el láser del enemigo hacia abajo.

    Args:
        laser (dict): Diccionario con las propiedades del láser.
    """
    laser["rect"].y += laser["speed"]


def calculate_direction(start_pos:tuple, end_pos:tuple):
    """
    Calcula la dirección normalizada entre dos puntos.

    Args:
        start_pos (tuple): Posición inicial (x, y).
        end_pos (tuple): Posición final (x, y).

    Returns:
        tuple: Dirección normalizada (dx, dy).
    """
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = (dx**2 + dy**2) ** 0.5
    if distance == 0:
        return (0, 0)
    return (dx / distance, dy / distance)


def move_enemies(enemies:list):
    """
    Mueve los enemigos y cambia su dirección al alcanzar los bordes.

    Args:
        enemies (list): Lista de diccionarios con las propiedades de los enemigos.
    """
    for enemy in enemies:
        if enemy["rect"].y < enemy["target_y"]:
            enemy["rect"].y += enemy["speed"]
        else:
            enemy["rect"].y = enemy["target_y"]
            enemy["rect"].x += enemy["direction"] * enemy["speed"]

        # Cambiar de dirección al alcanzar los bordes
        if enemy["rect"].left <= 0 or enemy["rect"].right >= screen_width:
            enemy["direction"] *= -1


def detectar_colision(rect_1:pygame.Rect, rect_2:pygame.Rect) -> bool:
    """
    Detecta si dos rectángulos colisionan.

    Args:
        rect_1 (pygame.Rect): Primer rectángulo.
        rect_2 (pygame.Rect): Segundo rectángulo.

    Returns:
        bool: True si hay colisión, False si no.
    """
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


def punto_en_rectangulo(punto:tuple, rect:pygame.Rect) -> bool:
    """
    Verifica si un punto está dentro de un rectángulo.

    Args:
        punto (tuple): Coordenadas del punto (x, y).
        rect (pygame.Rect): Rectángulo.

    Returns:
        bool: True si el punto está dentro del rectángulo, False si no.
    """
    x, y = punto

    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def distancia_entre_puntos(punto_1: tuple[int, int], punto_2: tuple[int, int]) -> float:
    """
    Calcula la distancia entre dos puntos.

    Args:
        punto_1 (tuple): Primer punto (x, y).
        punto_2 (tuple): Segundo punto (x, y).

    Returns:
        float: Distancia entre los puntos.
    """
    return ((punto_1[0] - punto_2[0]) ** 2 + (punto_1[1] - punto_2[1]) ** 2) ** 0.5


def calcular_radio(rect:pygame.Rect)->int:
    """
    Calcula el radio de un rectángulo, asumido como círculo.

    Args:
        rect (pygame.Rect): Rectángulo.

    Returns:
        int: Radio del círculo.
    """
    return rect.width // 2


def detectar_colision_circulos(rect_1:pygame.Rect, rect_2:pygame.Rect) -> bool:
    """
    Detecta si dos círculos colisionan, usando rectángulos como límites.

    Args:
        rect_1 (pygame.Rect): Primer rectángulo.
        rect_2 (pygame.Rect): Segundo rectángulo.

    Returns:
        bool: True si hay colisión, False si no.
    """
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2


def terminar():
    """
    Finaliza el juego y cierra Pygame.
    """
    pygame.quit()
    exit()


def wait_user(tecla:int):
    """
    Espera a que el usuario presione una tecla específica para continuar.

    Args:
        tecla (int): Código de la tecla a esperar.
    """
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
    """
    Muestra texto en la pantalla en una coordenada específica.

    Args:
        superficie (pygame.Surface): Superficie donde se dibujará el texto.
        coordenada (tuple): Coordenada del centro del texto (x, y).
        texto (str): Texto a mostrar.
        fuente (pygame.font.Font): Fuente del texto.
        color (tuple): Color del texto. Por defecto es WHITE.
        background_color (tuple): Color de fondo del texto. Por defecto es None.
    """
    sup_text = fuente.render(texto, True, color, background_color)
    rect_texto = sup_text.get_rect(center=coordenada)

    superficie.blit(sup_text, rect_texto)
    pygame.display.flip()
