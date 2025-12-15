import pygame
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
game_ending = False
font = pygame.font.SysFont("Arial", 36, bold=True)

Shield_activated = False
lives = 3
score = 0


class Draw:
    def __init__(self, screen, color, x, y, width, height, y_speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = screen
        self.color = color
        self.y_speed = y_speed

    def draw_rect(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move_rect(self, other):
        global lives, score, Shield_activated

        # move falling cube
        other.rect.y += other.y_speed

        # paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.x < 0:
                self.rect.x = 0

        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.x > 500 - self.rect.width:
                self.rect.x = 500 - self.rect.width

        # cube off screen -> respawn (shield can block life loss once)
        if other.rect.y > 500:
            other.rect.y = 0
            other.rect.x = random.randint(0, 500 - other.rect.width)

            if Shield_activated:
                Shield_activated = False   # shield absorbs this miss
            else:
                lives -= 1

        # collision -> score + respawn cube
        if other.rect.colliderect(self.rect):
            self.color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            other.rect.y = random.randint(0, 50)
            other.rect.x = random.randint(0, 500 - other.rect.width)
            score += 1


# paddle
paddle = Draw(screen, (250, 0, 0), 225, 480, 100, 10, 0)

power_up = None
power_up_spawned = False

Shield = None
Shield_spawned = False

# start with ONE cube
cubes = [Draw(screen, (255, 0, 0), random.randint(0, 480), 0, 20, 20, 3)]
spawned_second = False


def reset_game():
    global lives, score, game_ending, cubes, spawned_second
    global power_up, power_up_spawned, Shield, Shield_spawned, Shield_activated

    power_up = None
    power_up_spawned = False

    Shield = None
    Shield_spawned = False
    Shield_activated = False

    lives = 3
    score = 0
    game_ending = False
    spawned_second = False
    cubes = [Draw(screen, (255, 0, 0), random.randint(0, 480), 0, 20, 20, 3)]
    paddle.rect.x = 225
    paddle.rect.width = 100


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_ending:
                reset_game()

    screen.fill((0, 0, 0))

    if not game_ending:
        # update gameplay
        for cube in cubes:
            paddle.move_rect(cube)

        # Power Up (green): widen paddle
        random_num_power_up = random.randint(1, 1000)
        if random_num_power_up == 1 and (not power_up_spawned) and power_up is None:
            power_up = Draw(screen, (0, 255, 0), random.randint(0, 480), 0, 20, 20, 3)
            power_up_spawned = True

        if power_up is not None:
            power_up.rect.y += power_up.y_speed
            if power_up.rect.colliderect(paddle.rect):
                power_up = None
                paddle.rect.width += 20
                power_up_spawned = False
            elif power_up.rect.y > 500:
                power_up = None
                power_up_spawned = False

        # Shield (blue): blocks next missed cube
        random_num_shield = random.randint(1, 1000)
        if random_num_shield == 5 and (not Shield_spawned) and Shield is None:
            Shield = Draw(screen, (0, 0, 255), random.randint(0, 480), 0, 20, 20, 3)
            Shield_spawned = True

        if Shield is not None:
            Shield.rect.y += Shield.y_speed
            if Shield.rect.colliderect(paddle.rect):
                Shield = None
                Shield_activated = True
                Shield_spawned = False  # <-- allow shield to spawn again later
            elif Shield.rect.y > 500:
                Shield = None
                Shield_spawned = False  # <-- allow shield to spawn again later

        # spawn second cube when score reaches 5
        if score >= 5 and not spawned_second:
            cubes.append(Draw(screen, (255, 0, 0), random.randint(0, 480), 0, 20, 20, 3))
            spawned_second = True

        # draw gameplay
        paddle.draw_rect()
        for cube in cubes:
            cube.draw_rect()

        if power_up is not None:
            power_up.draw_rect()

        if Shield is not None:
            Shield.draw_rect()

        # HUD
        text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        shield_surface = font.render(f"Shield: {'ON' if Shield_activated else 'OFF'}", True, (255, 255, 255))

        screen.blit(lives_surface, (0, 0))
        screen.blit(text_surface, (320, 0))
        screen.blit(shield_surface, (0, 40))

        if lives <= 0:
            game_ending = True

    else:
        game_over = font.render("Game Over! Press R", True, (255, 255, 255))
        screen.blit(game_over, (60, 220))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
