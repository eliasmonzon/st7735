from machine import Pin
import tft_config
import st7789
import vga1_8x8 as font
import time

# =========================================
# TFT HORIZONTAL
# =========================================

tft = tft_config.config(rotation=1)
tft.init()

# =========================================
# COLORES
# =========================================

BLACK   = st7789.BLACK
WHITE   = st7789.WHITE
RED     = st7789.RED
GREEN   = st7789.GREEN
BLUE    = st7789.BLUE
CYAN    = st7789.CYAN
YELLOW  = st7789.YELLOW
MAGENTA = st7789.MAGENTA

colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# =========================================
# PANTALLA
# =========================================

WIDTH = 160
HEIGHT = 128

# =========================================
# BOTONES
# =========================================

LEFT_BTN    = Pin(33, Pin.IN, Pin.PULL_UP)
RIGHT_BTN   = Pin(32, Pin.IN, Pin.PULL_UP)
RESTART_BTN = Pin(25, Pin.IN, Pin.PULL_UP)

# =========================================
# VARIABLES
# =========================================

level = 1
lives = 3

# =========================================
# PALA
# =========================================

paddle_w = 36
paddle_h = 5

paddle_x = WIDTH // 2 - paddle_w // 2
paddle_y = HEIGHT - 12

# =========================================
# PELOTA
# =========================================

ball_r = 3

ball_x = WIDTH // 2
ball_y = HEIGHT - 30

ball_dx = 2
ball_dy = -2

# =========================================
# BLOQUES
# =========================================

blocks = []

# =========================================
# CREAR NIVEL
# =========================================

def create_level():

    global blocks
    global ball_x
    global ball_y
    global ball_dx
    global ball_dy

    blocks = []

    cols = 10
    block_w = WIDTH // cols
    block_h = 10

    rows = 4 + level

    if rows > 7:
        rows = 7

    for r in range(rows):

        for c in range(cols):

            blocks.append({

                "x": c * block_w,
                "y": 15 + (r * block_h),
                "w": block_w,
                "h": block_h,
                "alive": True,
                "color": colors[(r + c) % len(colors)]

            })

    ball_x = WIDTH // 2
    ball_y = HEIGHT - 30

    speed = 2 + level // 2

    if speed > 5:
        speed = 5

    ball_dx = speed
    ball_dy = -speed

# =========================================
# RESET GAME
# =========================================

def reset_game():

    global level
    global lives
    global paddle_x
    global ball_x
    global ball_y
    global ball_dx
    global ball_dy

    level = 1
    lives = 3

    paddle_x = WIDTH // 2 - paddle_w // 2

    ball_x = WIDTH // 2
    ball_y = HEIGHT - 30

    ball_dx = 2
    ball_dy = -2

    tft.fill(BLACK)

    create_level()

# =========================================
# HUD
# =========================================

def draw_hud():

    tft.fill_rect(0, 0, WIDTH, 12, BLACK)

    text = "L:{} V:{}".format(level, lives)

    tft.text(font, text, 2, 2, WHITE)

# =========================================
# DIBUJAR BLOQUES
# =========================================

def draw_blocks():

    for b in blocks:

        if b["alive"]:

            tft.fill_rect(
                b["x"],
                b["y"],
                b["w"],
                b["h"],
                b["color"]
            )

# =========================================
# DIBUJAR PALA
# =========================================

def draw_paddle():

    tft.fill_rect(
        paddle_x,
        paddle_y,
        paddle_w,
        paddle_h,
        CYAN
    )

# =========================================
# DIBUJAR PELOTA
# =========================================

def draw_ball():

    tft.fill_rect(
        ball_x - ball_r,
        ball_y - ball_r,
        ball_r * 2,
        ball_r * 2,
        WHITE
    )

# =========================================
# BORRAR PELOTA
# =========================================

def erase_ball(x, y):

    tft.fill_rect(
        x - ball_r,
        y - ball_r,
        ball_r * 2,
        ball_r * 2,
        BLACK
    )

