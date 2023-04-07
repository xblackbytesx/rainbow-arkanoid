import sys
import random
import pygame

def create_particles(x, y, n, colors):
    particles = []
    for _ in range(n):
        particle = pygame.Rect(x, y, 5, 5)
        particle_speed = [random.uniform(-1, 1), random.uniform(-1, 1)]
        particle_color = random.choice(colors)
        particles.append((particle, particle_speed, particle_color))
    return particles

def update_particles(particles, screen):
    for particle, speed, color in particles:
        particle.move_ip(speed)
        pygame.draw.rect(screen, color, particle)

# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rainbow Arkanoid")

# Helper for generating randomized colors
def random_color():
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

# Blocks and colors
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
block_colors = [random.choice(colors) for _ in range(50)]

# Particles
particles = []

# Color palette
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Paddle
paddle = pygame.Rect(300, 500, 100, 10)

# Ball
ball = pygame.Rect(400, 300, 15, 15)
ball_speed = [2, -2]

# Blocks
block_width, block_height = 60, 20
blocks = [pygame.Rect(100 + 70 * x, 50 + 30 * y, block_width, block_height) for y in range(5) for x in range(10)]

# Galaxy background
stars = [pygame.Rect(random.randint(0, 800), random.randint(0, 600), 2, 2) for _ in range(100)]

# Lives and score
lives = 3
score = 0
font = pygame.font.Font(None, 36)

# Sound effects
pygame.mixer.init()
paddle_hit = pygame.mixer.Sound("./assets/audio/paddle_hit.wav")
block_break = pygame.mixer.Sound("./assets/audio/block_break.flac")
wall_bounce = pygame.mixer.Sound("./assets/audio/wall_bounce.wav")
game_over_sound = pygame.mixer.Sound("./assets/audio/game_over.wav")

# Background music
pygame.mixer.music.load("./assets/audio/background_music.wav")
pygame.mixer.music.play(-1)  # Loop background music infinitely

# Game loop
running = True
color_change_timer = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bind paddle to cursor movement
    mouse_x, _ = pygame.mouse.get_pos()
    paddle.centerx = mouse_x
    if paddle.left < 0:
        paddle.left = 0
    if paddle.right > 800:
        paddle.right = 800

    # Ball movement
    ball.move_ip(ball_speed[0], ball_speed[1])

    # Detect ball
    if ball.left < 0 or ball.right > 800:
        ball_speed[0] = -ball_speed[0]
        wall_bounce.play()
    if ball.top < 0:
        ball_speed[1] = -ball_speed[1]
        wall_bounce.play()
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        paddle_hit.play()

    if ball.bottom > 600:
        lives -= 1
        ball.x, ball.y = 400, 300
        ball_speed = [2, -2]

    # Detect blocks
    for i, block in enumerate(blocks):
        if ball.colliderect(block):
            ball_speed[1] = -ball_speed[1]
            block_break.play()
            particles.extend(create_particles(block.x, block.y, 10, colors))
            blocks.pop(i)
            block_colors.pop(i)
            score += 100
            break

    # Refresh screen
    screen.fill((0, 0, 25))
    for star in stars:
        pygame.draw.rect(screen, WHITE, star)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, GREEN, ball.center, ball.width // 2)
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block)

    # Show current sore and remaining lives
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (600, 10))

    # Update and draw particles
    update_particles(particles, screen)

    pygame.display.flip()
    pygame.time.delay(10)

    # Randomize colors every second
    color_change_timer += 10
    if color_change_timer >= 100:
        block_colors = [random_color() for _ in range(len(blocks))]
        color_change_timer = 0

    # Game over
    if lives <= 0:
        game_over_sound.play()  # Play background music
        pygame.mixer.music.stop()  # Stop background music
        screen.fill((0, 0, 25))
        game_over_text = font.render("Game Over", True, WHITE)
        # score_text(screen, "GAME OVER", (640, 350), 48, WHITE)
        # score_text(screen, "Press any key to exit", (640, 400), 24, WHITE)
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
                break

pygame.quit()
sys.exit()