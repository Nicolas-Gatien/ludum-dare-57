import pygame
import random
import math
from typing import List, Tuple

pygame.init()
pygame.display.set_caption("Caver")
pygame.font.init()
pygame.mixer.init()

LEFT = 0
RIGHT = 1

class Frog():
    def __init__(self, position: Tuple[float, float]) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(position[0], position[1])
        self.current_gravity = -350
        self.gravity_scale = 400
        self.movement_speed = 50
        self.jumped = False
        self.flipped = False
        self.jump_time = 0

class GameState():
    def __init__(self, screen: pygame.Surface) -> None:
        self.player_position = pygame.Vector2(screen.width / 2, 250)
        self.player_speed = 0
        self.player_acceleration = 1000
        self.player_current_gravity = 0
        self.player_gravity_scale = 1000
        self.dead = False

        self.frogs: List[Frog] = []

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
        return self.walls[LEFT]
    
    @left_wall.setter
    def left_wall(self, value):
        self.walls[LEFT] = value
    
    @property
    def right_wall(self):
        return self.walls[RIGHT]
    
    @right_wall.setter
    def right_wall(self, value):
        self.walls[RIGHT] = value

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.Clock = pygame.time.Clock()
running: bool = True
delta_time: float = 0

miner = pygame.image.load('miner.png').convert_alpha()
miner = pygame.transform.scale(miner, (48, 48))

frog_sprite = pygame.image.load('frog.png').convert_alpha()
frog_sprite = pygame.transform.scale(frog_sprite, (48, 48))

jump_sound = pygame.mixer.Sound('jump.ogg')
death_sound = pygame.mixer.Sound('die.ogg')

def distance(point_a: pygame.Vector2, point_b: pygame.Vector2):
    return math.sqrt(((point_b.x - point_a.x) ** 2) + ((point_b.y - point_a.y) ** 2))

def tuple_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]):
    return math.sqrt(((point_b[0] - point_a[0]) ** 2) + ((point_b[1] - point_a[1]) ** 2))


def extend_wall(wall: List[Tuple[float, float]]):
    offset = (math.sin(game.score / 10) * 25) + (math.sin(game.score / 2) * 10) + (math.sin(game.score / 8) * 0.75)
    base = wall[len(wall) - 1]
    coordinate = (base[0] + (random.uniform(-1, 1) * 20) + offset, base[1] + 20)
    return coordinate

def spawn_frog(wall: List[Tuple[float, float]], index: int, wall_number: int):
    base = wall[index]
    previous = wall[index - 1]

    if (wall_number == LEFT):
        if (previous[0] > base[0]):
            return None
    elif (wall_number == RIGHT):
        if (base[0] > previous[0]):
            return None
    
    if tuple_distance(base, previous) < 30:
        return None
    
    coordinates = ((previous[0] + base[0]) / 2, (previous[1] + base[1]) / 2)

    return Frog(coordinates)

game = GameState(screen=screen)

