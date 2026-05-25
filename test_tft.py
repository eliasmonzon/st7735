import st7789
import tft_config
import time
import math
import vga1_8x8 as font1      # Fuente pequeña
import vga1_16x32 as font2    # Fuente GRANDE
import vga2_8x8 as font3      # Fuente alternativa

# =========================
# TFT
# =========================

tft = tft_config.config(0)

try:
    tft.init()
except:
    pass

# =========================
# TAMAÑO PANTALLA
# =========================

W = 128
H = 160

# =========================
# COLORES
# =========================

BLACK   = st7789.BLACK
WHITE   = st7789.WHITE
RED     = st7789.RED
GREEN   = st7789.GREEN
BLUE    = st7789.BLUE
YELLOW  = st7789.YELLOW
CYAN    = st7789.CYAN
MAGENTA = st7789.MAGENTA

# =========================
# FUNCIONES DE TEXTO CENTRADO
# =========================

def texto_pequeno(msg, y, color):
    """Texto con fuente vga1_8x8 (8x8)"""
    x = (W - (len(msg) * 8)) // 2
    tft.text(font1, msg, x, y, color)

def texto_grande(msg, y, color):
    """Texto con fuente vga1_16x32 (16x32)"""
    x = (W - (len(msg) * 16)) // 2
    tft.text(font2, msg, x, y, color)

def texto_alternativo(msg, y, color):
    """Texto con fuente vga2_8x8 (8x8 estilo retro)"""
    x = (W - (len(msg) * 8)) // 2
    tft.text(font3, msg, x, y, color)

# =========================
# PRUEBA DE FUENTES (Test 1)
# =========================

def test_fonts():
    """Muestra todas las fuentes disponibles"""
    tft.fill(BLACK)
    
    # Título
    texto_pequeno("FONT TEST", 2, WHITE)
    
    # Fuente 1 (vga1_8x8)
    tft.text(font1, "vga1_8x8:", 5, 20, CYAN)
    tft.text(font1, "Texto pequeno", 5, 32, GREEN)
    
    # Fuente 2 (vga1_16x32)
    tft.text(font2, "vga1_16x32:", 5, 50, YELLOW)
    tft.text(font2, "GRANDE", 5, 85, RED)
    
    # Fuente 3 (vga2_8x8)
    tft.text(font3, "vga2_8x8:", 5, 120, MAGENTA)
    tft.text(font3, "retro font", 5, 132, WHITE)
    
    time.sleep(3)

# =========================
# EFECTO PLASMA (Test 2)
# =========================

def plasma():
    """Efecto plasma con texto"""
    for y in range(H):
        for x in range(W):
            r = int(128 + 127 * math.sin(x / 10))
            g = int(128 + 127 * math.sin(y / 8))
            b = int(128 + 127 * math.sin((x + y) / 12))
            color = st7789.color565(r, g, b)
            tft.pixel(x, y, color)
    
    tft.fill_rect(0, 0, W, 20, BLACK)
    texto_pequeno("PLASMA", 2, WHITE)
    texto_alternativo("EFFECT", 12, YELLOW)
    time.sleep(2)

# =========================
# LINEAS (Test 3)
# =========================

def lines():
    """Dibujo de líneas"""
    tft.fill(BLACK)
    
    for x in range(0, W, 6):
        tft.line(0, 0, x, H - 1, RED)
    
    for y in range(0, H, 6):
        tft.line(0, 0, W - 1, y, GREEN)
    
    texto_pequeno("LINES", 5, WHITE)
    texto_alternativo("DEMO", 15, CYAN)
    time.sleep(2)

# =========================
# RECTANGULOS (Test 4)
# =========================

def rects():
    """Rectángulos concéntricos"""
    tft.fill(BLACK)
    
    for s in range(10, 120, 8):
        x = (W - s) // 2
        y = (H - s) // 2
        tft.rect(x, y, s, s, BLUE)
    
    texto_pequeno("RECTS", 5, YELLOW)
    texto_grande("BOX", 40, GREEN)
    time.sleep(2)

# =========================
# ANIMACION CUADRADO REBOTANDO (Test 5)
# =========================

def animation():
    """Cuadrado que rebota con múltiples fuentes"""
    x = 0
    y = 60
    dx = 2
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < 5000:  # 5 segundos
        tft.fill(BLACK)
        
        # Textos con diferentes fuentes
        texto_pequeno("BOUNCE", 5, CYAN)
        texto_alternativo("BOX", 20, YELLOW)
        texto_grande(">", 100, RED)
        
        # Cuadrado rebotando
        tft.fill_rect(x, y, 20, 20, MAGENTA)
        
        x += dx
        
        if x <= 0:
            dx = 2
            texto_grande("<", 100, GREEN)
        
        if x >= W - 20:
            dx = -2
            texto_grande(">", 100, BLUE)
        
        time.sleep_ms(15)
    
    time.sleep(1)