# =========================================
# GAME OVER
# =========================================

def game_over():

    tft.fill(BLACK)

    tft.text(font, "GAME OVER", 40, 50, RED)
    tft.text(font, "PRESS BUTTON", 25, 75, WHITE)

# =========================================
# NEXT LEVEL
# =========================================

def next_level():

    global level

    level += 1

    tft.fill(BLACK)

    tft.text(font, "LEVEL {}".format(level), 45, 60, GREEN)

    time.sleep(2)

# =========================================
# INICIO
# =========================================

tft.fill(BLACK)

create_level()

# =========================================
# LOOP PRINCIPAL
# =========================================

while True:

    old_ball_x = ball_x
    old_ball_y = ball_y

    old_paddle_x = paddle_x

    # =====================================
    # BOTONES
    # =====================================

    if LEFT_BTN.value() == 0:
        paddle_x -= 5

    if RIGHT_BTN.value() == 0:
        paddle_x += 5

    # =====================================
    # LIMITES PALA
    # =====================================

    if paddle_x < 0:
        paddle_x = 0

    if paddle_x > WIDTH - paddle_w:
        paddle_x = WIDTH - paddle_w

    # =====================================
    # MOVER PELOTA
    # =====================================

    ball_x += ball_dx
    ball_y += ball_dy

    # =====================================
    # REBOTE PAREDES
    # =====================================

    if ball_x <= ball_r:

        ball_x = ball_r
        ball_dx = -ball_dx

    if ball_x >= WIDTH - ball_r:

        ball_x = WIDTH - ball_r
        ball_dx = -ball_dx

    if ball_y <= 12 + ball_r:

        ball_y = 12 + ball_r
        ball_dy = -ball_dy

    # =====================================
    # PERDER VIDA
    # =====================================

    if ball_y > HEIGHT:

        lives -= 1

        ball_x = WIDTH // 2
        ball_y = HEIGHT - 30

        ball_dx = 2
        ball_dy = -2

        if lives <= 0:

            game_over()

            while True:

                if RESTART_BTN.value() == 0:

                    time.sleep_ms(200)

                    reset_game()

                    break

    # =====================================
    # REBOTE PALA
    # =====================================

    if (
        ball_y + ball_r >= paddle_y and
        ball_y - ball_r <= paddle_y + paddle_h and
        ball_x + ball_r >= paddle_x and
        ball_x - ball_r <= paddle_x + paddle_w
    ):

        ball_dy = -abs(ball_dy)

        offset = (
            ball_x - (paddle_x + paddle_w // 2)
        ) // 6

        ball_dx = offset

        if ball_dx == 0:
            ball_dx = 1

        ball_y = paddle_y - ball_r - 1

    # =====================================
    # COLISION BLOQUES
    # =====================================

    alive = 0

    for b in blocks:

        if b["alive"]:

            alive += 1

            if (
                ball_x + ball_r >= b["x"] and
                ball_x - ball_r <= b["x"] + b["w"] and
                ball_y + ball_r >= b["y"] and
                ball_y - ball_r <= b["y"] + b["h"]
            ):

                b["alive"] = False

                tft.fill_rect(
                    b["x"],
                    b["y"],
                    b["w"],
                    b["h"],
                    BLACK
                )

                ball_dy = -ball_dy

                break

    # =====================================
    # SIGUIENTE NIVEL
    # =====================================

    if alive == 0:

        next_level()

        tft.fill(BLACK)

        create_level()

    # =====================================
    # BORRAR OBJETOS
    # =====================================

    erase_ball(old_ball_x, old_ball_y)

    tft.fill_rect(
        old_paddle_x,
        paddle_y,
        paddle_w,
        paddle_h,
        BLACK
    )

    # =====================================
    # DIBUJAR
    # =====================================

    draw_hud()
    draw_blocks()
    draw_paddle()
    draw_ball()

    time.sleep_ms(12)