import pygame
pygame.init()
font = pygame.font.Font(None,30)


def debug(info,y=10,x=10):
    display_surface = pygame.display.get_surface()
    debuf_surf = font.render(str(info),True,'Black')
    debuf_rect = debuf_surf.get_rect(topleft=(x,y))
    display_surface.blit(debuf_surf,debuf_rect)



def debug_mode(self):
    debug(int(self.clock.get_fps()), 200, 10)
    debug(len(self.level.visible_sprites), 220, 10)
    debug(len(self.level.obstacle_sprites), 240, 10)
    debug(self.level.visible_sprites.count_sprite_updates, 280, 10)
    debug(self.level.player.exp, 260, 10)