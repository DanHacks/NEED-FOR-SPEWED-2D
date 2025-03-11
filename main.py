import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODED BY HYDAN - NFS 2D Racing")

# Colors
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Load images
car_images = [
    pygame.image.load("assets/car.png"),
    pygame.image.load("assets/car1.png")
]
obstacle_img = pygame.image.load("assets/obstacle.png")
police_img = pygame.image.load("assets/police.png")
nitro_img = pygame.image.load("assets/nitro.png")
coin_img = pygame.image.load("assets/coin.png")
life_img = pygame.image.load("assets/life.png")
road_img = pygame.image.load("assets/road.png")

# Resize images
car_images = [pygame.transform.scale(img, (60, 100)) for img in car_images]
obstacle_img = pygame.transform.scale(obstacle_img, (60, 60))
police_img = pygame.transform.scale(police_img, (60, 100))
nitro_img = pygame.transform.scale(nitro_img, (40, 40))
coin_img = pygame.transform.scale(coin_img, (40, 40))
life_img = pygame.transform.scale(life_img, (40, 40))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Load sounds
crash_sound = pygame.mixer.Sound("assets/crash.wav")
pygame.mixer.music.load("assets/racing.mp3")

# Game modes
GAME_MODES = {
    "Easy": {"speed": 4, "obstacles": 2, "police": 1, "color": GREEN},
    "Medium": {"speed": 6, "obstacles": 4, "police": 2, "color": YELLOW},
    "Hard": {"speed": 8, "obstacles": 6, "police": 3, "color": RED}
}

# Font
font = pygame.font.Font(None, 40)

# Game selection screen
def game_selection():
    global selected_mode
    running = True
    mode_list = list(GAME_MODES.keys())
    selected_index = 1  # Default to Medium

    while running:
        screen.fill((0, 0, 0))

        title = font.render("SELECT GAME MODE", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 100, 50))

        for i, mode in enumerate(mode_list):
            color = GAME_MODES[mode]["color"]
            text = font.render(mode, True, color)
            screen.blit(text, (WIDTH // 2 - 50, 150 + i * 50))

            if i == selected_index:
                pygame.draw.rect(screen, color, (WIDTH // 2 - 100, 140 + i * 50, 200, 40), 3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_index > 0:
                    selected_index -= 1
                elif event.key == pygame.K_DOWN and selected_index < len(mode_list) - 1:
                    selected_index += 1
                elif event.key == pygame.K_RETURN:
                    selected_mode = mode_list[selected_index]
                    running = False

game_selection()

# Initialize game variables
selected_car = 0
car_x, car_y = WIDTH // 2, HEIGHT - 120
car_speed_x = 5
car_speed_y = 5
max_speed = GAME_MODES[selected_mode]["speed"]
lives = 4
score = 0
nitro_active = False
nitro_timer = 0

# Obstacles, Police, Nitro, Coins, Life
obstacles = [{"x": random.randint(100, WIDTH - 100), "y": -100} for _ in range(GAME_MODES[selected_mode]["obstacles"])]
police = [{"x": random.randint(100, WIDTH - 100), "y": -200} for _ in range(GAME_MODES[selected_mode]["police"])]
nitro = {"x": random.randint(100, WIDTH - 100), "y": -500}
coin = {"x": random.randint(100, WIDTH - 100), "y": -300}
heart = {"x": random.randint(100, WIDTH - 100), "y": -700}

# Game loop
running = True
pygame.mixer.music.play(-1)

while running:
    screen.blit(road_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Car movement
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed_x
    if keys[pygame.K_RIGHT] and car_x < WIDTH - 60:
        car_x += car_speed_x
    if keys[pygame.K_UP] and car_y > 0:
        car_y -= car_speed_y
    if keys[pygame.K_DOWN] and car_y < HEIGHT - 100:
        car_y += car_speed_y

    # Nitro activation
    if keys[pygame.K_b] and nitro_timer == 0:
        nitro_active = True
        nitro_timer = 120  # Nitro lasts 2 seconds (120 frames)
        score += 100  # Nitro gives extra 100 points

    if nitro_active:
        nitro_timer -= 1
        if nitro_timer <= 0:
            nitro_active = False

    # Update obstacles
    for obj in obstacles:
        obj["y"] += max_speed
        if obj["y"] > HEIGHT:
            obj["y"] = -100
            obj["x"] = random.randint(100, WIDTH - 100)

    # Update police
    for cop in police:
        cop["y"] += max_speed
        if cop["y"] > HEIGHT:
            cop["y"] = -200
            cop["x"] = random.randint(100, WIDTH - 100)

    # Update nitro, coins, heart
    nitro["y"] += max_speed
    coin["y"] += max_speed
    heart["y"] += max_speed

    # Reset objects if they go off-screen
    for item in [nitro, coin, heart]:
        if item["y"] > HEIGHT:
            item["y"] = -random.randint(300, 700)
            item["x"] = random.randint(100, WIDTH - 100)

    # Draw elements
    screen.blit(car_images[selected_car], (car_x, car_y))
    for obj in obstacles:
        screen.blit(obstacle_img, (obj["x"], obj["y"]))
    for cop in police:
        screen.blit(police_img, (cop["x"], cop["y"]))

    screen.blit(nitro_img, (nitro["x"], nitro["y"]))
    screen.blit(coin_img, (coin["x"], coin["y"]))
    screen.blit(life_img, (heart["x"], heart["y"]))

    # Collision detection
    car_rect = pygame.Rect(car_x, car_y, 60, 100)

    # Check collisions
    if car_rect.colliderect(pygame.Rect(nitro["x"], nitro["y"], 40, 40)):
        nitro["y"] = HEIGHT + 50
        nitro_timer = 120  # 2-second invincibility
        score += 100  # +100 points

    if car_rect.colliderect(pygame.Rect(coin["x"], coin["y"], 40, 40)):
        coin["y"] = HEIGHT + 50
        score += 10  # +10 points

    if car_rect.colliderect(pygame.Rect(heart["x"], heart["y"], 40, 40)) and lives < 4:
        heart["y"] = HEIGHT + 50
        lives += 1  # Gain 1 life

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, (255, 215, 0))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 60))

    pygame.display.update()

pygame.quit()
