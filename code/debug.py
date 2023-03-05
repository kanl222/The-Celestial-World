import pygame
pygame.init()
font = pygame.font.Font(None,30)


pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y=10, x=10):
    display_surface = pygame.display.get_surface()
    debuf_surf = font.render(str(info), True, 'Black')
    debuf_rect = debuf_surf.get_rect(topleft=(x, y))
    display_surface.blit(debuf_surf, debuf_rect)

def debug_mode(body_game):
    try:
        debug(f'FPS: {int(body_game.clock.get_fps())}', 200, 10)
        debug(body_game.level.player.stats['magic'], 300, 10)
    except Exception as e:
        print(f"Error in debug_mode: {e}")