import pygame
pygame.init()
font = pygame.font.Font(None,30)


def debug(info,y=10,x=10):
    display_surface = pygame.display.get_surface()
    debuf_surf = font.render(str(info),True,'Black')
    debuf_rect = debuf_surf.get_rect(topleft=(x,y))
    display_surface.blit(debuf_surf,debuf_rect)