def die():
    global game
    
    if game.dead:
        return
    game.player_current_gravity = game.SCROLL_SPEED
    game.SCROLL_SPEED = 0
    game.player_speed = -(game.player_speed * 2)
    game.player_current_gravity = -100
    game.player_acceleration = 0
    death_sound.play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game.player_speed < 0:
        blitted_miner = pygame.transform.rotate(miner, -game.player_speed / 10)
        blitted_miner = pygame.transform.flip(blitted_miner, True, False)
    else:
        blitted_miner = pygame.transform.rotate(miner, game.player_speed / 10)

    # LEVEL GENERATION
    while distance(
        pygame.Vector2(game.left_wall[len(game.left_wall) - 1][0], game.left_wall[len(game.left_wall) - 1][1]), 
        pygame.Vector2(game.right_wall[len(game.right_wall) - 1][0], game.right_wall[len(game.right_wall) - 1][1])) < 200:
        game.left_wall[len(game.left_wall) - 1] = (game.left_wall[len(game.left_wall) - 1][0] - 1, game.left_wall[len(game.left_wall) - 1][1])
        game.right_wall[len(game.right_wall) - 1] = (game.right_wall[len(game.right_wall) - 1][0] + 1, game.right_wall[len(game.right_wall) - 1][1])

    while distance(
        pygame.Vector2(game.left_wall[len(game.left_wall) - 1][0], game.left_wall[len(game.left_wall) - 1][1]), 
        pygame.Vector2(game.right_wall[len(game.right_wall) - 1][0], game.right_wall[len(game.right_wall) - 1][1])) > 500:
        game.left_wall[len(game.left_wall) - 1] = (game.left_wall[len(game.left_wall) - 1][0] + 1, game.left_wall[len(game.left_wall) - 1][1])
        game.right_wall[len(game.right_wall) - 1] = (game.right_wall[len(game.right_wall) - 1][0] - 1, game.right_wall[len(game.right_wall) - 1][1])
    
    while game.left_wall[len(game.left_wall) - 1][0] < 200:
        game.left_wall[len(game.left_wall) - 1] = (game.left_wall[len(game.left_wall) - 1][0] + 23, game.left_wall[len(game.left_wall) - 1][1])
        game.right_wall[len(game.right_wall) - 1] = (game.right_wall[len(game.right_wall) - 1][0] + 23, game.right_wall[len(game.right_wall) - 1][1])

    while game.right_wall[len(game.right_wall) - 1][0] > screen.width - 200:
        game.left_wall[len(game.left_wall) - 1] = (game.left_wall[len(game.left_wall) - 1][0] - 23, game.left_wall[len(game.left_wall) - 1][1])
        game.right_wall[len(game.right_wall) - 1] = (game.right_wall[len(game.right_wall) - 1][0] - 23, game.right_wall[len(game.right_wall) - 1][1])

    if game.dead:
        game.player_position.y += game.player_current_gravity * delta_time
        game.player_current_gravity += game.player_gravity_scale * delta_time

    for wall in game.walls:
        for point in wall:
            if distance(pygame.Vector2(point[0], point[1]), game.player_position) <= 20:
                die()
                game.dead = True
            for frog in game.frogs:
                if distance(frog.position, pygame.Vector2(point[0], point[1])) <= 20:
                    frog.jumped = False
                    frog.current_gravity = -350
                    frog.flipped = False
                if distance(frog.position, game.player_position) <= 30:
                    die()
                    game.dead = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        game.player_speed -= game.player_acceleration * delta_time
    if keys[pygame.K_d]:
        game.player_speed += game.player_acceleration * delta_time
    if keys[pygame.K_r] and game.dead:
        game = GameState(screen)

    # PLAYER MOVEMENT
    game.player_position.x += game.player_speed * delta_time

    # SCROLLING
    for i, wall in enumerate(game.walls):
        game.walls[i] = [(point[0], point[1] - game.SCROLL_SPEED * delta_time) for point in wall]

        if wall[2][1] < 0:
            coordinate = extend_wall(wall)
            if (random.random() > 0.95 - (game.score / 50000)):
                new_frog = spawn_frog(wall, len(wall) - 1, i)
                if new_frog:
                    game.frogs.append(new_frog)
            game.walls[i].append(coordinate)
            game.walls[i].pop(1)

    game.SCROLL_SPEED *= 1 + (0.005 * delta_time) 
    game.player_acceleration *= 1 + (0.005 * delta_time) 


    for i, frog in enumerate(game.frogs):
        if (frog.position.y < -100):
            game.frogs.pop(i)
            continue
            
        if (game.frogs[i].jump_time > 0):
            game.frogs[i].jump_time -= delta_time
            print(game.frogs[i].jump_time)

        game.frogs[i].position = pygame.Vector2(frog.position.x, frog.position.y - game.SCROLL_SPEED * delta_time)
        
        if (distance(frog.position, game.player_position) < 375):
            if (game.frogs[i].jump_time <= 0 and game.frogs[i].jumped == False):
                game.frogs[i].jumped = True
                game.frogs[i].jump_time = 0.1

                jump_sound.play()
                game.frogs[i].movement_speed = distance(frog.position, game.player_position) * ((game.player_position.x - frog.position.x) / abs(game.player_position.x - frog.position.x)) / 2.5
                if (game.player_position.x > frog.position.x):
                    game.frogs[i].flipped = True

            game.frogs[i].jumped = True
        
        if (frog.jumped):
            game.frogs[i].position.y += frog.current_gravity * delta_time
            game.frogs[i].current_gravity += frog.gravity_scale * delta_time
            game.frogs[i].position.x += frog.movement_speed * delta_time

    game.player_speed *= 0.95 - (1 * delta_time)

    render_left_wall = [point for point in game.left_wall]
    render_left_wall.append((0, screen.height))

    render_right_wall = [point for point in game.right_wall]
    render_right_wall.append((screen.width, screen.height))

    if not(game.dead):
        game.score += 20 * delta_time * (game.SCROLL_SPEED / 300)

    screen.fill("black")

    pygame.draw.polygon(screen, "white", render_left_wall)
    pygame.draw.polygon(screen, "white", render_right_wall)
    player = pygame.draw.circle(screen, "purple", game.player_position, 20)
    screen.blit(blitted_miner, (game.player_position.x - (blitted_miner.width / 2), game.player_position.y - (blitted_miner.height / 2)))
    if game.dead:
        score_surface = my_font.render(f"You Fell {round(game.score)} meters!", False, "white")
        restart_surface = my_font.render("Press 'R' to Restart", False, "white")
        buffer = 20
        background_rect = pygame.Rect(screen.width / 2 - restart_surface.width / 2 - buffer / 2, screen.height / 2 - restart_surface.height / 2 - buffer / 2, restart_surface.width + buffer, restart_surface.height + restart_surface.height + buffer)

        pygame.draw.rect(screen, "black", background_rect, round(background_rect.height / 2), 16)
        screen.blit(score_surface, ((screen.width / 2) - score_surface.width / 2, (screen.height / 2) - score_surface.height / 2))
        screen.blit(restart_surface, ((screen.width / 2) - restart_surface.width / 2, (screen.height / 2) + restart_surface.height / 2))

    for frog in game.frogs:
        if frog.movement_speed < 0:
            blitted_frog = pygame.transform.rotate(frog_sprite, -frog.movement_speed * frog.current_gravity / 1000)
        else:
            blitted_frog = pygame.transform.rotate(frog_sprite, frog.movement_speed * frog.current_gravity / 1000)
        
        if frog.jumped == False:
            blitted_frog = frog_sprite

        if ((game.player_position.x > frog.position.x and frog.jumped == False) or frog.flipped == True):
            blitted_frog = pygame.transform.flip(blitted_frog, True, False)
        
        if (distance(frog.position, game.player_position) < 425 and frog.jumped == False):
            blitted_frog = pygame.transform.scale(blitted_frog, (blitted_frog.width * 1.2, blitted_frog.height * 0.8))


        screen.blit(blitted_frog, (frog.position.x - blitted_frog.width / 2, (frog.position.y - 10) - blitted_frog.height / 2))
    offset = (math.sin(game.score / 10) * 50) + (math.sin(game.score / 2) * 20) + (math.sin(game.score / 8) * 1.75)

    text_surface = my_font.render(f"{str(round(game.score))}m", False, "white")
    screen.blit(text_surface, ((screen.width / 2) - text_surface.width / 2,0))

    #stats_surface = my_font.render(f"SCROLL SPEED: {game.SCROLL_SPEED}\nPLAYER SPEED: {game.player_acceleration}", False, "red")
    #screen.blit(stats_surface, (0, 0))


    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()