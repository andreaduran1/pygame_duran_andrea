import pygame
from modulos import *
from settings import *


def game_loop(
    screen,
    font,
    font_title,
    background,
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
):
    running = True
    pygame.mouse.set_visible(False)
    playing_music = True

    # Crear la nave
    nave = create_nave(nave)

    # Lista para almacenar los láseres, enemigos y power-ups
    lasers = []
    enemies = []
    enemy_lasers = []
    powerups = []

    # Reloj para controlar los FPS
    clock = pygame.time.Clock()

    # Temporizador para crear enemigos y power-ups
    ENEMY_EVENT = pygame.USEREVENT + 1
    POWERUP_EVENT = pygame.USEREVENT + 2
    ENEMY_SHOOT_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(ENEMY_EVENT, 1000)  # Crear un enemigo cada segundo
    pygame.time.set_timer(POWERUP_EVENT, 20000)  # Crear un power-up cada 20 segundos
    pygame.time.set_timer(ENEMY_SHOOT_EVENT, 2000)  # Enemigos disparan cada 2 segundos

    # Inicializar la puntuación
    score = 0

    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    direction = calculate_direction(
                        nave["rect"].midtop, (mouse_x, mouse_y)
                    )
                    laser = create_laser(nave["rect"].midtop, direction)
                    lasers.append(laser)
                    laser_sound.play()
            if event.type == ENEMY_EVENT:
                enemy = create_enemy(nave_enemiga)
                enemies.append(enemy)
            if event.type == POWERUP_EVENT:
                powerup = create_powerup(powerup_shield)
                powerups.append(powerup)
            if event.type == ENEMY_SHOOT_EVENT:
                for enemy in enemies:
                    if enemy["rect"].y >= enemy["target_y"]:
                        enemy_laser = create_enemy_laser(
                            enemy["rect"].midbottom
                        )
                        enemy_lasers.append(enemy_laser)
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE
                    and nave["shield_powerups"] > 0
                    and not nave["shield_active"]
                ):
                    nave["shield_active"] = True
                    nave["shield_timer"] = (
                        current_time + 10000
                    )  # Escudo activo por 10 segundos
                    nave["shield_powerups"] -= 1
                    force_field_sound.play()

                if event.key == pygame.K_p:
                    pygame.mixer.music.pause()
                    mostrar_texto(screen, CENTER_SCREEN, "Pause", font, WHITE)
                    wait_user(pygame.K_p)
                    if playing_music:
                        pygame.mixer.music.unpause()

                if event.key == pygame.K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    playing_music = not playing_music

        # movimientos
        move_nave(nave)

        for laser in lasers:
            move_laser(laser)

        for enemy_laser in enemy_lasers:
            move_enemy_laser(enemy_laser)

        move_enemies(enemies)

        # deteccion de colisiones/acciones
        for enemy in enemies[:]:
            for laser in lasers[:]:
                if detectar_colision(enemy["rect"], laser["rect"]):
                    enemy["hit"] = True
                    enemy["hit_time"] = current_time
                    enemy["img"] = explosion
                    lasers.remove(laser)
                    score += 100

        for laser in enemy_lasers[:]:
            if nave["shield_active"]:
                shield_radius = nave["rect"].width
                shield_rect = pygame.Rect(0, 0, shield_radius * 2, shield_radius * 2)
                shield_rect.center = nave["rect"].center
                if detectar_colision_circulos(shield_rect, laser["rect"]):
                    enemy_lasers.remove(laser)
            else:
                if detectar_colision(nave["rect"], laser["rect"]):
                    nave["lives"] -= 1
                    impact_sound.play()
                    enemy_lasers.remove(laser)
                    if nave["lives"] <= 0:
                        running = False
                        pygame.mixer.music.pause()
                        game_over_sound.play()

        for enemy in enemies[:]:
            if nave["shield_active"]:
                shield_radius = nave["rect"].width
                shield_rect = pygame.Rect(0, 0, shield_radius * 2, shield_radius * 2)
                shield_rect.center = nave["rect"].center
                if detectar_colision_circulos(shield_rect, enemy["rect"]):
                    enemy["hit"] = True
                    enemy["hit_time"] = current_time
                    enemy["img"] = explosion
                    score += 100
            else:
                if detectar_colision(nave["rect"], enemy["rect"]):
                    nave["lives"] = 0
                    enemy["hit"] = True
                    enemy["hit_time"] = current_time
                    enemy["img"] = explosion
                    if nave["lives"] <= 0:
                        running = False
                        pygame.mixer.music.pause()
                        game_over_sound.play()

        for powerup in powerups[:]:
            if detectar_colision(nave["rect"], powerup["rect"]):
                nave["shield_powerups"] += 1
                powerups.remove(powerup)

        if nave["shield_active"] and current_time >= nave["shield_timer"]:
            nave["shield_active"] = False

        # dibujo pantalla
        screen.blit(background, ORIGIN)
        screen.blit(nave["img"], nave["rect"])

        if nave["shield_active"]:
            pygame.draw.circle(screen, BLUE, nave["rect"].center, nave["rect"].width, 4)

        for laser in lasers:
            pygame.draw.rect(screen, laser["color"], laser["rect"])

        for enemy in enemies:
            if enemy["hit"]:
                if current_time - enemy["hit_time"] < 100:  # Animación de 100 ms
                    screen.blit(enemy["img"], enemy["rect"])
                    explosion_sound.play()
                else:
                    enemies.remove(enemy)
            else:
                screen.blit(enemy["img"], enemy["rect"])

        for enemy_laser in enemy_lasers:
            pygame.draw.rect(screen, enemy_laser["color"], enemy_laser["rect"])

        for powerup in powerups:
            screen.blit(powerup["img"], powerup["rect"])

        if not playing_music:
            mostrar_texto(screen, POSICION_MUTE, "Mute", font, WHITE)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_rect = cursor.get_rect(center=(mouse_x, mouse_y))
        screen.blit(cursor, cursor_rect)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        powerup_text = font.render(f"Escudo: {nave["shield_powerups"]}", True, WHITE)
        screen.blit(powerup_text, POSICION_POWERUP)

        lives_text = font.render(f'Lives: {nave["lives"]}', True, WHITE)
        screen.blit(lives_text, (screen_width - 200, 10))

        pygame.display.flip()

    # Llamar a la pantalla de game over
    from game_over import game_over_screen

    game_over_screen(screen, score, font_title, font,high_score)
