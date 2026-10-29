"""Network Defender - a network-security themed action game (Pygame).

File sections:
  1. SETTINGS & COLORS - screen size, colors, difficulty levels
  2. TEXTS             - 4-language text dictionary (EN, AZ, TR, RU)
  3. UTILITIES         - helper functions (IP generation, color calculation, distance)
  4. OBJECTS           - Button, Particle, Packet, MatrixRain, Node classes
  5. MAIN APPLICATION  - GameApp: menu, game, pause, drawing, events

Game rules: click RED (hacker) packets to block them, let GREEN (user) packets reach the server.
ESC or P pauses the game.
"""

import pygame
import random
import math
import sys
import colorsys

# =========================================================================== #
# SETTINGS & COLORS (Theme: Cyberpunk / Hacker)
# =========================================================================== #
WIDTH, HEIGHT = 1280, 720
FPS = 60

C_BG = (8, 12, 24)
C_CORE = (0, 200, 255)
C_NORMAL = (46, 172, 118)
C_HACKER = (255, 40, 75)
C_TEXT = (220, 230, 255)
C_HOVER = (255, 255, 255)
C_PANEL = (20, 28, 48)
C_GRID = (20, 40, 60)

# Difficulty levels: health, hacker probability, speed multiplier
DIFFICULTIES = [
    {"hp": 5, "hack": 0.25, "spd": 0.8},   # Easy
    {"hp": 3, "hack": 0.35, "spd": 1.0},   # Normal
    {"hp": 2, "hack": 0.45, "spd": 1.25},  # Hard
]

# =========================================================================== #
# LANGUAGES DICTIONARY
# =========================================================================== #
TEXTS = {
    "EN": {
        "play": "INITIALIZE SYSTEM", "set": "SECURITY SETTINGS", "lang": "LANGUAGE: EN", "exit": "DISCONNECT (EXIT)",
        "back": "RETURN TO MAIN", "retry": "REBOOT SYSTEM", "fail": "CRITICAL SYSTEM FAILURE",
        "score": "SECURITY SCORE: ", "hp": "SYSTEM INTEGRITY: ", "banned": "BANNED IPs: ", "lang_title": "LANGUAGE SETTINGS",
        "l_fx": "VISUAL EFFECTS: ", "l_diff": "DIFFICULTY: ", "l_grid": "BACKGROUND ANIMATION: ",
        "l_tip": "PACKET INFO: ", "l_full": "FULLSCREEN: ", "on": "ON", "off": "OFF",
        "diff_names": ["EASY", "NORMAL", "HARD"],
        "about_btn": "ABOUT THE GAME", "about_title": "ABOUT",
        "about_g": "Network Defender is an action game about network security.",
        "about_t": "-- SYSTEM MANUAL --",
        "about_1": "Protect the core server from incoming hacker attacks.",
        "about_2": "Click on RED packets to ban them from the network.",
        "about_3": "Let GREEN user packets pass safely.",
        "about_dev_t": "-- DEVELOPER --",
        "dev": "Developer: Vaqif Ismayilov", "ver": "Version: 2.0 (Pygame Engine)",
        "built": "Built with Python & Pygame",
        "sub": "> DEFEND THE NETWORK. BAN THE HACKERS.",
        "online": "SYSTEM ONLINE", "uptime": "UPTIME",
        "paused": "SYSTEM PAUSED", "resume": "RESUME", "pause_hint": "Press ESC or P to resume"
    },
    "AZ": {
        "play": "SİSTEMİ BAŞLAT", "set": "TƏHLÜKƏSİZLİK AYARLARI", "lang": "DİL: AZ", "exit": "SİSTEMDƏN ÇIXIŞ",
        "back": "ƏSAS MENYUYA QAYIT", "retry": "YENİDƏN BAŞLAT", "fail": "KRİTİK SİSTEM XƏTASI",
        "score": "TƏHLÜKƏSİZLİK XALI: ", "hp": "SİSTEM CANI: ", "banned": "BLOKLANAN IP: ", "lang_title": "DİL SEÇİMİ",
        "l_fx": "VİZUAL EFEKTLƏR: ", "l_diff": "ÇƏTİNLİK: ", "l_grid": "FON ANİMASİYASI: ",
        "l_tip": "PAKET MƏLUMATI: ", "l_full": "TAM EKRAN: ", "on": "AÇIQ", "off": "BAĞLI",
        "diff_names": ["ASAN", "NORMAL", "ÇƏTİN"],
        "about_btn": "OYUN HAQQINDA", "about_title": "HAQQINDA",
        "about_g": "Network Defender şəbəkə təhlükəsizliyi mövzusunda aksiya oyunudur.",
        "about_t": "-- OYUN TƏLİMATI --",
        "about_1": "Mərkəzi serveri haker hücumlarından qoruyun.",
        "about_2": "QIRMIZI paketləri klikləyərək sistemdən bloklayın.",
        "about_3": "YAŞIL istifadəçi paketlərini təhlükəsiz buraxın.",
        "about_dev_t": "-- TƏRTİBATÇI --",
        "dev": "Tərtibatçı: Vaqif İsmayılov", "ver": "Versiya: 2.0 (Pygame Mühərriki)",
        "built": "Python və Pygame ilə hazırlanıb",
        "sub": "> ŞƏBƏKƏNİ QORU. HAKERLƏRİ BLOKLA.",
        "online": "SİSTEM AKTİVDİR", "uptime": "İŞLƏMƏ VAXTI",
        "paused": "SİSTEM DAYANDIRILDI", "resume": "DAVAM ET", "pause_hint": "Davam etmək üçün ESC və ya P basın"
    },
    "TR": {
        "play": "SİSTEMİ BAŞLAT", "set": "GÜVENLİK AYARLARI", "lang": "DİL: TR", "exit": "BAĞLANTIYI KES",
        "back": "ANA MENÜYE DÖN", "retry": "SİSTEMİ YENİDEN BAŞLAT", "fail": "KRİTİK SİSTEM HATASI",
        "score": "GÜVENLİK SKORU: ", "hp": "SİSTEM BÜTÜNLÜĞÜ: ", "banned": "YASAKLI IP: ", "lang_title": "DİL AYARLARI",
        "l_fx": "GÖRSEL EFEKTLER: ", "l_diff": "ZORLUK: ", "l_grid": "ARKA PLAN ANİMASYONU: ",
        "l_tip": "PAKET BİLGİSİ: ", "l_full": "TAM EKRAN: ", "on": "AÇIK", "off": "KAPALI",
        "diff_names": ["KOLAY", "NORMAL", "ZOR"],
        "about_btn": "OYUN HAKKINDA", "about_title": "HAKKINDA",
        "about_g": "Network Defender, ağ güvenliği temalı bir aksiyon oyunudur.",
        "about_t": "-- SİSTEM KILAVUZU --",
        "about_1": "Merkezi sunucuyu hacker saldırılarından koruyun.",
        "about_2": "KIRMIZI paketlere tıklayarak onları engelleyin.",
        "about_3": "YEŞİL kullanıcı paketlerine izin verin.",
        "about_dev_t": "-- GELİŞTİRİCİ --",
        "dev": "Geliştirici: Vaqif İsmayılov", "ver": "Sürüm: 2.0 (Pygame Motoru)",
        "built": "Python ve Pygame ile yapıldı",
        "sub": "> AĞI KORU. HACKER'LARI ENGELLE.",
        "online": "SİSTEM ÇEVRİMİÇİ", "uptime": "ÇALIŞMA SÜRESİ",
        "paused": "SİSTEM DURAKLATILDI", "resume": "DEVAM ET", "pause_hint": "Devam için ESC veya P tuşuna basın"
    },
    "RU": {
        "play": "ЗАПУСК СИСТЕМЫ", "set": "НАСТРОЙКИ БЕЗОПАСНОСТИ", "lang": "ЯЗЫК: RU", "exit": "ОТКЛЮЧЕНИЕ (ВЫХОД)",
        "back": "В ГЛАВНОЕ МЕНЮ", "retry": "ПЕРЕЗАГРУЗКА", "fail": "КРИТИЧЕСКИЙ СБОЙ",
        "score": "ОЧКИ ЗАЩИТЫ: ", "hp": "ЦЕЛОСТНОСТЬ: ", "banned": "ЗАБЛОКИРОВАНО: ", "lang_title": "ВЫБОР ЯЗЫКА",
        "l_fx": "ВИЗУАЛЬНЫЕ ЭФФЕКТЫ: ", "l_diff": "СЛОЖНОСТЬ: ", "l_grid": "АНИМАЦИЯ ФОНА: ",
        "l_tip": "ИНФО О ПАКЕТЕ: ", "l_full": "ПОЛНЫЙ ЭКРАН: ", "on": "ВКЛ", "off": "ВЫКЛ",
        "diff_names": ["ЛЕГКО", "НОРМА", "СЛОЖНО"],
        "about_btn": "ОБ ИГРЕ", "about_title": "ОБ ИГРЕ",
        "about_g": "Network Defender — экшен-игра о сетевой безопасности.",
        "about_t": "-- РУКОВОДСТВО --",
        "about_1": "Защитите центральный сервер от хакерских атак.",
        "about_2": "Нажимайте на КРАСНЫЕ пакеты, чтобы блокировать их.",
        "about_3": "Пропускайте ЗЕЛЕНЫЕ пакеты пользователей.",
        "about_dev_t": "-- РАЗРАБОТЧИК --",
        "dev": "Разработчик: Вагиф Исмаилов", "ver": "Версия: 2.0 (Движок Pygame)",
        "built": "Создано на Python и Pygame",
        "sub": "> ЗАЩИТИ СЕТЬ. БЛОКИРУЙ ХАКЕРОВ.",
        "online": "СИСТЕМА В СЕТИ", "uptime": "АПТАЙМ",
        "paused": "СИСТЕМА НА ПАУЗЕ", "resume": "ПРОДОЛЖИТЬ", "pause_hint": "Нажмите ESC или P, чтобы продолжить"
    }
}

