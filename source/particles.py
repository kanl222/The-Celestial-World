import pygame as pg
from random import choice

pg.font.init()

class Particle:
    def __init__(self):
        # frames \u2014 \u0441\u043b\u043e\u0432\u0430\u0440\u044c \u0430\u043d\u0438\u043c\u0430\u0446\u0438\u0439 (\u043d\u0430\u043f\u0440., 'leaf'). \u041f\u043e\u0434\u043a\u043b\u0430\u0441\u0441\u044b \u0434\u043e\u043b\u0436\u043d\u044b \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u0442\u044c \u0435\u0433\u043e \u043f\u0440\u0438 \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e\u0441\u0442\u0438.
        self.frames: dict = {}

    def reflect_images(self, frames):
        return [pg.transform.flip(x, True, False) for x in frames]

    def create_grass_particles(self, pos, groups):
        leaf_frames = self.frames.get('leaf')
        if leaf_frames:
            ParticleEffect(pos, choice(leaf_frames), groups)

    def create_particles(self, frames, pos, groups):
        ParticleEffect(pos, frames, groups)

    def create_bullet_magic(self, direction, pos: tuple, frames: list, groups) -> None:
        """C\u043e\u0437\u0434\u0430\u0451\u0442 \u043f\u0443\u043b\u044e \u043c\u0430\u0433\u0438\u0438 \u0441 \u0437\u0430\u0434\u0430\u043d\u043d\u044b\u043c \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435\u043c."""
        Bullet(direction, pos, frames, groups)

    def create_number(self, pos, number, groups, color=None):
        MoveNumberRender(pos, number, groups, color)



class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'particle'
        self.queue = 2
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class MoveNumberRender(pg.sprite.Sprite):
    FONT_OBJECT = pg.font.SysFont(None, 30)
    SHADOW_OFFSET = (1, 1)

    def __init__(self, pos: tuple, number: str, groups: list, color=(255, 255, 255)):
        super().__init__(groups)
        self.queue = 4
        self.moving_y = 0
        self.animation_speed = 1.2
        self.image = pg.Surface((30*len(number), 30*len(number)), pg.SRCALPHA)
        text = self.FONT_OBJECT.render(number, True, color)
        shadow_text = self.FONT_OBJECT.render(number, True, (0, 0, 0))
        self.image.blit(shadow_text, self.SHADOW_OFFSET)
        self.image.blit(text, (0,0))
        self.rect = self.image.get_rect(midtop=(pos[0], pos[1] - 10))

    def animate(self):
        if self.moving_y < 16:
            self.rect.y -= self.animation_speed
            self.moving_y += self.animation_speed
        else:
            self.kill()

    def update(self):
        self.animate()




class Bullet(pg.sprite.Sprite):
    def __init__(self, direction, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'particle'
        self.speed = 10
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = direction
        self.frames = [self.direction_image(i) for i in animation_frames]
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)
        self.hit_time = pg.time.get_ticks()

    def collision(self):
        self.kill()

    def rot_center(self,image, angle):
        loc = image.get_rect().center  # rot_image is not defined
        rot_sprite = pg.transform.rotate(image, angle).convert_alpha()
        rot_sprite.get_rect().center = loc
        return rot_sprite

    def direction_image(self,img):
        if self.direction == (1, 0):
            return self.rot_center(img,180)
        elif self.direction == (-1, 0):
            return img
        elif self.direction == (0, -1):
            return self.rot_center(img,-90)
        else:
            return self.rot_center(img,90)

    def update(self) -> None:
        current_time = pg.time.get_ticks()
        if current_time - self.hit_time >= 2000:
            self.collision()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
