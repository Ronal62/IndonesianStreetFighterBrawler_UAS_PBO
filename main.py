import pygame
from pygame import mixer
from fighter import Warrior, Wizard

# Inisialisasi mixer dan pygame
mixer.init()
pygame.init()

# Buat jendela permainan
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Atur framerate
clock = pygame.time.Clock()
FPS = 60

# Definisi warna
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Variabel permainan
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Skor pemain [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Data petarung
WARRIOR_DATA = {"size": 162, "scale": 4, "offset": [72, 56]}
WIZARD_DATA = {"size": 250, "scale": 3, "offset": [112, 107]}

# Muat musik dan suara
mixer.music.load("assets/audio/music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1, 0.0, 5000)
sword_fx = mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Muat gambar latar belakang
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Muat spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Muat gambar kemenangan
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Langkah animasi petarung
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Definisi font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Fungsi untuk menggambar teks
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Fungsi untuk menggambar latar belakang
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Fungsi untuk menggambar bilah kesehatan
def draw_health_bar(health, x, y):
    ratio = health / 100
    bar_width = 400
    bar_height = 30

    # Gambar latar belakang bar (putih)
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, bar_width + 4, bar_height + 4))

    # Gambar bar kesehatan (merah)
    pygame.draw.rect(screen, RED, (x, y, bar_width * ratio, bar_height))

# Buat dua instance petarung dengan inheritance
fighter_1 = Warrior(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Wizard(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Loop permainan
run = True
while run:
    clock.tick(FPS)

    # Gambar latar belakang
    draw_bg()

    # Tampilkan statistik pemain
    draw_health_bar(fighter_1.get_health(), 20, 20)
    draw_health_bar(fighter_2.get_health(), 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # Perbarui countdown
    if intro_count <= 0:
        # Gerakkan petarung
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # Tampilkan countdown
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # Perbarui timer countdown
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Perbarui dan gambar petarung
    fighter_1.update()
    fighter_2.update()
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Periksa jika salah satu pemain kalah
    if not round_over:
        if not fighter_1.is_alive():
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.is_alive():
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Tampilkan gambar kemenangan
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1.reset(200, 310)
            fighter_2.reset(700, 310)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Perbarui tampilan
    pygame.display.update()

# Keluar dari pygame
pygame.quit()
