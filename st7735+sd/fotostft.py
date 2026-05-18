from machine import Pin, SPI
import os
import time
import mysd
import st7789
import tft_config

# =========================
# TFT ST7789
# =========================

tft = tft_config.config(0)

tft.init()

# =========================
# SD
# =========================

spi_sd = SPI(
    1,
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(23),
    miso=Pin(19)
)

cs_sd = Pin(13, Pin.OUT)

sd = mysd.SDCard(spi_sd, cs_sd)

vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

print("SD montada")

# =========================
# MOSTRAR JPG
# =========================

def mostrar(nombre):

    tft.fill(st7789.BLACK)

    tft.jpg(nombre, 0, 0, st7789.SLOW)

# =========================
# LOOP
# =========================

while True:

    print("foto-1")
    mostrar("/sd/foto-1.jpg")
    time.sleep(3)

    print("foto-2")
    mostrar("/sd/foto-2.jpg")
    time.sleep(3)

    print("foto-3")
    mostrar("/sd/foto-3.jpg")
    time.sleep(0.5)