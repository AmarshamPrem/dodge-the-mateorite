import pygame
import random
from pathlib import Path

# Constants
SCREEN_WIDTH = 414
SCREEN_HEIGHT = 736
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


def load_image(name, size=None):
    image = pygame.image.load(ASSETS_DIR / name)
    image = image.convert_alpha() if image.get_alpha() else image.convert()
    if size:
        image = pygame.transform.scale(image, size)
    return image


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Dodge")
clock = pygame.time.Clock()

# Assets
background_image = pygame.transform.scale(load_image("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
rocket_image = load_image("rocket.png", size=(int(SCREEN_WIDTH * 0.22), int(SCREEN_HEIGHT * 0.16)))
meteor_image = load_image("meteorite.png", size=(int(SCREEN_WIDTH * 0.16), int(SCREEN_WIDTH * 0.16)))
game_over_image = load_image("game_over.png", size=(int(SCREEN_WIDTH * 0.72), int(SCREEN_WIDTH * 0.72)))
replay_image = load_image("replay.jpg", size=(int(SCREEN_WIDTH * 0.27), int(SCREEN_WIDTH * 0.27)))
font = pygame.font.SysFont(None, 36)

# Game Variables
score = 0
high_score = 0
game_over = False


class Player:
    def __init__(self):
        self.image = rocket_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160))
        self.hitbox = self.rect.inflate(-28, -40)

    def move(self, dx):
        new_x = self.rect.x + dx
        if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
            self.rect.x = new_x
            self.hitbox = self.rect.inflate(-28, -40)

    def draw(self):
        screen.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, difficulty):
        self.image = meteor_image
        self.rect = self.image.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), -40))
        self.hitbox = self.rect.inflate(-30, -30)
        self.speed = 3.8 + min(6.0, difficulty / 12.0) + random.uniform(0.1, 0.4)

    def fall(self):
        self.rect.y += self.speed
        self.hitbox = self.rect.inflate(-30, -30)

    def draw(self):
        screen.blit(self.image, self.rect)


def reset_game():
    global score, game_over
    score = 0
    game_over = False


def main():
    global high_score, game_over, score
    player = Player()
    obstacles = []
    spawn_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                replay_rect = replay_image.get_rect(center=(SCREEN_WIDTH // 2, 900))
                if replay_rect.collidepoint(event.pos):
                    reset_game()
                    player = Player()
                    obstacles = []
                    spawn_timer = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.move(-7)
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.move(7)
        if keys[pygame.K_r] and game_over:
            reset_game()
            player = Player()
            obstacles = []
            spawn_timer = 0

        if not game_over:
            spawn_timer += 1
            if spawn_timer > 25:
                obstacles.append(Obstacle(score))
                spawn_timer = 0

            for obstacle in obstacles[:]:
                obstacle.fall()
                if obstacle.rect.top > SCREEN_HEIGHT:
                    obstacles.remove(obstacle)
                    score += 1

                if player.hitbox.colliderect(obstacle.hitbox):
                    game_over = True
                    high_score = max(high_score, score)

        screen.blit(background_image, (0, 0))
        player.draw()
        for obstacle in obstacles:
            obstacle.draw()

        score_text = font.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            screen.blit(game_over_image, game_over_image.get_rect(center=(SCREEN_WIDTH // 2, 350)))

            replay_rect = replay_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))
            screen.blit(replay_image, replay_rect)

            replay_text = font.render("Click or press R to replay", True, WHITE)
            screen.blit(replay_text, replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
