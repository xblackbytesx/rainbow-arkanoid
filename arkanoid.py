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
screen = pygame.display.set_mode((1920, 1280))
pygame.display.set_caption("Rainbow Arkanoid")

window_width, window_height = screen.get_size()

# Helper for generating randomized colors
def random_color():
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

# Blocks and colors
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
block_colors = [random.choice(colors) for _ in range(150)]

# Particles
particles = []

# Color palette
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Paddle
paddle = pygame.Rect(860, 1000, 200, 20)

# Ball
ball = pygame.Rect(960, 600, 30, 30)
ball_speed = [4, -4]

# Blocks
block_width, block_height = 120, 40
block_rows = 5
level = 1

def create_level(level, block_rows):
    return [pygame.Rect(200 + 140 * x, 100 + 60 * y, block_width, block_height) for y in range(block_rows) for x in range(12)]

blocks = create_level(level, block_rows)

# Galaxy background
stars = [pygame.Rect(random.randint(0, 1920), random.randint(0, 1280), 2, 2) for _ in range(150)]

# Lives and score
lives = 3
score = 0
font = pygame.font.Font(None, 72)

# Sound effects
pygame.mixer.init()
paddle_hit = pygame.mixer.Sound("./assets/audio/paddle_hit.wav")
block_break = pygame.mixer.Sound("./assets/audio/block_break.flac")
wall_bounce = pygame.mixer.Sound("./assets/audio/wall_bounce.wav")
game_over_sound = pygame.mixer.Sound("./assets/audio/game_over.wav")

# Background music
pygame.mixer.music.load("./assets/audio/background_music.wav")
pygame.mixer.music.play(-1)  # Loop background music infinitely

def show_start_level(screen, level, font):
    screen.fill((0, 0, 25))
    level_start_text = font.render(f"Start Level {level}", True, WHITE)
    screen.blit(level_start_text, (320, 300))
    pygame.display.flip()
    pygame.time.delay(2000)

# Game loop
running = True
color_change_timer = 0
ball_speed = [4, -4] # Move ball_speed definition here, outside the while loop

show_start_level(screen, level, font)  # Toon "Start Level 1" aan het begin
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bind paddle to cursor movement
    mouse_x, _ = pygame.mouse.get_pos()
    paddle.centerx = mouse_x
    if paddle.left < 0:
        paddle.left = 0
    if paddle.right > 1920:
        paddle.right = 1920

    # Ball movement
    ball.move_ip(ball_speed[0], ball_speed[1])

    # Detect ball
    if ball.left < 0 or ball.right > 1920:
        ball_speed[0] = -ball_speed[0]
        wall_bounce.play()
    if ball.top < 0:
        ball_speed[1] = -ball_speed[1]
        wall_bounce.play()
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        paddle_hit.play()

    if ball.bottom > 1200:
        lives -= 1
        ball.x, ball.y = 400, 300
        ball_speed = [4, -4]  # Keep the ball speed constant

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

    # Get relative dimensions
    lives_x = window_width * 0.05  # 5% from the left edge of the window
    lives_y = window_height * 0.05  # 5% from the top edge of the window

    score_x = window_width * 0.95 - score_text.get_width()  # 5% from the right edge of the window
    score_y = window_height * 0.05  # 5% from the top edge of the window

    screen.blit(lives_text, (lives_x, lives_y))
    screen.blit(score_text, (score_x, score_y))

    # Update and draw particles
    update_particles(particles, screen)

    pygame.display.flip()
    pygame.time.delay(10)

    # Randomize colors every second
    color_change_timer += 10
    if color_change_timer >= 100:
        block_colors = [random_color() for _ in range(len(blocks))]
        color_change_timer = 0

    # Check if level is complete
    if not blocks:
        level += 1
        blocks = create_level(level, block_rows)
        block_colors = [random.choice(colors) for _ in range(block_rows * 150)]
        ball.x, ball.y = 960, 600
        ball_speed = [4, -4]
        show_start_level(screen, level, font)  # Toon "Start Level X" bij het begin van elk nieuw level

        # Vervang de vorige screen.fill((0, 0, 25)) regel door deze while loop
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            screen.fill((0, 0, 25))
            for star in stars:
                pygame.draw.rect(screen, WHITE, star)
            pygame.draw.rect(screen, BLUE, paddle)
            pygame.draw.circle(screen, GREEN, ball.center, ball.width // 2)
            for i, block in enumerate(blocks):
                pygame.draw.rect(screen, block_colors[i], block)
            pygame.display.flip()

    # Game over
    if lives <= 0:
        game_over_sound.play()  # Play background music
        pygame.mixer.music.stop()  # Stop background music
        screen.fill((0, 0, 25))
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (860, 640))
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
                break

pygame.quit()
sys.exit()