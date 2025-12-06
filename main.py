import time as t
from pygame import *
from random import randint
import random
import os
import re


# --- Skin loading helper ---
def load_skins(folder: str) -> list:
    """Returns sorted list of 'folder/X.png' paths where X is integer."""
    if not os.path.exists(folder):
        os.makedirs(folder)
        return []
    files = [f for f in os.listdir(folder) if re.match(r"^\d+\.png$", f)]
    files.sort(key=lambda x: int(x.split('.')[0]))  # Sort by number: 1.png, 2.png, 10.png
    return [os.path.join(folder, f) for f in files]


def menu() -> tuple:
    global Fein
    menu_font = font.SysFont('Arial', 40, bold=True)
    title_font = font.SysFont('Arial', 56, bold=True)
    small_font = font.SysFont('Arial', 24)

    # Load skin paths
    bg_skins = load_skins("BG")
    plat_skins = load_skins("Platform")
    ball_skins = load_skins("Skins")

    # Default to first skin if available, else placeholder
    if not bg_skins:
        bg_skins = ["BG\\1.png"]  # fallback to your default
    if not plat_skins:
        plat_skins = ["plat.png"]
    if not ball_skins:
        ball_skins = ["Skins\\2.png"]

    # Current selections (indices)
    bg_idx = 0
    plat_idx = 0
    ball_idx = 0

    # Menu state
    categories = ["Background", "Platform", "Ball", "Play", "Quit"]
    selected = 0  # index in categories

    preview_w, preview_h = 120, 70

    while True:
        # Draw background preview
        try:
            bg_preview = transform.scale(image.load(bg_skins[bg_idx]), (700, 500))
            window.blit(bg_preview, (0, 0))
        except:
            window.fill((30, 30, 30))

        # Semi-transparent overlay
        overlay = Surface((700, 500), SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        window.blit(overlay, (0, 0))

        # Title
        title = title_font.render("PONG! SKINS", True, (255, 255, 255))
        window.blit(title, (700//2 - title.get_width()//2, 40))

        # Category labels & previews
        y_start = 140
        for i, cat in enumerate(categories[:3]):  # Only first 3 are skinnable
            color = (255, 255, 0) if i == selected else (220, 220, 220)
            label = small_font.render(f"{cat}:", True, color)
            window.blit(label, (80, y_start + i*100))

            # Preview box
            preview_rect = Rect(250, y_start + i*100 - 10, preview_w, preview_h)
            draw.rect(window, (60, 60, 60), preview_rect, border_radius=5)
            draw.rect(window, (100, 100, 100), preview_rect, 2, border_radius=5)

            # Load and draw preview image
            try:
                img_path = [bg_skins[bg_idx], plat_skins[plat_idx], ball_skins[ball_idx]][i]
                preview_img = transform.scale(image.load(img_path), (preview_w, preview_h))
                window.blit(preview_img, preview_rect.topleft)
            except Exception as e:
                fallback = small_font.render("?", True, (255, 50, 50))
                window.blit(fallback, (preview_rect.centerx - fallback.get_width()//2,
                                       preview_rect.centery - fallback.get_height()//2))

            # Skin number
            num = small_font.render(f"← →", True, (180, 180, 180))
            window.blit(num, (400, y_start + i*100))
            current_num = small_font.render(str([bg_idx+1, plat_idx+1, ball_idx+1][i]), True, (255, 255, 255))
            window.blit(current_num, (480, y_start + i*100))

        # Play / Quit buttons
        for j in range(2):
            i = 3 + j
            color = (100, 255, 100) if i == selected and j == 0 else \
                    (255, 100, 100) if i == selected and j == 1 else (200, 200, 200)
            label = small_font.render(categories[i], True, color)
            window.blit(label, (700//2 - label.get_width()//2, y_start + (3 + j)*90))

        # Controls hint
        hint = small_font.render("↑/↓: Select | ←/→: Change Skin | ENTER: Confirm", True, (180, 180, 180))
        window.blit(hint, (700//2 - hint.get_width()//2, 470))

        display.update()
        clock.tick(FPS)

        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    selected = (selected - 1) % len(categories)
                elif e.key == K_DOWN:
                    selected = (selected + 1) % len(categories)
                elif e.key == K_LEFT:
                    if selected == 0:
                        bg_idx = (bg_idx - 1) % len(bg_skins)
                    elif selected == 1:
                        plat_idx = (plat_idx - 1) % len(plat_skins)
                    elif selected == 2:
                        ball_idx = (ball_idx - 1) % len(ball_skins)
                elif e.key == K_RIGHT:
                    if selected == 0:
                        bg_idx = (bg_idx + 1) % len(bg_skins)
                    elif selected == 1:
                        plat_idx = (plat_idx + 1) % len(plat_skins)
                    elif selected == 2:
                        ball_idx = (ball_idx + 1) % len(ball_skins)
                elif e.key == K_RETURN:
                    if selected == 3:  # Play
                        return bg_skins[bg_idx], plat_skins[plat_idx], ball_skins[ball_idx]
                    elif selected == 4:  # Quit
                        quit()


# ------------------- INIT -------------------
init()
mixer.init()
font.init()

FPS = 60
Game = True
PATH = __file__[:-8]

window = display.set_mode((700, 500))
display.set_caption("PONG!")
try:
    display.set_icon(image.load("icon.png"))
except:
    pass

# Default skins (will be replaced by menu)
bg_path = PATH + "\\BG\\5.png"
plat_path = "plat.png"
ball_path = PATH + "\\Skins\\2.png"

clock = time.Clock()

mixer.music.load(PATH + "\\Sound\\music.wav")
t1 = t.time()
mixer.music.play()

Hit1 = mixer.Sound(PATH + "\\Sound\\Hit1.wav")  # High pitch
Hit1_ = t.time()
Hit2 = mixer.Sound(PATH + "\\Sound\\Hit2.wav")  # Low pitch
Hit2_ = t.time()


class GameSprite(sprite.Sprite):
    def __init__(self, speed, img, size_x, size_y, x, y, arg) -> None:
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (size_x, size_y))
        self.speed_y = speed
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.other = arg

    def reset(self) -> None:
        window.blit(self.image, (self.rect.x, self.rect.y))

class ScoreDisplay:
    def __init__(self, font, color=(255, 255, 255)):
        self.font = font
        self.color = color
        self.value = 0
        self.surface = font.render("0", True, color)

    def update(self, new_value):
        if new_value != self.value:
            self.value = new_value
            self.surface = self.font.render(str(new_value), True, self.color)
        return self.surface

    def get_width(self):
        return self.surface.get_width()

    def blit_at_right(self, surf, x_right, y):
        # Blit so right edge is at x_right
        surf.blit(self.surface, (x_right - self.surface.get_width(), y))


# Placeholder init (will be reinitialized after menu)
p1 = GameSprite(3, plat_path, 5, 50, 3, 225, 0)  # left
p2 = GameSprite(3, plat_path, 5, 50, 690, 225, 0)  # right
ball = GameSprite(3, ball_path, 5, 5, 348, 248, [1, 1])
bg = transform.scale(image.load(bg_path), (700, 500))

Fein = font.SysFont('Arial', 20)


# ------------------- MENU START -------------------
bg_path, plat_path, ball_path = menu()

# Re-init assets with selected skins
try:
    bg = transform.scale(image.load(bg_path), (700, 500))
except:
    bg = Surface((700, 500))
    bg.fill((50, 50, 50))

p1 = GameSprite(3, plat_path, 5, 50, 3, 225, 0)
p2 = GameSprite(3, plat_path, 5, 50, 690, 225, 0)
ball = GameSprite(3, ball_path, 5, 5, 348, 248, [1, 1])

p1_score = 0
p2_score = 0

menu_timer = t.time()

# ------------------- MAIN LOOP -------------------
while Game:
    menu_timer_ = t.time()
    Hit1__ = t.time()
    Hit2__ = t.time()
    t2 = t.time()
    if t2 - t1 > 8:
        t1 = t.time()
        mixer.music.play()

    for e in event.get():
        if e.type == QUIT:
            Game = False

    window.blit(bg, (0, 0))
    p1.reset()
    p2.reset()
    ball.reset()

    p1_score_disp = ScoreDisplay(Fein)
    p2_score_disp = ScoreDisplay(Fein)

    keys = key.get_pressed()

    # ------- movement -------
    if keys[K_w] and p1.rect.y >= 55:
        p1.rect.y -= p1.speed
    if keys[K_s] and p1.rect.y <= 395:
        p1.rect.y += p1.speed
    if keys[K_p] and p2.rect.y >= 55:
        p2.rect.y -= p1.speed
    if keys[K_l] and p2.rect.y <= 395:
        p2.rect.y += p1.speed

    if keys[K_ESCAPE] and (menu_timer_ - menu_timer > 1):
        # Re-enter menu and update skins
        new_bg, new_plat, new_ball = menu()
        # Update only if changed
        if new_bg != bg_path:
            bg_path = new_bg
            try:
                bg = transform.scale(image.load(bg_path), (700, 500))
            except:
                bg = Surface((700, 500)).fill((60,60,60))
        if new_plat != plat_path:
            plat_path = new_plat
            p1 = GameSprite(3, plat_path, 5, 50, 3, 225, 0)
            p2 = GameSprite(3, plat_path, 5, 50, 690, 225, 0)
        if new_ball != ball_path:
            ball_path = new_ball
            ball = GameSprite(3, ball_path, 5, 5, 348, 248, [1, 1])
        menu_timer = t.time()

    # ------- ball mov -------
    if ball.other[0]:
        ball.rect.x += ball.speed
    else:
        ball.rect.x -= ball.speed

    # LEFT PADDLE collision
    if ball.rect.x <= 5 and p1.rect.colliderect(ball.rect):
        raw_speed_y = (ball.rect.centery - p1.rect.centery) / 10
        # Enforce minimum vertical speed to prevent horizontal-only movement
        if abs(raw_speed_y) < 1.5:
            raw_speed_y = 1.5 if raw_speed_y >= 0 else -1.5
        ball.speed_y = raw_speed_y
        ball.other[0] = 1
        Hit1_ = t.time()
        Hit1.play()
    # LEFT MISS
    if ball.rect.x <= 0 and not p1.rect.colliderect(ball.rect):
        p2_score += 1
        ball.other[0] = 1
        ball.rect.x = 348
        ball.rect.y = 248
        ball.speed_y = 3

    # RIGHT PADDLE collision
    if ball.rect.x >= 685 and p2.rect.colliderect(ball.rect):
        raw_speed_y = (ball.rect.centery - p2.rect.centery) / 10
        # Enforce minimum vertical speed
        if abs(raw_speed_y) < 1.5:
            raw_speed_y = 1.5 if raw_speed_y >= 0 else -1.5
        ball.speed_y = raw_speed_y
        ball.other[0] = 0
        Hit1_ = t.time()
        Hit1.play()

    # RIGHT MISS
    if ball.rect.x >= 695 and not p2.rect.colliderect(ball.rect):
        p1_score += 1
        ball.other[0] = 0
        ball.rect.x = 348
        ball.rect.y = 248
        ball.speed_y = 3

    # Vertical movement
    if ball.other[1]:
        ball.rect.y += ball.speed_y
    else:
        ball.rect.y -= ball.speed_y

    
    # Top wall (y = 50)
    if ball.rect.top <= 50:
         # In top/bottom collision:
        ball.speed_y = max(1.5, abs(ball.speed_y)) * (1 + random.uniform(-0.1, 0.1))
        ball.rect.top = 50
        ball.other[1] = 1  # move down
        # Optional: add slight randomization to prevent perfect loops
        # ball.speed_y = max(1.5, abs(ball.speed_y))  # ensure min speed
        Hit2_ = t.time()
        Hit2.play()

    # Bottom wall (y = 450)
    if ball.rect.bottom >= 450:
        # In top/bottom collision:
        ball.speed_y = max(1.5, abs(ball.speed_y)) * (1 + random.uniform(-0.1, 0.1))
        ball.rect.bottom = 450
        ball.other[1] = 0  # move up
        # ball.speed_y = max(1.5, abs(ball.speed_y))
        Hit2_ = t.time()
        Hit2.play()

    # --- Stable score display (units digit stays in place for both sides) ---
    p1_txt = str(p1_score)
    p2_txt = str(p2_score)

    p1_surface = Fein.render(p1_txt, True, (255, 255, 255))
    p2_surface = Fein.render(p2_txt, True, (255, 255, 255))

    # Left score: right-align at x=80 (so units digit is always at x=80)
    window.blit(p1_surface, (20, 20))

    # Right score: right-align at x=690 (so units digit is always at x=690)
    window.blit(p2_surface, (680 - p2_surface.get_width(), 20))
    

    display.update()
    clock.tick(FPS)