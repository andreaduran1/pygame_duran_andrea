import pygame
from modulos import *

def show_ranking(screen,font):
    clock = pygame.time.Clock()
    running = True

    # Leer los scores desde un archivo
    try:
        with open('scores.csv', "r", encoding="utf-8") as archivo:
            encabezado = archivo.readline().strip("\n").split(",")

            lineas = archivo.readlines()

            scores = []

            for linea in lineas:
                score = {}

                linea = linea.strip("\n").split(",")

                nombre, puntaje = linea
                score["nombre"] = nombre
                score["puntaje"] = puntaje
                scores.append(score)

    except FileNotFoundError:
        scores = []


    while running:
        pygame.mixer.music.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BLACK)

        y_offset = 100
        for score in scores:
            mostrar_texto(screen, (MID_WIDTH_SCREEN, y_offset), f'{score["nombre"]}: {score["puntaje"]}', font)
            y_offset += 40

        pygame.display.flip()
        clock.tick(FPS)
