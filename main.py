from Game import *
import pygame
import sys

def draw_button(screen, rect, color, hover_color, is_hovered):
    pygame.draw.rect(screen, color, rect)
    if is_hovered:
        pygame.draw.rect(screen, hover_color, rect)

def menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game Menu")
    title_font = pygame.font.SysFont("Consolas", 48)
    btn_font = pygame.font.SysFont("Consolas", 32)
    btn_width, btn_height = 300, 60
    center_x = 400
    start_y = 250
    gap = 80
    buttons = []
    for i, text in enumerate(["Click Game", "Quit"]):
        btn_rect = pygame.Rect(
            center_x - btn_width // 2,
            start_y + i * gap,
            btn_width,
            btn_height,
        )
        buttons.append((text, btn_rect))
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in buttons:
                    if rect.collidepoint(event.pos):
                        if text == "Click Game":
                            pygame.quit()
                            click_game()
                            pygame.init()
                            screen = pygame.display.set_mode((800, 600))
                        elif text == "Quit":
                            pygame.quit()
                            sys.exit()
        screen.fill('black')
        title_surf = title_font.render("GAME TEST", True, 'white')
        title_rect = title_surf.get_rect(midtop=(400, 80))
        screen.blit(title_surf, title_rect)
        for text, rect in buttons:
            hovered = rect.collidepoint(mouse_pos)
            color = 'grey' if hovered else 'darkgrey'
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, 'white', rect, width=2, border_radius=10)
            btn_surf = btn_font.render(text, True, 'white')
            btn_rect = btn_surf.get_rect(center=rect.center)
            screen.blit(btn_surf, btn_rect)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    menu()




