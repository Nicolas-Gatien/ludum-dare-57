import pygame
import random
from typing import List, Tuple

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.Clock = pygame.time.Clock()
running: bool = True
delta_time: float = 0

ADJUSTMENT_SPEED = 100
polygon_coordinates: List[Tuple[int, int]] = [
    (0, 0), 
    (screen.width / 2 - 150, 0),
    (screen.width / 2 - 200, screen.height / 2),
    (screen.width / 2, screen.height),
    (0, screen.height), 
]

def adjust_polygon(points: List[Tuple[int, int]], delta: float):
    new_points: List[Tuple[int, int]] = []
    for point in points:
        new_point = ([coord + ( delta * random.uniform(-1, 1) * ADJUSTMENT_SPEED ) for coord in point])
        new_points.append(new_point)

    return new_points

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    polygon_coordinates = adjust_polygon(polygon_coordinates, delta_time)
    pygame.draw.polygon(screen, "white", polygon_coordinates)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()