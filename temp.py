import pygame
from time import sleep
from math import dist, cos, sin, radians, degrees

pygame.init()

window = pygame.display.set_mode((500, 500))


def point_cast(center, angle, radius):
    return (
        round(cos(radians(angle)) * radius + center[0]),
        round(-sin(radians(angle)) * radius + center[1]),
    )


assert point_cast((0, 0), 0, 50) == (50, 0)
assert point_cast((0, 0), 90, 50) == (0, -50)
assert point_cast((0, 0), 180, 50) == (-50, 0)
assert point_cast((0, 0), 270, 50) == (0, 50)
assert point_cast((250, 250), 0, 50) == (300, 250)


x = 250
y = 250
mouse_hold = False
radius = 50
offset_x = 0
offset_y = 0

rectangle = pygame.Rect(400, 400, 50, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and dist((x, y), event.pos) <= radius:
            mouse_hold = True
            offset_x = x - event.pos[0]
            offset_y = y - event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_hold = False
        if event.type == pygame.MOUSEMOTION and mouse_hold:
            x = event.pos[0] + offset_x
            y = event.pos[1] + offset_y
        if event.type == pygame.MOUSEWHEEL:
            radius += event.y
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), rectangle)
    pygame.draw.circle(window, (255, 0, 0), (x, y), radius)
    for angle in range(0, 360, 15):
        point = point_cast((x, y), angle, 50)
        color = (0, 255, 255) if rectangle.collidepoint(point) else (0, 0, 0)
        pygame.draw.circle(window, color, point, 3)
    pygame.display.update()
    sleep(1/60)
    # y += 2
