import pygame
from modulos import *
from settings import *

def game_over_screen(screen, score, font_title, font,high_score):
    clock = pygame.time.Clock()
    running = True

    # Guardar el puntaje en el archivo
    name = input("Ingresa tus iniciales: ")

    with open('scores.csv', 'a') as archivo:
        archivo.write(f'{name},{score}\n')

    if score > high_score:
        high_score = score
        with open('high_score.csv', 'w') as archivo:
            archivo.write(f'{high_score}')


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
                from main import main_menu
                main_menu()

        screen.fill(BLACK)
        game_over_text = font_title.render('Game Over', True, RED)
        high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
        score_text = font.render(f'Score: {score}', True, WHITE)
        prompt_text = font.render('Press Enter', True, WHITE)

        screen.blit(game_over_text, (MID_WIDTH_SCREEN - game_over_text.get_width() // 2, 200))
        screen.blit(high_score_text, (MID_WIDTH_SCREEN - high_score_text.get_width() // 2, 350))
        screen.blit(score_text, (MID_WIDTH_SCREEN - score_text.get_width() // 2, 400))
        screen.blit(prompt_text, (MID_WIDTH_SCREEN - prompt_text.get_width() // 2, 500))

        pygame.display.flip()
        clock.tick(FPS)