# =========================================================================== #
# UTILITIES
# =========================================================================== #
def generate_ip():
    """Creates a random IPv4 address (e.g. '187.23.4.91') and returns it as a string.
    The four parts are generated separately (int -> str conversion), then joined with dots. Called by
    Packet.__init__ so that every packet has its own unique IP.
    """
    parts = [str(random.randint(100, 255)), str(random.randint(1, 255)),
             str(random.randint(0, 10)), str(random.randint(1, 255))]
    return ".".join(parts)

# LAMBDA: a short anonymous function that calculates the distance between two points (x1,y1) and (x2,y2).
# Used everywhere to check the distance between the mouse and a packet.
calc_dist = lambda x1, y1, x2, y2: math.hypot(x1 - x2, y1 - y2)


def hsv(h, s=1.0, v=1.0):
    """Converts an HSV color (h, s, v: 0..1) to an RGB tuple (0..255) that pygame understands.
    h - hue (0 red, ~0.5 cyan, ~0.8 purple), s - saturation, v - brightness. Used so that the colors
    of titles and background elements flow over time.
    """
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def lerp_color(a, b, t):
    """Blends between two colors (linear interpolation).
    a - start color, b - end color, t - between 0..1. t=0 -> a, t=1 -> b, t=0.5 -> the middle. If t is
    out of range it is clamped to 0..1. Used for button hover animation and faded colors.
    """
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# =========================================================================== #
# OBJECTS
# =========================================================================== #
class Button:
    """Animated button: grows and glows on hover, slides in from the sides when entering the screen.
    """
    def __init__(self, x, y, w, h, text, font, accent_color=C_CORE):
        """Creates the button. x, y, w, h - position and size; text - label; font - font; accent_color -
        the main color of the button.
        hover_t (0..1) is the state of the hover animation, appear (0..1) is the state of the
        screen-entry animation.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.accent_color = accent_color
        self.is_hovered = False
        self.hover_t = 0.0      # 0..1 smooth animation
        self.appear = 1.0       # 0..1 screen-entry animation
        self.delay = 0.0
        self.slide_dir = -1

    def reset_anim(self, delay, direction):
        """Restarts the entry animation. delay - how many seconds to wait, direction - -1 slides in
        from the left, +1 from the right.
        """
        self.appear = 0.0
        self.delay = delay
        self.slide_dir = direction
        self.hover_t = 0.0

    def check_hover(self, mouse_pos):
        """Sets is_hovered=True if the mouse is over the button, otherwise False."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def update(self, dt, mouse_pos):
        """Called every frame. Checks hover, increases 'appear' once the delay is over, and smoothly
        moves hover_t toward the target (1 when hovered, otherwise 0). dt - seconds since the last
        frame.
        """
        self.check_hover(mouse_pos)
        if self.delay > 0:
            self.delay -= dt
        else:
            self.appear = min(1.0, self.appear + dt * 3.5)
        target = 1.0 if self.is_hovered else 0.0
        self.hover_t += (target - self.hover_t) * min(1.0, dt * 14)

    def draw(self, surf):
        """Draws the button: glow, fill, border, left indicator and text.
        If the text does not fit in the button, it is automatically shrunk. If the animation has not
        started yet (appear<=0), nothing is drawn.
        """
        if self.appear <= 0:
            return
        e = 1 - (1 - self.appear) ** 3
        off = int((1 - e) * 500 * self.slide_dir)
        h = self.hover_t
        r = self.rect.inflate(int(14 * h), int(6 * h)).move(off, 0)

        # Glow
        if h > 0.02:
            glow = pygame.Surface((r.w + 70, r.h + 70), pygame.SRCALPHA)
            for i in range(5, 0, -1):
                a = int(75 * h * (1 - i / 6))
                gr = pygame.Rect(35, 35, r.w, r.h).inflate(i * 10, i * 10)
                pygame.draw.rect(glow, (*self.accent_color, a), gr, border_radius=12 + i * 3)
            surf.blit(glow, (r.x - 35, r.y - 35))

        fill = lerp_color(C_PANEL, self.accent_color, h)
        pygame.draw.rect(surf, fill, r, border_radius=10)
        pygame.draw.rect(surf, self.accent_color, r, width=2, border_radius=10)

        # Small indicator on the left side
        tick_col = lerp_color(self.accent_color, C_BG, h)
        pygame.draw.rect(surf, tick_col, (r.x + 10, r.centery - 9, 4, 18), border_radius=2)

        text_color = lerp_color(C_TEXT, C_BG, h)
        ts = self.font.render(self.text, True, text_color)
        if ts.get_width() > r.w - 50:  # shrink long text if it does not fit in the button
            k = (r.w - 50) / ts.get_width()
            ts = pygame.transform.smoothscale(ts, (int(ts.get_width() * k), int(ts.get_height() * k)))
        surf.blit(ts, ts.get_rect(center=r.center))

    def is_clicked(self, event):
        """Returns True if the left button is pressed and the mouse is over the button (and the
        animation is almost finished).
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.appear > 0.6:
                return True
        return False


class Particle:
    """A small colored circle that scatters during an explosion."""
    def __init__(self, x, y, color):
        """Spawns with a random direction and speed. life=1.0 means fully visible; it disappears as it
        drops to 0.
        """
        self.x, self.y = x, y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 6)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.life, self.color = 1.0, color

    def update(self, dt):
        """Moves the particle by its velocity and reduces its life. The '60 * dt' factor gives the same
        speed regardless of FPS.
        """
        self.x += self.vx * 60 * dt
        self.y += self.vy * 60 * dt
        self.life -= dt * 1.5

    def draw(self, surf):
        """Draws the particle as a circle that shrinks and becomes transparent as its life decreases."""
        if self.life > 0:
            alpha = int(255 * self.life)
            radius = max(1, int(5 * self.life))
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (radius, radius), radius)
            surf.blit(s, (self.x - radius, self.y - radius))


class Packet:
    """A network packet. If is_hacker=True it is a red virus, otherwise a green envelope. Travels from
    the edge of the screen toward the server in the center.
    """
    def __init__(self, cx, cy, hack_chance=0.35, speed_mult=1.0):
        """cx, cy - server center. hack_chance - probability that the packet is a hacker (0..1),
        speed_mult - difficulty speed multiplier.
        The packet spawns around the server at a random angle, slightly outside the screen. IP, LOAD
        (high for hackers), speed and color are assigned.
        """
        angle = random.uniform(0, math.tau)
        dist = 780  # spawns slightly outside the edge of the screen (it used to be too far away)
        self.x, self.y = cx + math.cos(angle) * dist, cy + math.sin(angle) * dist
        self.cx, self.cy = cx, cy

        self.ip = generate_ip()
        self.is_hacker = random.random() < hack_chance
        self.load = random.randint(50, 150) if self.is_hacker else random.randint(1, 10)
        base = random.uniform(66, 120) if self.is_hacker else random.uniform(44, 88)
        self.speed = base * speed_mult
        self.radius = 14
        self.spin = random.uniform(0, math.tau)
        self.angle = math.atan2(cy - self.y, cx - self.x)
        self.color = C_HACKER if self.is_hacker else C_NORMAL
        self.hovered = False

    def update(self, dt):
        """Moves the packet toward the server (computing the angle and using cos/sin). The hacker shape
        spins while doing this.
        """
        self.angle = math.atan2(self.cy - self.y, self.cx - self.x)
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        if self.is_hacker:
            self.spin += dt * 2.5

    def draw(self, surf, font, show_info=True):
        """Draws the packet: a trail line behind it; a spinning spiky virus for hackers, an envelope for
        users. When the mouse hovers over it, a white ring and (if show_info=True) the IP/LOAD info
        appear.
        """
        x, y = int(self.x), int(self.y)
        col = C_HOVER if self.hovered else self.color

        # Trail left behind
        tx, ty = x - math.cos(self.angle) * 30, y - math.sin(self.angle) * 30
        pygame.draw.line(surf, lerp_color(C_BG, self.color, 0.45), (x, y), (int(tx), int(ty)), 2)

        if self.is_hacker:
            # Attacker: spinning spiky "virus" shape
            pts = []
            for i in range(16):
                r = 17 if i % 2 == 0 else 10
                a = self.spin + i * math.pi / 8
                pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
            pygame.draw.polygon(surf, col, pts)
            pygame.draw.circle(surf, C_BG, (x, y), 8)
            pygame.draw.circle(surf, col, (x - 3, y - 1), 2)
            pygame.draw.circle(surf, col, (x + 3, y - 1), 2)
            pygame.draw.line(surf, col, (x - 3, y + 4), (x + 3, y + 4), 1)
        else:
            # User packet: envelope shape
            rect = pygame.Rect(0, 0, 26, 18)
            rect.center = (x, y)
            pygame.draw.rect(surf, C_BG, rect, border_radius=3)
            pygame.draw.rect(surf, col, rect, 2, border_radius=3)
            pygame.draw.lines(surf, col, False,
                              [(rect.x + 2, rect.y + 3), (x, y + 2), (rect.right - 3, rect.y + 3)], 2)

        if self.hovered:
            pygame.draw.circle(surf, C_HOVER, (x, y), 24, 1)
            if show_info:
                text = font.render(f"IP: {self.ip} | LOAD: {self.load}", True, col)
                surf.blit(text, (self.x + 26, self.y - 10))


class MatrixRain:
    """'Hacker' code raining down in the background (Matrix effect). Each column consists of symbols
    flowing from top to bottom: the head symbol is bright, the tail gradually fades.
    """
    CHARS = "01ABCDEF<>/{}[]#$%&*+=;:"
    ALPHAS = [170, 125, 90, 60, 38, 20]
    PALETTES = [(0, 255, 170), (0, 200, 255), (170, 90, 255), (255, 40, 75)]
    WEIGHTS = [50, 22, 20, 8]

    def __init__(self, font):
        """Creates, once, ready-made images of the symbols for every color palette and every
        transparency level (to avoid re-rendering every frame), and builds all the columns.
        """
        self.cell = 18
        self.glyphs = []   # glyphs[palette][char] -> [alpha levels]
        self.heads = []
        for col in self.PALETTES:
            gp, hp = {}, {}
            for ch in self.CHARS:
                base = font.render(ch, True, col)
                levels = []
                for a in self.ALPHAS:
                    s = base.copy()
                    s.set_alpha(a)
                    levels.append(s)
                gp[ch] = levels
                head = font.render(ch, True, lerp_color(col, (255, 255, 255), 0.7))
                head.set_alpha(235)
                hp[ch] = head
            self.glyphs.append(gp)
            self.heads.append(hp)

        self.columns = []
        for x in range(0, WIDTH, self.cell):
            self.columns.append(self._new_column(x, initial=True))

    def _new_column(self, x, initial=False):
        """Returns a dictionary with random parameters for one column (starting y, speed, length, color
        palette, symbols).
        """
        length = random.randint(8, 22)
        return {
            "x": x,
            "y": random.uniform(-HEIGHT, HEIGHT) if initial else random.uniform(-300, -20),
            "speed": random.uniform(70, 210),
            "len": length,
            "pal": random.choices(range(len(self.PALETTES)), self.WEIGHTS)[0],
            "chars": [random.choice(self.CHARS) for _ in range(length)],
        }

    def update(self, dt):
        """Moves the columns down; restarts a column from the top once it has fully left the screen;
        occasionally changes a random symbol.
        """
        for i, c in enumerate(self.columns):
            c["y"] += c["speed"] * dt
            if c["y"] - c["len"] * self.cell > HEIGHT:
                self.columns[i] = self._new_column(c["x"])
                continue
            if random.random() < dt * 8:
                c["chars"][random.randrange(c["len"])] = random.choice(self.CHARS)

    def draw(self, surf):
        """Draws the columns: the head symbol is bright, the rest fade toward the tail. Those outside
        the screen are skipped.
        """
        cell = self.cell
        for c in self.columns:
            pal, n = c["pal"], c["len"]
            for i in range(n):
                cy = int(c["y"]) - i * cell
                if cy < -cell or cy > HEIGHT:
                    continue
                ch = c["chars"][i]
                if i == 0:
                    surf.blit(self.heads[pal][ch], (c["x"], cy))
                else:
                    lvl = min(5, (i - 1) * 6 // n)
                    surf.blit(self.glyphs[pal][ch][lvl], (c["x"], cy))


class Node:
    """A moving network node (the dots in the background connected to each other by lines)."""
    def __init__(self):
        """Spawns at a random place on the screen with a random speed."""
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-25, 25)
        self.vy = random.uniform(-25, 25)

    def update(self, dt):
        """Moves the node and reverses its direction when it reaches the edge of the screen."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1