# =========================
# PRUEBA DE COLORES (Test 6)
# =========================

def test_colors():
    """Prueba todos los colores básicos"""
    colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]
    names = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA", "WHITE"]
    
    tft.fill(BLACK)
    texto_pequeno("COLOR TEST", 2, WHITE)
    
    for i, (color, name) in enumerate(zip(colors, names)):
        y = 20 + (i * 18)
        tft.fill_rect(10, y, 30, 12, color)
        tft.text(font1, name, 50, y, WHITE)
        time.sleep_ms(300)
    
    time.sleep(2)

# =========================
# PRUEBA DE RENDIMIENTO (Test 7)
# =========================

def test_performance():
    """Prueba velocidad de llenado"""
    tft.fill(BLACK)
    texto_pequeno("SPEED TEST", 2, WHITE)
    texto_alternativo("Filling...", H//2 - 4, YELLOW)
    
    start = time.ticks_ms()
    
    # Llenar pantalla con diferentes colores
    for i, color in enumerate([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]):
        tft.fill(color)
        time.sleep_ms(50)
    
    elapsed = time.ticks_diff(time.ticks_ms(), start)
    
    tft.fill(BLACK)
    texto_grande(f"{elapsed}ms", H//2 - 16, GREEN)
    texto_pequeno("Fill speed test", H//2 + 10, WHITE)
    
    time.sleep(2)

# =========================
# DEMO FINAL COMPLETA (Test 8)
# =========================

def final_demo():
    """Demo final combinando gráficos y texto"""
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < 6000:  # 6 segundos
        # Fondo degradado
        for y in range(H):
            r = (y * 255) // H
            g = ((H - y) * 255) // H
            b = 128
            tft.line(0, y, W-1, y, st7789.color565(r, g, b))
        
        # Textos combinados
        texto_grande("TFT", 20, BLACK)
        texto_pequeno("128x160", 55, YELLOW)
        texto_alternativo("TEST OK!", 80, WHITE)
        texto_grande("PASS", 120, GREEN)
        
        time.sleep_ms(100)
    
    time.sleep(1)

# =========================
# MENSAJE FINAL
# =========================

def mensaje_final():
    """Mensaje de completado"""
    tft.fill(BLACK)
    
    # Animación de texto
    for _ in range(3):
        texto_grande("OK!", H//2 - 16, GREEN)
        texto_pequeno("TEST COMPLETE", H//2 + 10, WHITE)
        time.sleep(0.5)
        tft.fill(BLACK)
        time.sleep(0.3)
    
    texto_pequeno("TFT funciona!", H//2 - 8, CYAN)
    texto_alternativo("3 fuentes OK", H//2 + 8, YELLOW)
    time.sleep(2)

# =========================
# LOOP PRINCIPAL DE PRUEBAS
# =========================

def run_all_tests():
    """Ejecuta todas las pruebas en secuencia"""
    print("\n=== INICIANDO TEST DE TFT ===")
    
    tests = [
        ("Fuentes", test_fonts),
        ("Plasma", plasma),
        ("Líneas", lines),
        ("Rectángulos", rects),
        ("Animación", animation),
        ("Colores", test_colors),
        ("Rendimiento", test_performance),
        ("Demo Final", final_demo)
    ]
    
    for name, test_func in tests:
        print(f"Ejecutando: {name}...")
        test_func()
    
    mensaje_final()
    
    print("=== TEST COMPLETADO ===")
    print("✓ TFT 128x160 funciona correctamente")
    print("✓ 3 fuentes disponibles:")
    print("  - vga1_8x8 (pequeña)")
    print("  - vga1_16x32 (grande)")
    print("  - vga2_8x8 (alternativa)")

# =========================
# DEMO INFINITA (opcional)
# =========================

def demo_infinita():
    """Demo infinita para mostrar todas las capacidades"""
    demos = [plasma, lines, rects, test_colors, final_demo]
    
    while True:
        for demo in demos:
            demo()
            time.sleep(1)

# =========================
# INICIAR
# =========================

if __name__ == "__main__":
    try:
        # Ejecutar todas las pruebas una vez
        run_all_tests()
        
        # Opcional: demo infinita (descomentar si se quiere)
        # print("\nIniciando demo infinita...")
        # demo_infinita()
        
        # Mantener el último frame
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest interrumpido por usuario")
        tft.fill(BLACK)
        tft.text(font2, "STOP", W//2 - 32, H//2 - 16, RED)
        time.sleep(2)
        tft.fill(BLACK)
        
    except Exception as e:
        print(f"\nError: {e}")
        tft.fill(BLACK)
        tft.text(font1, "ERROR", 5, H//2 - 8, RED)
        tft.text(font1, str(e)[:20], 5, H//2 + 8, YELLOW)
