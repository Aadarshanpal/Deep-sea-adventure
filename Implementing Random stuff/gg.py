import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Ocean Adventure")

# Colors
BLUE = (0, 100, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Player
player = pygame.Rect(50, 400, 60, 30)

# Obstacles and collectibles
obstacles = []
treasures = []

score = 0
lives = 3
clock = pygame.time.Clock()
running = True
spawn_timer = 0

font = pygame.font.SysFont(None, 36)

while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < 800:
        player.y += 5
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < 600:
        player.x += 5

    # Spawn obstacles and treasures
    spawn_timer += 1
    if spawn_timer % 60 == 0:  # every 1 second
        obstacles.append(pygame.Rect(600, random.randint(0, 770), 60, 30))
        if random.random() < 0.5:
            treasures.append(pygame.Rect(600, random.randint(0, 770), 30, 30))

    # Move obstacles and check collision
    for obs in obstacles[:]:
        obs.x -= 5
        if obs.x < 0:
            obstacles.remove(obs)
        if player.colliderect(obs):
            lives -= 1
            obstacles.remove(obs)

    # Move treasures and check collection
    for tre in treasures[:]:
        tre.x -= 5
        if tre.x < 0:
            treasures.remove(tre)
        if player.colliderect(tre):
            score += 10
            treasures.remove(tre)

    # Draw player, obstacles, treasures
    pygame.draw.rect(screen, WHITE, player)
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)
    for tre in treasures:
        pygame.draw.rect(screen, YELLOW, tre)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Check game over
    if lives <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (200, 400))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()