# =========================================================================== #
# MAIN APPLICATION
# =========================================================================== #
class GameApp:
    """The main class of the game. Manages the window and the states (menu, play, paused, settings,
    about, language, gameover), events, updating and drawing.
    """
    def __init__(self):
        """Initializes Pygame, creates the window and fonts, prepares the settings, effects and
        buttons, and starts in the menu state.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Network Defender")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 18, bold=True)
        self.set_font = pygame.font.SysFont("consolas", 20, bold=True)
        self.btn_font = pygame.font.SysFont("consolas", 24, bold=True)
        self.title_font = pygame.font.SysFont("consolas", 64, bold=True)
        self.mid_font = pygame.font.SysFont("consolas", 40, bold=True)
        self.rain_font = pygame.font.SysFont("consolas", 16, bold=True)

        self.state = "menu"
        self.lang_code = "EN"

        self.settings = {
            "fx": True,      # visual effects
            "diff": 1,       # 0=easy, 1=normal, 2=hard
            "grid": True,    # background animation
            "tip": True,     # packet info
            "full": False,   # fullscreen
        }

        self.time_passed = 0.0
        self.sub_start = 0.0

        # Intro effects
        self.glitch_cd = 2.0
        self.glitch_dur = 0.0
        self.glyph_cache = {}
        self.trail = []
        self.last_mouse = (0, 0)

        self.rain = MatrixRain(self.rain_font)
        self.nodes = [Node() for _ in range(45)]
        self.bg_surf = self.build_background()
        self.play_bg = self.build_play_background()
        self.radar_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay = self.build_overlay()
        self.dim_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.dim_surf.fill((4, 8, 18, 175))
        self.ticker = self.font.render(
            " ///  ".join(f"BLOCKED {generate_ip()}" for _ in range(14)) + " ///  ",
            True, lerp_color(C_BG, C_HACKER, 0.6))

        self.setup_ui()
        self.update_language("EN")
        self.reset_game()
        self.set_state("menu")

    # ----------------------------------------------------------------------- #
    # Setup functions
    # ----------------------------------------------------------------------- #
    def build_background(self):
        """Builds the top-to-bottom dark blue -> purple gradient background image for menu screens
        (created once).
        """
        surf = pygame.Surface((WIDTH, HEIGHT))
        top, bottom = (6, 10, 24), (30, 8, 48)
        for y in range(HEIGHT):
            pygame.draw.line(surf, lerp_color(top, bottom, y / HEIGHT), (0, y), (WIDTH, y))
        return surf

    def build_play_background(self):
        """Builds a slightly different background for the game screen: dark-teal gradient, radar rings
        and crosshair lines (created once).
        """
        surf = pygame.Surface((WIDTH, HEIGHT))
        top, bottom = (5, 14, 28), (6, 34, 44)
        for y in range(HEIGHT):
            pygame.draw.line(surf, lerp_color(top, bottom, y / HEIGHT), (0, y), (WIDTH, y))
        cx, cy = WIDTH // 2, HEIGHT // 2
        ring = (14, 46, 64)
        for r in (110, 200, 300, 410, 530):
            pygame.draw.circle(surf, ring, (cx, cy), r, 1)
        pygame.draw.line(surf, ring, (cx, 0), (cx, HEIGHT))
        pygame.draw.line(surf, ring, (0, cy), (WIDTH, cy))
        return surf

    def draw_radar(self):
        """Draws a faint radar beam rotating around the server (with a fading trail behind it). Drawn on
        a separate transparent surface and then placed on the screen.
        """
        cx, cy, R = WIDTH // 2, HEIGHT // 2, 530
        a = self.time_passed * 0.7
        self.radar_surf.fill((0, 0, 0, 0))
        for i in range(14):
            a1, a2 = a - i * 0.045, a - (i + 1) * 0.045
            p1 = (cx + math.cos(a1) * R, cy + math.sin(a1) * R)
            p2 = (cx + math.cos(a2) * R, cy + math.sin(a2) * R)
            pygame.draw.polygon(self.radar_surf, (*C_CORE, int(34 * (1 - i / 14))), [(cx, cy), p1, p2])
        pygame.draw.line(self.radar_surf, (*C_CORE, 80), (cx, cy),
                         (cx + math.cos(a) * R, cy + math.sin(a) * R), 2)
        self.screen.blit(self.radar_surf, (0, 0))

    def draw_server(self, cx, cy):
        """Draws the main server: a 3-block rack, blinking LEDs and a shield rotating around it. Turns
        red when health is lost (core_flash). cx, cy - center.
        """
        t = self.time_passed
        flash = min(1.0, self.core_flash / 0.35)
        col = lerp_color(C_CORE, C_HACKER, flash)
        dim = lerp_color(C_BG, col, 0.35)

        pr = 44 + int(2 * math.sin(t * 3))
        pygame.draw.circle(self.screen, dim, (cx, cy), pr, 2)
        arc_rect = pygame.Rect(cx - pr - 6, cy - pr - 6, (pr + 6) * 2, (pr + 6) * 2)
        for k in range(3):
            a0 = t * 1.4 + k * 2.094
            pygame.draw.arc(self.screen, col, arc_rect, a0, a0 + 1.0, 3)

        body = pygame.Rect(cx - 22, cy - 28, 44, 56)
        pygame.draw.rect(self.screen, (12, 20, 34), body, border_radius=6)
        pygame.draw.rect(self.screen, col, body, 2, border_radius=6)
        for k in range(3):
            ur = pygame.Rect(cx - 17, cy - 23 + k * 17, 34, 13)
            pygame.draw.rect(self.screen, (22, 34, 54), ur, border_radius=3)
            pygame.draw.rect(self.screen, dim, ur, 1, border_radius=3)
            for j in range(2):
                on = math.sin(t * 6 + k * 2.3 + j * 1.7) > 0
                led = C_NORMAL if on else lerp_color(C_BG, C_NORMAL, 0.25)
                pygame.draw.circle(self.screen, led, (ur.x + 6 + j * 7, ur.centery), 2)
            pygame.draw.line(self.screen, dim, (ur.x + 22, ur.centery - 3), (ur.right - 4, ur.centery - 3))
            pygame.draw.line(self.screen, dim, (ur.x + 22, ur.centery + 3), (ur.right - 4, ur.centery + 3))

    def draw_heart(self, x, y, filled=True):
        """Draws a heart shape centered at (x, y). If filled=False it looks faded (a lost life)."""
        col = C_HACKER if filled else lerp_color(C_BG, C_HACKER, 0.22)
        pygame.draw.circle(self.screen, col, (x - 4, y - 3), 5)
        pygame.draw.circle(self.screen, col, (x + 4, y - 3), 5)
        pygame.draw.polygon(self.screen, col, [(x - 8, y - 1), (x + 8, y - 1), (x, y + 8)])

    def build_overlay(self):
        """Builds the CRT effect placed over the whole screen: darkened corners (vignette) and scan
        lines. Created once.
        """
        vig = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        steps = 70
        for i in range(steps):
            a = int(150 * (1 - i / steps) ** 2)
            pygame.draw.rect(vig, (0, 0, 0, a), (i, i, WIDTH - 2 * i, HEIGHT - 2 * i), 1)
        scan = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(scan, (0, 0, 0, 38), (0, y), (WIDTH, y))
        vig.blit(scan, (0, 0))
        return vig

    def setup_ui(self):
        """Creates all the buttons: main menu, settings, languages, pause menu, back and restart. The
        area of the in-game pause button is also defined here.
        """
        bx, bw, bh = WIDTH // 2 - 175, 350, 60
        self.btn_play = Button(bx, 280, bw, bh, "", self.btn_font, C_NORMAL)
        self.btn_settings = Button(bx, 360, bw, bh, "", self.btn_font, C_CORE)
        self.btn_lang = Button(bx, 440, bw, bh, "", self.btn_font, C_CORE)
        self.btn_exit = Button(bx, 520, bw, bh, "", self.btn_font, C_HACKER)

        self.menu_buttons = [self.btn_play, self.btn_settings, self.btn_lang, self.btn_exit]
        self.btn_back = Button(bx, 615, bw, bh, "", self.btn_font, C_HACKER)
        self.btn_restart = Button(bx, 500, bw, bh, "", self.btn_font, C_NORMAL)

        # Pause menu + in-game pause button
        self.btn_resume = Button(bx, 300, bw, bh, "", self.btn_font, C_NORMAL)
        self.btn_pause_restart = Button(bx, 380, bw, bh, "", self.btn_font, C_CORE)
        self.btn_pause_menu = Button(bx, 460, bw, bh, "", self.btn_font, C_HACKER)
        self.pause_buttons = [self.btn_resume, self.btn_pause_restart, self.btn_pause_menu]
        self.pause_rect = pygame.Rect(WIDTH - 70, 16, 50, 40)

        sx, sw, sh = WIDTH // 2 - 250, 500, 55
        self.btn_fx = Button(sx, 140, sw, sh, "", self.set_font, C_NORMAL)
        self.btn_diff = Button(sx, 205, sw, sh, "", self.set_font, C_CORE)
        self.btn_grid = Button(sx, 270, sw, sh, "", self.set_font, C_NORMAL)
        self.btn_tip = Button(sx, 335, sw, sh, "", self.set_font, C_NORMAL)
        self.btn_full = Button(sx, 400, sw, sh, "", self.set_font, C_NORMAL)
        self.btn_about = Button(sx, 490, sw, sh, "", self.set_font, C_CORE)
        self.set_buttons = [self.btn_fx, self.btn_diff, self.btn_grid,
                            self.btn_tip, self.btn_full, self.btn_about]

        lx, lw, lh = WIDTH // 2 - 150, 300, 50
        self.lang_btns = [
            Button(lx, 240, lw, lh, "ENGLISH", self.btn_font, C_CORE),
            Button(lx, 310, lw, lh, "AZƏRBAYCANCA", self.btn_font, C_CORE),
            Button(lx, 380, lw, lh, "TÜRKÇE", self.btn_font, C_CORE),
            Button(lx, 450, lw, lh, "РУССКИЙ", self.btn_font, C_CORE)
        ]
        self.lang_codes = ["EN", "AZ", "TR", "RU"]

    def buttons_for(self, state):
        """Returns the list of buttons that are on screen in the given state. update() and set_state()
        work based on this.
        """
        if state == "menu":
            return self.menu_buttons
        if state == "language":
            return self.lang_btns + [self.btn_back]
        if state == "settings":
            return self.set_buttons + [self.btn_back]
        if state == "about":
            return [self.btn_back]
        if state == "gameover":
            return [self.btn_restart]
        if state == "paused":
            return self.pause_buttons
        return []

    def set_state(self, new_state):
        """Changes the state (e.g. 'menu' -> 'play'). Starts the entry animation of the new screen's
        buttons; when returning to the menu, restarts the typing of the subtitle.
        """
        self.state = new_state
        if new_state == "menu":
            self.sub_start = self.time_passed
        for i, b in enumerate(self.buttons_for(new_state)):
            b.reset_anim(i * 0.07, -1 if i % 2 == 0 else 1)

    def update_language(self, new_lang):
        """Changes the language (EN/AZ/TR/RU) and updates all button labels."""
        self.lang_code = new_lang
        self.sub_start = self.time_passed
        self.refresh_texts()

    def refresh_texts(self):
        """Updates the label and color of all buttons according to the selected language and current
        settings (ON/OFF, difficulty name, etc.).
        """
        t = TEXTS[self.lang_code]
        s = self.settings
        self.btn_play.text = t["play"]
        self.btn_settings.text = t["set"]
        self.btn_lang.text = t["lang"]
        self.btn_exit.text = t["exit"]
        self.btn_back.text = t["back"]
        self.btn_restart.text = t["retry"]

        def onoff(v):
            """Converts a True/False value to the ON/OFF label in the selected language."""
            return t["on"] if v else t["off"]

        def color(v):
            """Returns green if the setting is on, red if it is off."""
            return C_NORMAL if v else C_HACKER

        self.btn_fx.text = t["l_fx"] + onoff(s["fx"])
        self.btn_fx.accent_color = color(s["fx"])

        self.btn_diff.text = t["l_diff"] + t["diff_names"][s["diff"]]
        self.btn_diff.accent_color = [C_NORMAL, C_CORE, C_HACKER][s["diff"]]

        self.btn_grid.text = t["l_grid"] + onoff(s["grid"])
        self.btn_grid.accent_color = color(s["grid"])

        self.btn_tip.text = t["l_tip"] + onoff(s["tip"])
        self.btn_tip.accent_color = color(s["tip"])

        self.btn_full.text = t["l_full"] + onoff(s["full"])
        self.btn_full.accent_color = color(s["full"])

        self.btn_about.text = t["about_btn"]
        self.btn_resume.text = t["resume"]
        self.btn_pause_restart.text = t["retry"]
        self.btn_pause_menu.text = t["back"]

    # ----------------------------------------------------------------------- #
    # Game logic
    # ----------------------------------------------------------------------- #
    def reset_game(self):
        """Resets everything for a new game: health by difficulty, score, packets, particles, banned
        IPs. spawn_timer=99 makes sure the first packet spawns immediately.
        """
        hp = DIFFICULTIES[self.settings["diff"]]["hp"]
        self.stats = {"health": hp, "max_health": hp, "score": 0}
        self.packets = []
        self.particles = []
        self.banned_ips = set()
        self.spawn_timer = 99  # the first packet spawns immediately
        self.time_survived = 0.0
        self.core_flash = 0.0

    def spawn_packet(self):
        """Creates a new packet matching the current difficulty (hacker chance, speed) and adds it to
        the list.
        """
        d = DIFFICULTIES[self.settings["diff"]]
        self.packets.append(Packet(WIDTH // 2, HEIGHT // 2, d["hack"], d["spd"]))

    def create_explosion(self, x, y, color):
        """Creates an explosion of 30 colored particles at point (x, y). Does nothing if the 'Visual
        effects' setting is off.
        """
        if self.settings["fx"]:
            for _ in range(30):
                self.particles.append(Particle(x, y, color))

    def handle_settings_click(self, event):
        """Handles clicks on the buttons of the settings screen: effects, difficulty (Easy -> Normal ->
        Hard), background animation, packet info, fullscreen and the About page. Then updates the
        labels.
        """
        s = self.settings
        if self.btn_fx.is_clicked(event):
            s["fx"] = not s["fx"]
        elif self.btn_diff.is_clicked(event):
            s["diff"] = (s["diff"] + 1) % 3
        elif self.btn_grid.is_clicked(event):
            s["grid"] = not s["grid"]
        elif self.btn_tip.is_clicked(event):
            s["tip"] = not s["tip"]
        elif self.btn_full.is_clicked(event):
            s["full"] = not s["full"]
            pygame.display.toggle_fullscreen()
        elif self.btn_about.is_clicked(event):
            self.set_state("about")
            return
        else:
            return
        self.refresh_texts()

    def handle_events(self):
        """Handles all events (closing the window, keyboard, mouse) according to the current state.
        During the game: click on a packet (hacker -> +15 points and the IP is banned; user packet ->
        -1 health), pause with ESC/P or the pause button, automatic pause when the window loses focus.
        In the pause menu: resume / restart / go back to the main menu.
        """
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.WINDOWFOCUSLOST and self.state == "play":
                self.pause_game()      # the game pauses automatically when switching to another window

            if self.state == "menu":
                for btn in self.menu_buttons:
                    if btn.is_clicked(event):
                        if btn == self.btn_play:
                            self.reset_game()
                            self.set_state("play")
                        elif btn == self.btn_settings:
                            self.set_state("settings")
                        elif btn == self.btn_lang:
                            self.set_state("language")
                        elif btn == self.btn_exit:
                            pygame.quit()
                            sys.exit()

            elif self.state == "language":
                if self.btn_back.is_clicked(event):
                    self.set_state("menu")
                else:
                    for i, btn in enumerate(self.lang_btns):
                        if btn.is_clicked(event):
                            self.update_language(self.lang_codes[i])
                            self.set_state("menu")
                            break

            elif self.state == "settings":
                if self.btn_back.is_clicked(event):
                    self.set_state("menu")
                else:
                    self.handle_settings_click(event)

            elif self.state == "about":
                if self.btn_back.is_clicked(event):
                    self.set_state("settings")

            elif self.state == "play":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.pause_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.pause_rect.collidepoint(mouse_pos):
                        self.pause_game()
                        continue
                    clicked_packet = None
                    for p in reversed(self.packets):
                        if calc_dist(mouse_pos[0], mouse_pos[1], p.x, p.y) < p.radius * 2.5:
                            clicked_packet = p
                            break

                    if clicked_packet:
                        self.packets.remove(clicked_packet)
                        if clicked_packet.is_hacker:
                            self.stats["score"] += 15
                            self.banned_ips.add(clicked_packet.ip)
                            self.create_explosion(clicked_packet.x, clicked_packet.y, C_HACKER)
                        else:
                            self.stats["health"] -= 1
                            self.core_flash = 0.35
                            self.create_explosion(clicked_packet.x, clicked_packet.y, C_HOVER)

            elif self.state == "paused":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.set_state("play")
                elif self.btn_resume.is_clicked(event):
                    self.set_state("play")
                elif self.btn_pause_restart.is_clicked(event):
                    self.reset_game()
                    self.set_state("play")
                elif self.btn_pause_menu.is_clicked(event):
                    self.set_state("menu")

            elif self.state == "gameover":
                if self.btn_restart.is_clicked(event):
                    self.set_state("menu")

    def update_fx(self, dt, mouse_pos):
        """Updates the animations on the menu and pause screens: title glitch timer, code rain, nodes
        and mouse trail.
        """
        # Glitch timer
        if self.glitch_dur > 0:
            self.glitch_dur -= dt
        else:
            self.glitch_cd -= dt
            if self.glitch_cd <= 0:
                self.glitch_dur = 0.18
                self.glitch_cd = random.uniform(1.5, 4.0)

        if self.settings["grid"]:
            self.rain.update(dt)
            for n in self.nodes:
                n.update(dt)

        # Mouse trail
        if self.settings["fx"]:
            if mouse_pos != self.last_mouse:
                self.trail.append([mouse_pos[0], mouse_pos[1], 1.0])
                self.last_mouse = mouse_pos
            for tr in self.trail:
                tr[2] -= dt * 2.5
            self.trail = [tr for tr in self.trail if tr[2] > 0]
        else:
            self.trail = []

    def update(self, dt):
        """Called every frame (dt - seconds since the last frame). Updates the buttons; if not in the
        game state, it only updates the effects and returns (which is why everything freezes while
        paused).
        In the game: spawns packets (faster over time), moves the packets, checks for those that reach
        the server (hacker -> health is lost, user -> +5 points), updates the particles.
        LAMBDA: filter(lambda p: p.life > 0, ...) removes dead particles; sort(key=lambda p: p.load)
        makes packets with high LOAD (hackers) be drawn on top.
        When health reaches 0, it switches to the 'gameover' state.
        """
        self.time_passed += dt
        mouse_pos = pygame.mouse.get_pos()

        for b in self.buttons_for(self.state):
            b.update(dt, mouse_pos)

        if self.state != "play":
            self.update_fx(dt, mouse_pos)
            return

        self.time_survived += dt
        self.core_flash = max(0.0, self.core_flash - dt)
        self.spawn_timer += dt

        spawn_rate = max(0.55, 1.6 - (self.time_survived / 35))
        if self.spawn_timer > spawn_rate:
            self.spawn_packet()
            self.spawn_timer = 0

        for p in self.packets[:]:
            p.hovered = calc_dist(mouse_pos[0], mouse_pos[1], p.x, p.y) < p.radius * 2.5
            p.update(dt)

            if calc_dist(p.x, p.y, WIDTH // 2, HEIGHT // 2) < 40:
                self.packets.remove(p)
                if p.is_hacker:
                    self.stats["health"] -= 1
                    self.core_flash = 0.35
                    self.create_explosion(p.x, p.y, C_HACKER)
                else:
                    self.stats["score"] += 5
                    self.create_explosion(p.x, p.y, C_NORMAL)

        for p in self.particles:
            p.update(dt)

        # ====== LAMBDA AND FILTER ADDITION (Topic 6) ======
        self.particles = list(filter(lambda p: p.life > 0, self.particles))
        self.packets.sort(key=lambda p: p.load)
        # ==================================================

        if self.stats["health"] <= 0:
            self.set_state("gameover")

    # ----------------------------------------------------------------------- #
    # Drawing (draw) functions
    # ----------------------------------------------------------------------- #
    def accent(self, shift=0.0):
        """Returns a neon color that flows over time between cyan -> purple -> magenta. shift - shifts
        the color phase so that different elements have different colors.
        """
        return hsv(0.72 + 0.2 * math.sin(self.time_passed * 0.7 + shift), 0.85, 1.0)

    def draw_cyber_grid(self):
        """Draws a faint grid of lines slowly flowing downward on the menu background."""
        offset = (self.time_passed * 20) % 50
        col = lerp_color(C_BG, self.accent(), 0.14)
        for x in range(0, WIDTH, 50):
            pygame.draw.line(self.screen, col, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(self.screen, col, (0, y + offset - 50), (WIDTH, y + offset - 50))

    def draw_nodes(self):
        """Draws the nodes; connects those closer than 150 pixels to each other with lines that fade
        with distance.
        """
        acc = self.accent(1.0)
        maxd = 150
        maxd2 = maxd * maxd
        n = len(self.nodes)
        for i in range(n):
            a = self.nodes[i]
            for j in range(i + 1, n):
                b = self.nodes[j]
                dx, dy = a.x - b.x, a.y - b.y
                d2 = dx * dx + dy * dy
                if d2 < maxd2:
                    k = 1 - math.sqrt(d2) / maxd
                    pygame.draw.line(self.screen, lerp_color((12, 16, 34), acc, k * 0.55),
                                     (int(a.x), int(a.y)), (int(b.x), int(b.y)))
        for nd in self.nodes:
            pygame.draw.circle(self.screen, lerp_color(C_BG, acc, 0.8), (int(nd.x), int(nd.y)), 3)

    def draw_background(self):
        """Draws the background of the menu screens: gradient + (if the setting is on) grid, nodes and
        code rain.
        """
        self.screen.blit(self.bg_surf, (0, 0))
        if self.settings["grid"]:
            self.draw_cyber_grid()
            self.draw_nodes()
            self.rain.draw(self.screen)

    def get_glyph(self, font, ch, color):
        """Returns the rendered image of a letter in the given color. When the same letter is needed
        again it is not recreated but kept in memory (glyph_cache).
        """
        key = (id(font), ch, color)
        g = self.glyph_cache.get(key)
        if g is None:
            g = font.render(ch, True, color)
            self.glyph_cache[key] = g
        return g

    def draw_wave_title(self, text, y, font, hue_center=0.72, hue_amp=0.2, sat=0.75):
        """Draws a waving title with flowing colors: each letter moves up and down separately, red/cyan
        shadows are added, and an occasional 'glitch' (jitter) happens.
        text - the text, y - vertical position, font - font, hue_center/hue_amp - hue range, sat -
        saturation.
        """
        t = self.time_passed
        glitch = self.glitch_dur > 0
        widths = [font.size(ch)[0] for ch in text]
        x = WIDTH // 2 - sum(widths) // 2
        sh = random.randint(6, 12) if glitch else 3
        for i, ch in enumerate(text):
            if ch != " ":
                wy = math.sin(t * 3 + i * 0.5) * 6
                jx = random.randint(-6, 6) if glitch and random.random() < 0.3 else 0
                px, py = x + jx, y + wy
                self.screen.blit(self.get_glyph(font, ch, (255, 40, 75)), (px - sh, py + sh))
                self.screen.blit(self.get_glyph(font, ch, (0, 200, 255)), (px + sh, py - sh))
                hue = hue_center + hue_amp * math.sin(t * 0.8 + i * 0.3)
                self.screen.blit(font.render(ch, True, hsv(hue, sat, 1.0)), (px, py))
            x += widths[i]

    def draw_text_center(self, text, y, color=C_TEXT, font=None):
        """Draws text horizontally centered on the screen at height y. If color and font are not given,
        the defaults (C_TEXT, self.font) are used.
        """
        f = font if font else self.font
        surf = f.render(text, True, color)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def draw_subtitle(self, y):
        """Draws the subtitle under the title with a typewriter effect (letter by letter); a blinking
        cursor remains at the end.
        """
        full = TEXTS[self.lang_code]["sub"]
        n = int((self.time_passed - self.sub_start) * 25)
        typed = full[:n]
        typing = n < len(full)
        if typing or int(self.time_passed * 2) % 2 == 0:
            typed += "_"
        x = WIDTH // 2 - self.set_font.size(full)[0] // 2
        self.screen.blit(self.set_font.render(typed, True, self.accent(2.0)), (x, y))

    def draw_divider(self, y):
        """Draws a colored line under the title with diamond ends, whose width changes like a pulse."""
        t = self.time_passed
        w = 300 + 60 * math.sin(t * 2)
        acc = self.accent(0.5)
        cx = WIDTH // 2
        pygame.draw.line(self.screen, acc, (cx - w, y), (cx + w, y), 2)
        for sx in (-1, 1):
            ex = cx + sx * w
            pygame.draw.polygon(self.screen, acc, [(ex, y - 6), (ex + sx * 8, y), (ex, y + 6), (ex - sx * 8, y)])

    def draw_emblem(self, cx, cy, r, direction=1):
        """The rotating 'core' emblem on the sides of the menu: a pulsing dot in the center, rotating
        arcs and green/red packets orbiting around it. cx, cy - center, r - radius, direction -
        rotation direction (+1/-1).
        """
        tt = self.time_passed
        t = tt * direction
        col = hsv(0.52 + 0.12 * math.sin(tt * 0.8), 0.85, 1.0)
        dim = lerp_color(C_BG, col, 0.35)
        pulse = 1 + 0.08 * math.sin(tt * 3)
        pygame.draw.circle(self.screen, col, (cx, cy), int(r * 0.2 * pulse))
        pygame.draw.circle(self.screen, dim, (cx, cy), int(r * 0.34), 2)
        pygame.draw.circle(self.screen, dim, (cx, cy), r, 1)
        base = pygame.Rect(cx - r, cy - r, r * 2, r * 2)
        for k in range(3):
            rect = base.inflate(-k * 44, -k * 44)
            a0 = t * (1.0 + 0.45 * k) + k * 2.1
            pygame.draw.arc(self.screen, col, rect, a0, a0 + 1.7, 4)
        for k in range(5):
            a = t * (0.9 + 0.17 * k) + k * 1.26
            rr = r * (0.5 + 0.1 * k)
            px, py = int(cx + math.cos(a) * rr), int(cy + math.sin(a) * rr)
            c = C_HACKER if k % 2 else C_NORMAL
            pygame.draw.circle(self.screen, c, (px, py), 7)
            pygame.draw.circle(self.screen, C_BG, (px, py), 4)
            pygame.draw.circle(self.screen, c, (px, py), 2)

    def draw_hud_frame(self):
        """On the menu screens, draws the 'SYSTEM ONLINE' status (blinking dot) and the uptime at the
        top, and a right-to-left scrolling 'BLOCKED IP' line at the bottom.
        """
        t = TEXTS[self.lang_code]
        tt = self.time_passed
        # Status
        dot_col = C_NORMAL if int(tt * 1.5) % 2 == 0 else lerp_color(C_BG, C_NORMAL, 0.35)
        pygame.draw.circle(self.screen, dot_col, (28, 26), 6)
        self.screen.blit(self.font.render(t["online"], True, C_NORMAL), (44, 16))
        up = f"{t['uptime']} {int(tt) // 60:02d}:{int(tt) % 60:02d}"
        us = self.font.render(up, True, lerp_color(C_BG, C_CORE, 0.8))
        self.screen.blit(us, (WIDTH - us.get_width() - 24, 16))
        # Scrolling line
        pygame.draw.line(self.screen, lerp_color(C_BG, C_HACKER, 0.35), (0, HEIGHT - 36), (WIDTH, HEIGHT - 36))
        w = self.ticker.get_width()
        x = -int((tt * 70) % w)
        while x < WIDTH:
            self.screen.blit(self.ticker, (x, HEIGHT - 28))
            x += w

    def draw_trail(self):
        """Draws the fading colored trail points behind the mouse."""
        acc = self.accent(3.0)
        for x, y, life in self.trail:
            pygame.draw.circle(self.screen, lerp_color(C_BG, acc, life), (int(x), int(y)), int(2 + 5 * life))

    def pause_game(self):
        """Pauses the game: clears the hover state of the packets and switches to the 'paused' state.
        Packets, time and spawning freeze at this point because update() stops when the state is not
        'play'.
        """
        for p in self.packets:
            p.hovered = False
        self.set_state("paused")

    def draw_pause_button(self):
        """Draws the small pause button in the top right during the game; turns white when the mouse is
        over it.
        """
        r = self.pause_rect
        col = C_HOVER if r.collidepoint(pygame.mouse.get_pos()) else C_CORE
        pygame.draw.rect(self.screen, (12, 20, 34), r, border_radius=8)
        pygame.draw.rect(self.screen, col, r, 2, border_radius=8)
        for dx in (-6, 6):
            pygame.draw.rect(self.screen, col, (r.centerx + dx - 3, r.centery - 9, 6, 18), border_radius=2)

    def draw_pause_menu(self, t):
        """Draws the pause menu: a dark veil over the game scene, the 'SYSTEM PAUSED' title, a short
        hint and 3 buttons.
        """
        self.screen.blit(self.dim_surf, (0, 0))
        self.draw_wave_title(t["paused"], 150, self.title_font)
        self.draw_text_center(t["pause_hint"], 235, C_TEXT, self.set_font)
        for btn in self.pause_buttons:
            btn.draw(self.screen)

    def draw(self):
        """Draws the whole screen every frame. First the background according to the state, then the
        elements of that state (menu, settings, about, language, game, pause, gameover), and finally
        the CRT effect (overlay) and the screen refresh.
        During the game: the server, packets, score, health hearts and pause button are drawn.
        """
        t = TEXTS[self.lang_code]

        if self.state in ("play", "paused"):
            self.screen.blit(self.play_bg, (0, 0))
            if self.settings["grid"]:
                self.draw_radar()
        else:
            self.draw_background()

        if self.state == "menu":
            self.draw_emblem(210, 430, 115, 1)
            self.draw_emblem(WIDTH - 210, 430, 115, -1)
            self.draw_wave_title("NETWORK DEFENDER", 80, self.title_font)
            self.draw_subtitle(178)
            self.draw_divider(235)
            for btn in self.menu_buttons:
                btn.draw(self.screen)

        elif self.state == "settings":
            self.draw_wave_title(t["set"], 50, self.mid_font)
            for btn in self.set_buttons + [self.btn_back]:
                btn.draw(self.screen)

        elif self.state == "about":
            self.draw_wave_title(t["about_title"], 50, self.title_font)
            self.draw_text_center(t["about_g"], 150, C_TEXT, self.btn_font)

            self.draw_text_center(t["about_t"], 220, C_HOVER, self.btn_font)
            self.draw_text_center(t["about_1"], 265, C_TEXT)
            self.draw_text_center(t["about_2"], 295, C_HACKER)
            self.draw_text_center(t["about_3"], 325, C_NORMAL)

            self.draw_text_center(t["about_dev_t"], 395, C_HOVER, self.btn_font)
            self.draw_text_center(t["dev"], 440, self.accent(1.5), self.btn_font)
            self.draw_text_center(t["ver"], 485, C_TEXT)
            self.draw_text_center(t["built"], 515, C_TEXT)

            self.btn_back.draw(self.screen)

        elif self.state == "language":
            self.draw_wave_title(t["lang_title"], 100, self.title_font)
            for btn in self.lang_btns + [self.btn_back]:
                btn.draw(self.screen)

        elif self.state in ("play", "paused"):
            for p in self.particles:
                p.draw(self.screen)

            self.draw_server(WIDTH // 2, HEIGHT // 2)

            for p in self.packets:
                p.draw(self.screen, self.font, self.settings["tip"])

            score_txt = self.font.render(f"{t['score']}{self.stats['score']}", True, C_TEXT)
            health_txt = self.font.render(t["hp"], True, C_HACKER)
            self.screen.blit(score_txt, (20, 20))
            self.screen.blit(health_txt, (20, 50))

            hx = 20 + health_txt.get_width() + 15
            for i in range(self.stats["max_health"]):
                self.draw_heart(hx + 8 + i * 24, 58, i < self.stats["health"])

            if self.state == "play":
                self.draw_pause_button()
            else:
                self.draw_pause_menu(t)

        elif self.state == "gameover":
            self.draw_wave_title(t["fail"], 150, self.title_font, hue_center=0.0, hue_amp=0.03, sat=0.85)
            self.draw_text_center(f"{t['score']}{self.stats['score']}  |  {t['banned']}{len(self.banned_ips)}",
                                  280, C_TEXT, self.btn_font)
            self.btn_restart.draw(self.screen)

        if self.state not in ("play", "paused"):
            self.draw_trail()
            self.draw_hud_frame()

        self.screen.blit(self.overlay, (0, 0))
        pygame.display.flip()

    def run(self):
        """Main game loop: every frame dt is calculated (FPS=60 target), then events -> update ->
        draw.
        """
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    app = GameApp()
    app.run()
