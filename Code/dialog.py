import pygame


pygame.init()
screen = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)
player = pygame.Rect(50, 50, 30, 30)

font = pygame.font.SysFont('Times New Roman', 50)
texts = ['Hi', 'Hello', 'Who are ye?', 'Someone']
text_renders = [font.render(text, True, (0, 0, 255)) for text in texts]
index = -1
space_released = True

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= 3
    if keys[pygame.K_d]:
        player.x += 3
    if keys[pygame.K_s]:
        player.y += 3
    if keys[pygame.K_w]:
        player.y -= 3

    pygame.draw.rect(screen, (0, 255, 0), box, width=2)
    pygame.draw.rect(screen, (255, 0, 0), player)

    if player.colliderect(box):
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            index = (index + 1) if (index + 1) != len(text_renders) else 0
        elif not keys[pygame.K_SPACE]:
            space_released = True
    else:
        index = -1

    if index != -1:
        screen.blit(text_renders[index], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()