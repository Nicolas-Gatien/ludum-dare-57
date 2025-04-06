import pygame
import random
import math
from typing import List, Tuple

pygame.init()
pygame.display.set_caption("Caver")
pygame.font.init()

class GameState():
    def __init__(self, screen: pygame.Surface) -> None:
        self.player_position = pygame.Vector2(screen.width / 2, 100)
        self.player_speed = 0
        self.player_acceleration = 1000
        self.player_current_gravity = 0
        self.player_gravity_scale = 1000
        self.dead = False

        self.walls = [[(0, 0), (screen.width / 2 - 200, 0)], [(screen.width, 0), (screen.width / 2 + 200, 0)]]
        INITIAL_WALL_LENGTH = 50

        for wall in self.walls:
            for _ in range(INITIAL_WALL_LENGTH):
                base = wall[len(wall) - 1]
                coordinate = (base[0] + (random.uniform(-1, 1) * 20), base[1] + 20)
                wall.append(coordinate)

        self.score = 0
        self.SCROLL_SPEED = 300

    @property
    def left_wall(self):
        return self.walls[0]
    
    @left_wall.setter
    def left_wall(self, value):
        self.walls[0] = value
    
    @property
    def right_wall(self):
        return self.walls[1]
    
    @right_wall.setter
    def right_wall(self, value):
        self.walls[1] = value

# GAME STATE:
# Player Position
# Score
# Wall Positions
# Dead

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.Clock = pygame.time.Clock()
running: bool = True
delta_time: float = 0

def distance(point_a: pygame.Vector2, point_b: pygame.Vector2):
    return math.sqrt(((point_b.x - point_a.x) ** 2) + ((point_b.y - point_a.y) ** 2))

def extend_wall(wall: List[Tuple[float, float]]):
    base = wall[len(wall) - 1]
    coordinate = (base[0] + (random.uniform(-1, 1) * 20), base[1] + 20)
    return coordinate

game = GameState(screen=screen)

def die():
    global game
    
    if game.dead:
        return
    game.player_current_gravity = game.SCROLL_SPEED
    game.SCROLL_SPEED = 0
    game.player_speed = -(game.player_speed * 0.75)
    game.player_acceleration = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game.dead:
        game.player_position.y += game.player_current_gravity * delta_time
        game.player_current_gravity += game.player_gravity_scale * delta_time

    for wall in game.walls:
        for point in wall:
            if distance(pygame.Vector2(point[0], point[1]), game.player_position) <= 20:
                die()
                game.dead = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        game.player_speed -= game.player_acceleration * delta_time
    if keys[pygame.K_d]:
        game.player_speed += game.player_acceleration * delta_time
    if keys[pygame.K_r] and game.dead:
        game = GameState(screen)


    game.player_position.x += game.player_speed * delta_time

    for i, wall in enumerate(game.walls):
        game.walls[i] = [(point[0], point[1] - game.SCROLL_SPEED * delta_time) for point in wall]

        if wall[2][1] < 0:
            game.walls[i].append(extend_wall(wall))
            game.walls[i].pop(1)

    render_left_wall = [point for point in game.left_wall]
    render_left_wall.append((0, screen.height))

    render_right_wall = [point for point in game.right_wall]
    render_right_wall.append((screen.width, screen.height))

    if not(game.dead):
        game.score += 20 * delta_time

    screen.fill("black")

    pygame.draw.polygon(screen, "white", render_left_wall)
    pygame.draw.polygon(screen, "white", render_right_wall)
    pygame.draw.circle(screen, "purple", game.player_position, 20)

    text_surface = my_font.render(str(round(game.score)), False, "white")
    screen.blit(text_surface, ((screen.width / 2) - text_surface.width / 2,0))

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()