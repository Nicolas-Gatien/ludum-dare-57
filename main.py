import pygame
import random
import math
from typing import List, Tuple

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.Clock = pygame.time.Clock()
running: bool = True
delta_time: float = 0

SCROLL_SPEED = 100

def initialize_wall(wall: List[Tuple[float, float]], count: int):
    for _ in range(count):
        base = wall[len(wall) - 1]
        coordinate = (base[0] + (random.uniform(-1, 1) * 20), base[1] + 20)
        wall.append(coordinate)
    
    return wall
        
left_wall: List[Tuple[float, float]] = [(0, 0), (screen.width / 2 - 200, 0)]
left_wall = initialize_wall(left_wall, 50)

right_wall: List[Tuple[float, float]] = [(screen.width, 0), (screen.width / 2 + 200, 0)]
right_wall = initialize_wall(right_wall, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    left_wall = [(point[0], point[1] - SCROLL_SPEED * delta_time) for point in left_wall]
    right_wall = [(point[0], point[1] - SCROLL_SPEED * delta_time) for point in right_wall]

    render_left_wall = [point for point in left_wall]
    render_left_wall.append((0, screen.height))

    render_right_wall = [point for point in right_wall]
    render_right_wall.append((screen.width, screen.height))


    screen.fill("black")

    pygame.draw.polygon(screen, "white", render_left_wall)
    pygame.draw.polygon(screen, "white", render_right_wall)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()