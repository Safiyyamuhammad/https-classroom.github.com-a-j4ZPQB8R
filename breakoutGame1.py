import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#load sound file
paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
brick_hit_sound = pygame.mixer.Sound("brick_hit.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
# Settings
PADDLE_WIDTH, PADDLE_HEIGHT = 200, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
ROWS, COLS = 5, 8

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = BLUE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.move_ip(-6, 0)
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.move_ip(6, 0)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = RED
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Create bricks
bricks = [Brick(30 + c * (BRICK_WIDTH + 10), 30 + r * (BRICK_HEIGHT + 10)) for r in range(ROWS) for c in range(COLS)]

# Create paddle and ball
paddle = Paddle()
ball = Ball()
# Score
score = 0
font = pygame.font.Font(None, 36)

# Main loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    ball.move()

    # Ball collision with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.dy = -ball.dy
        paddle_hit_sound.play()

    # Ball collision with bricks
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.dy = -ball.dy
            bricks.remove(brick)
            score += 10
            brick_hit_sound.play()
            break

    # Ball falls below screen
    if ball.rect.top >= HEIGHT:
        ball.reset()
        game_over_sound.play()


    # Draw everything
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
# Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()