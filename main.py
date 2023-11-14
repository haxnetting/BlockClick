
import pygame
import os
import pygame.mixer
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 437
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlockClick")

# Ustawienia gry
FPS = 60
VEL = 5.4
GRAVITY = 0.9
JUMP_VEL = -15
MAX_JUMPS = 1
BG_COLOR = (255, 255, 255)

# Wczytanie grafik
PLAYER_IMG = pygame.image.load(os.path.join("assets", "player.png"))
SPIKE_IMG = pygame.image.load(os.path.join("assets", "spike.png"))
BACKGROUND_IMG = pygame.image.load(os.path.join("assets", "background.png"))


# Klasa gracza
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = 500
        self.vel = VEL
        self.jump_vel = JUMP_VEL
        self.jumps = 0
        self.img = PLAYER_IMG
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            self.jump()

        self.rect.center = (self.x, self.y)

    def jump(self):
        if self.jumps < MAX_JUMPS:
            self.jumps += 1
            self.jump_vel = JUMP_VEL

    def update(self):
        self.y += self.jump_vel
        self.jump_vel += GRAVITY

        if self.y > HEIGHT - self.rect.height:
            self.y = HEIGHT - self.rect.height
            self.jumps = 0
            self.jump_vel = 0

    def draw(self, surface):
        surface.blit(self.img, self.rect)

# Klasa przeszkody

class Spike:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = SPIKE_IMG
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        self.hitbox = pygame.Rect(self.x + 0, self.y -0, 8.5, 20)

    def move(self):
        self.x -= VEL
        self.rect.center = (self.x, self.y)
        self.hitbox.center = (self.x, self.y)

    def off_screen(self):
        return self.x < -self.rect.width

    def draw(self, surface):
        surface.blit(self.img, self.rect)

    def draw_hitbox(self, surface):
        hitbox_surface = pygame.Surface((8.5, 20), pygame.SRCALPHA)
        hitbox_surface.set_alpha(0)
        pygame.draw.rect(hitbox_surface, (0, 0, 0), hitbox_surface.get_rect())
        surface.blit(hitbox_surface, self.hitbox)

# Funkcja główna

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    running = True
    paused = False
    pause_time = 3 * FPS
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_screen = False

        WIN.fill(BG_COLOR)
        font = pygame.font.SysFont(None, 45)
        text = font.render("Kliknij lewy przycisk myszy, aby rozpocząć grę!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(text, text_rect)

        pygame.display.update()

    pause_count = pause_time

    player = Player(100, HEIGHT // 2)
    spikes = []

    while running:
        clock.tick(FPS)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.jump()
                if event.button == 3:
                    if paused:
                        paused = False
                        pause_count = pause_time
                    else:
                        paused = True

        # Dodawanie przeszkód
        if len(spikes) == 0 or WIDTH - spikes[-1].x > 250:
            spike = Spike(WIDTH + 50, HEIGHT - 50)
            spikes.append(spike)
            if random.random() < 0.3: 
                spike2 = Spike(WIDTH - 7.5 + spike.rect.width, HEIGHT - 50)
                spikes.append(spike2)
            if random.random() < 0.2:
                spike3 = Spike(WIDTH - 20 + spike.rect.width, HEIGHT - 50)
                spikes.append(spike3)
            

        # Ruch obiektów
        if not paused:
            player.move()
            player.update()

            for spike in spikes:
                spike.move()

                if spike.hitbox.colliderect(player.rect):
                    running = False

                if spike.off_screen():
                    spikes.remove(spike)

        # Rysowanie obiektów
        WIN.blit(BACKGROUND_IMG, (0, 0))

        for spike in spikes:
            spike.draw(WIN)
            spike.draw_hitbox(WIN)

        player.draw(WIN)

        if paused:
            pause_count -= 1
            pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_surface.fill((128, 128, 128, 128))
            font = pygame.font.SysFont(None, 100)
            text = font.render("PAUZA", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pause_surface.blit(text, text_rect)
            WIN.blit(pause_surface, (0, 0))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()