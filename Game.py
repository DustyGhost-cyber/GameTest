import sys

import pygame
import pygame.font
import random

def click_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    #circle state
    circle_x = random.randint(0, screen.get_width())
    circle_y = random.randint(0, screen.get_height())
    color_circle = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    radius = 50
    # ── Existing ring variables ──
    ring_radius = radius + 150
    ring_active = True
    ring_speed = 200
    ring_hit_threshold = 15
    # ── Fade system ──
    fade_state = None  # None | "out" | "in"
    fade_alpha = 255
    fade_speed = 500
    # Frozen old circle state (for fade-out drawing)
    old_circle_x = 0
    old_circle_y = 0
    old_radius = 0
    old_ring_radius = 0
    old_color = (255, 255, 255)
    click_sound = pygame.mixer.Sound("hitmarker.mp3")
    point = 0


    def draw_word(text, size=16, color=(0, 0, 0)):
        font = pygame.font.SysFont("Consolas", size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(midtop=(screen.get_width() // 2, 10))
        screen.blit(text_surf, text_rect)

    while running:
        dt = clock.tick(60) / 1000


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and fade_state is None:
                if ring_active and abs(ring_radius - radius) <= ring_hit_threshold:
                    point += 10
                    # Freeze current state for fade-out
                    old_circle_x, old_circle_y = circle_x, circle_y
                    old_radius = radius
                    old_ring_radius = ring_radius
                    old_color = color_circle
                    # Enter fade-out phase
                    fade_state = "out"
                    fade_alpha = 255
                    click_sound.play()

        if fade_state == "out":
            fade_alpha -= fade_speed * dt
            if fade_alpha <= 0:
                # Fade-out done — generate new circle
                circle_x = random.randint(0, screen.get_width())
                circle_y = random.randint(0, screen.get_height())
                color_circle = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                radius = random.randint(3, 50)
                ring_radius = radius + 150
                ring_active = True
                # Switch to fade-in
                fade_state = "in"
                fade_alpha = 0
        elif fade_state == "in":
            fade_alpha += fade_speed * dt
            if fade_alpha >= 255:
                fade_alpha = 255
                fade_state = None  # back to normal play

        if fade_state is None and ring_active:
            ring_radius -= ring_speed * dt
            if ring_radius <= 0:
                ring_radius = radius + 150
                point = max(0, point - 1)

        screen.fill('black')

        draw_word(f'POINTS: {point}', size=16, color='white')
        if fade_state is None:
            pygame.draw.circle(screen, color_circle, (circle_x, circle_y), radius)
            if ring_active:
                pygame.draw.circle(screen, 'white', (circle_x, circle_y), ring_radius, width=3)
        else:
            surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            alpha = int(fade_alpha)
            if fade_state == "out":
                # Old circle + ring fading out
                pygame.draw.circle(surf, (*old_color, alpha),
                                    (old_circle_x, old_circle_y), old_radius)
                pygame.draw.circle(surf, (255, 255, 255, alpha),
                                        (old_circle_x, old_circle_y), old_ring_radius, width=3)
            elif fade_state == "in":
                # New circle + ring fading in
                pygame.draw.circle(surf, (*color_circle, alpha),
                                    (circle_x, circle_y), radius)
                pygame.draw.circle(surf, (255, 255, 255, alpha),
                                    (circle_x, circle_y), ring_radius, width=3)
            screen.blit(surf, (0, 0))

        pygame.display.flip()

    pygame.quit()
    sys.exit()