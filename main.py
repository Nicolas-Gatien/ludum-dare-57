import pygame
import random
import math
from typing import List, Tuple

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.Clock = pygame.time.Clock()
running: bool = True
delta_time: float = 0

SCROLL_SPEED = 300

def distance(point_a: pygame.Vector2, point_b: pygame.Vector2):
    return math.sqrt(((point_b.x - point_a.x) ** 2) + ((point_b.y - point_a.y) ** 2))

def initialize_wall(wall: List[Tuple[float, float]], count: int):
    for _ in range(count):
        base = wall[len(wall) - 1]
        coordinate = (base[0] + (random.uniform(-1, 1) * 20), base[1] + 20)
        wall.append(coordinate)
    
    return wall

def extend_wall(wall: List[Tuple[float, float]]):
    base = wall[len(wall) - 1]
    coordinate = (base[0] + (random.uniform(-1, 1) * 20), base[1] + 20)
    return coordinate
        
left_wall: List[Tuple[float, float]] = [(0, 0), (screen.width / 2 - 200, 0)]
left_wall = initialize_wall(left_wall, 50)
right_wall: List[Tuple[float, float]] = [(screen.width, 0), (screen.width / 2 + 200, 0)]
right_wall = initialize_wall(right_wall, 50)

player_position = pygame.Vector2(screen.width / 2, 100)
player_speed = 0
player_acceleration = 1000

player_current_gravity = 0
player_gravity_scale = 1000

dead = False

def die():
    global SCROLL_SPEED
    global player_current_gravity
    global player_speed
    global player_acceleration
    
    if dead:
        return
    player_current_gravity = SCROLL_SPEED
    SCROLL_SPEED = 0
    player_speed = -(player_speed * 0.75)
    player_acceleration = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if dead:
        player_position.y += player_current_gravity * delta_time
        player_current_gravity += player_gravity_scale * delta_time

    for point in left_wall:
        if distance(pygame.Vector2(point[0], point[1]), player_position) <= 20:
            die()
            dead = True

    for point in right_wall:
        if distance(pygame.Vector2(point[0], point[1]), player_position) <= 20:
            die()
            dead = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_speed -= player_acceleration * delta_time
    if keys[pygame.K_d]:
        player_speed += player_acceleration * delta_time

    player_position.x += player_speed * delta_time

    left_wall = [(point[0], point[1] - SCROLL_SPEED * delta_time) for point in left_wall]
    right_wall = [(point[0], point[1] - SCROLL_SPEED * delta_time) for point in right_wall]

    render_left_wall = [point for point in left_wall]
    render_left_wall.append((0, screen.height))

    render_right_wall = [point for point in right_wall]
    render_right_wall.append((screen.width, screen.height))

    # Check 2 position so there's a buffer of 1 point before it's added to the bottom
    if (left_wall[2][1] < 0):
        left_wall.append(extend_wall(left_wall))
        # Pop 1 because 0 is the corner piece that fills the rest of the screen
        left_wall.pop(1)

    if (right_wall[2][1] < 0):
        right_wall.append(extend_wall(right_wall))
        right_wall.pop(1)

    screen.fill("black")

    pygame.draw.polygon(screen, "white", render_left_wall)
    pygame.draw.polygon(screen, "white", render_right_wall)
    pygame.draw.circle(screen, "purple", player_position, 20)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()