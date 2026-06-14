# Constants are written in CapsLock
import pygame
import time

FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
TILE_SIZE = 64
timer = time.time()

coin = 0  # Create coin counter
coins_level = 0  # Coins in a level

Level_path = ""  # Level path

levels_R = {  # Official levels in the game
    "1": "levels/level 1.txt",
    "2": "levels/level 2.txt",
    "3": "levels/level 3.txt",
    "4": "levels/level 4.txt",
    "5": "levels/level 5.txt",
    "6": "levels/level 6.txt",
    "7": "levels/level 7.txt",
    "8": "levels/level 8.txt",
    "9": "levels/level 9.txt",
    "10": "levels/level 10.txt"
}


def load_level(LEVEL_PATH):
    global TILE_SIZE, Level_path, levels_R, coins_level, player_cords
    with open(LEVEL_PATH, "r", encoding='utf-8') as l1:  # Open level file
        level = l1.readlines()  # Load the current level configuration
    for i in levels_R:
        if levels_R[i] == LEVEL_PATH:  # Identify the active level from the official level list
            Level_path = i
            break

    objects = {  # Dictionary of game objects and entities with their coords
        "walls": [],
        "enemies": [],
        "turrets": [],
        "boss": [],
        "platforms": [],
        "j_platforms": [],
        "m_platforms": [],
        "m_j_platforms": [],
        "liquid": [],
        "spikes": [],
        "closed_door": [],
        "money": [],
        "chest": [],
        "FAK": [],
        "buttons": [],
        "portals": [],
        "start": [],
        "end": [],
        "npc": [],
        "air": [],
        "checkpoint": [],
        "coins": []
    }

    for i, f in enumerate(level):  # Parse the text map and populate game objects with coordinates
        for j, k in enumerate(f):
            if k == "#":
                objects["walls"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "e":
                objects["enemies"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "t":
                objects["turrets"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "b":
                objects["boss"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == ".":
                objects["air"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "p":
                objects["platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "P":
                objects["m_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "=":
                objects["j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "_":
                objects["m_j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "~":
                objects["liquid"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "^":
                objects["spikes"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE + 32))
            elif k == "n":
                objects["npc"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "-":
                objects["closed_door"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "*":
                objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "?":
                objects["chest"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "h":
                objects["FAK"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "!":  # TODO: Implement button functionality
                objects["buttons"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == ">":
                objects["start"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "<":
                objects["end"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "0":
                objects["portals"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "s":
                objects["checkpoint"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "$":
                objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "@":
                player_cords = [(j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE]
    coins_level = len(objects["money"])
    return player_cords, objects


def reset_level(level_number):
    global player, level_data, camera, gameplay, pause, death, is_jump, is_go, complete, coin, death_flag, player_cords
    path = levels_R.get(str(level_number))  # Load level data
    if path:
        player_cords, level_data = load_level(path)

        # Create camera and player:
        if player_cords:
            player = Player(player_cords[0], player_cords[1])
            camera = Camera()
    # Reset other gameplay state variables:
    gameplay = True
    pause = False
    death = False
    is_jump = False
    is_go = False
    complete = False
    coin = 0
    player.jump_buffer = 0
    death_flag = 0


class Player:
    def __init__(self, x, y):
        # Initialize player attributes and physics parameters
        self.x = x
        self.y = y
        self.width = 32  # hitbox width
        self.height = 56  # hitbox height
        self.speed = 5
        self.direction = "right"  # Current player movement direction
        self.animation_index = 0
        self.animation_timer = 0
        self.HITBOX_OFFSET_X = 7
        self.SPRITE_OFFSET_Y = 5

        self.vy = 0  # Vertical velocity (0 means standing still)
        self.gravity = 1  # Gravity force applied per frame
        self.jump_power = -22  # Initial jump velocity (negative for moving up)
        # Coyote time configuration (allows jumping slightly after leaving a ledge)
        self.coyote_time = 0  # Current coyote time frame counter
        self.coyote_max = 10  # Maximum frames available for a delayed jump
        # Jump buffer configuration (remembers jump input right before landing)
        self.jump_buffer = 0  # Jump buffer frame counter
        self.jump_buffer_max = 10  # Maximum frames to remember early jump input

    def jump(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump_buffer = self.jump_buffer_max  # Trigger jump buffer on input
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.vy < 0:  # if the player is moving upward
                    self.vy *= 0.5  # Reduce vertical velocity

    # Get player's hitbox:
    def get_rect(self):
        return pygame.Rect(self.x - self.HITBOX_OFFSET_X, self.y, self.width, self.height)
        # We subtract "self.HITBOX_OFFSET_X" because of the unknown mistake
        # TODO: correct the upper mistake

    def move(self, keys, level_data):
        global gameplay, death, is_jump, is_go, coin, complete
        old_x = self.x  # Store current X coordinate for collision resolution
        if keys[pygame.K_a]:
            is_go = True
            self.x -= self.speed
            self.direction = "left"

        if keys[pygame.K_d]:
            is_go = True

            self.x += self.speed
            self.direction = "right"

        if keys[pygame.K_a] or keys[pygame.K_d]:
            # Update animation timer and cycle through running frames (0 to 3)
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_index = (
                                               self.animation_index + 1) % 4
                self.animation_timer = 0

        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            is_go = False

        if is_jump:
            is_go = True
            if self.direction == "right":
                self.animation_index = 0
            else:
                self.animation_index = 3
        # Reset to idle animation frame
        if not is_go:
            if self.direction == "right":
                self.animation_index = 1
            else:
                self.animation_index = 2

        player_rect = self.get_rect()
        wall_collision = False
        # Check for collisions with objects
        # Check for horizontal collisions with walls
        for wallx, wally in level_data['walls']:

            wall_rect = pygame.Rect(wallx, wally, TILE_SIZE, TILE_SIZE)  # Create wall hitbox
            if player_rect.colliderect(wall_rect):
                wall_collision = True
                break
        # Check for vertical collisions with platforms
        # TODO: add more types of platforms (passable platforms and their moving versions)
        for plat_x, plat_y in level_data["platforms"] + level_data["m_platforms"] + level_data["j_platforms"] + \
                              level_data["m_j_platforms"]:
            # Create left and right parts of a platform hitbox
            plat_rect_left = pygame.Rect(plat_x - 1, plat_y, 1, TILE_SIZE)
            plat_rect_right = pygame.Rect(plat_x + TILE_SIZE + 1, plat_y, 1, TILE_SIZE)
            if player_rect.colliderect(plat_rect_left) and self.direction == "right":
                self.x = old_x
                break
            elif player_rect.colliderect(plat_rect_right) and self.direction == "left":
                self.x = old_x
                break
        # Check for collisions with spikes
        for s_x, s_y in level_data["spikes"]:
            # Create spike hitbox
            spike_rect = pygame.Rect((s_x, s_y, TILE_SIZE, TILE_SIZE // 2))  # Spikes are smaller

            if player_rect.colliderect(spike_rect):
                death = True
                break

        # Check for collisions with coins
        for c_x, c_y in level_data["money"]:
            coin_rect = pygame.rect.Rect((c_x, c_y, TILE_SIZE // 2, TILE_SIZE // 2))
            if player_rect.colliderect(coin_rect):
                for coin_pos in level_data["money"][:]:  # Use list copy [:] for safe deletion
                    coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], TILE_SIZE, TILE_SIZE)
                    if player_rect.colliderect(coin_rect):
                        level_data["money"].remove(coin_pos)
                        coin += 1
        # Check for collisions with exit level triggers
        for e_x, e_y in level_data["end"]:
            end_rect = pygame.rect.Rect((e_x, e_y, TILE_SIZE, TILE_SIZE))
            if player_rect.colliderect(end_rect):
                complete = True

        if self.y > 2000:  # Prevent the player from falling into the void
            death = True

        if wall_collision:
            self.x = old_x

        old_y = self.y
        self.vy += self.gravity  # Increase speed of fall (the longer the player falls, the faster he falls)
        self.y += self.vy  # Start falling

        self.check_vertical_collision(old_y, level_data)
        on_ground = self.ground_check(level_data)
        if on_ground:
            is_jump = False
            self.coyote_time = self.coyote_max
        else:
            self.coyote_time = max(0, self.coyote_time - 1)  # Decrement coyote time counter
            is_jump = True
            # Tick down jump buffer frame counter
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        # Trigger jump if player is on ground or left ledge recently
        if self.jump_buffer > 0 and (on_ground or self.coyote_time > 0):
            self.vy = self.jump_power
            self.coyote_time = 0
            self.jump_buffer = 0

    def ground_check(self, level_data):
        player_rect = self.get_rect()
        # Create ground detector rectangle
        ground_check_rect = pygame.Rect(player_rect.x,
                                        player_rect.y + player_rect.height,
                                        player_rect.width,
                                        2)

        for plat_x, plat_y in level_data["platforms"] + level_data["j_platforms"] + level_data["m_platforms"] + \
                              level_data["m_j_platforms"]:
            plat_hb = pygame.Rect(plat_x, plat_y, TILE_SIZE, TILE_SIZE)  # Create platform hitbox
            if ground_check_rect.colliderect(plat_hb):
                return True
        return False

    def check_vertical_collision(self, old_y, level_data):
        player_rect = self.get_rect()
        obstacles = (level_data.get("walls", []) +
                     level_data.get("platforms", []) +
                     level_data.get("m_platforms", []))
        for x, y in obstacles:
            block_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)  # Create obstacle hitbox
            if player_rect.colliderect(block_rect):
                self.y = old_y
                self.vy = 0  # Stop falling (encountered an obstacle)
                break

    def draw(self, surface, camera_x, camera_y):  # Draw player function
        screen_x = self.x - camera_x - self.width // 2  # Calculate screen player X coordinate
        screen_y = self.y - camera_y - self.SPRITE_OFFSET_Y  # Calculate screen player Y coordinate

        if self.direction == "right":
            current_frame = player_right[self.animation_index % len(player_right)]
        else:
            current_frame = player_left[self.animation_index % len(player_left)]
        surface.blit(current_frame, (screen_x, screen_y))

        if Debug:
            rect = self.get_rect()
            # Red player hitbox
            debug_rect = pygame.Rect(rect.x - camera_x,
                                     rect.y - camera_y,
                                     rect.width, rect.height)
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 3)

            # Player hitbox center dot
            center_x = self.x - camera_x + self.width // 4  # Offset by a quarter of the width to center the do
            center_y = self.y - camera_y + self.height // 2
            pygame.draw.circle(surface, (0, 255, 0), (center_x, center_y), 5)
            pygame.draw.circle(surface, (0, 0, 255), (center_x, center_y), 3)

            # Print coordinates
            font = pygame.font.Font(None, 24)
            debug_text = font.render(f"X:{self.x:.0f} Y:{self.y:.0f}", True, (255, 255, 255))
            surface.blit(debug_text, (10, 10))


class Camera:
    def __init__(self):
        # Initialize camera viewport matching screen dimensions
        self.x = 0  # Camera coordinate X in the game world
        self.y = 0  # Camera coordinate Y in the game world
        # Camera review (640x360)
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

    def update(self, player):  # Calculate camera coordinates in the game world
        self.x = player.x - SCREEN_WIDTH // 2
        self.y = player.y - SCREEN_HEIGHT // 2

    def apply(self, x, y):  # Convert world coordinates into screen ones
        return x - self.x, y - self.y


def draw_level(surface, level_data, camera):
    # TODO: add more objects
    for x, y in level_data["walls"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(wall, (screen_x, screen_y))
    for x, y in level_data["platforms"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(every_platform, (screen_x, screen_y))
    for x, y in level_data["money"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(money, (screen_x, screen_y))
    for x, y in level_data["buttons"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(button, (screen_x, screen_y))
    for x, y in level_data["spikes"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(spikes, (screen_x, screen_y))
    if Debug:
        # Show objects' hitboxes
        for x, y in level_data["walls"]:
            screen_x, screen_y = camera.apply(x, y)
            wall_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, (255, 0, 0), wall_hb, 2)
        for x, y in level_data["platforms"]:
            screen_x, screen_y = camera.apply(x, y)
            plat_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, (0, 0, 255), plat_hb, 2)
        for x, y in level_data["spikes"]:
            screen_x, screen_y = camera.apply(x, y)
            spike_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE // 2)
            pygame.draw.rect(surface, (255, 0, 0), spike_hb, 2)
        for x, y in level_data["money"]:
            screen_x, screen_y = camera.apply(x, y)
            coin_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE // 2, TILE_SIZE // 2)
            pygame.draw.rect(surface, (255, 0, 0), coin_hb, 2)


def change_lan():
    global start_button, levels_label, confirm_exit_label, yes, no, settings_label
    global pause_label, exit_pause, F1_mode, debug_label, lose_label, win, lan_en, en, CC
    global us_uk_flag, ru_flag, white

    # Language settings
    # UI Text dictionary
    texts = {
        "en": {
            "play": "Play",
            "pause": "Pause",
            "win": "You won!",
            "lose": "You lose!",
            "settings": "Settings",
            "levels": "Levels",
            "exit_confirm": "Are you sure you want to exit?",
            "yes": "Yes",
            "no": "No",
            "exit": "Exit",
            "fullscreen": "Fullscreen mode",
            "debug": "Debug",
            "menu": "Menu",
            "coins": "Coins collected",
            "language": "Language",
        },
        "ru": {
            "play": "Играть",
            "pause": "Пауза",
            "win": "Вы выиграли!",
            "lose": "Вы проиграли!",
            "settings": "Настройки",
            "levels": "Уровни",
            "exit_confirm": "Вы точно хотите выйти?",
            "yes": "Да",
            "no": "Нет",
            "exit": "Выйти",
            "fullscreen": "Полноэкранный режим",
            "debug": "Отладка",
            "menu": "В меню",
            "coins": "Собрано монет",
            "language": "Язык"
        }
    }
    if not en:
        current_flag = ru_flag
        LANGUAGE = "ru"
        CC = texts["ru"]["coins"]
    else:
        current_flag = us_uk_flag
        LANGUAGE = "en"
        CC = texts["en"]["coins"]
    # Update all UI text elements based on current language

    start_button = font.render(texts[LANGUAGE]["play"], True, "black")
    levels_label = font1.render(texts[LANGUAGE]["levels"], True, "white")
    confirm_exit_label = font.render(texts[LANGUAGE]["exit_confirm"], True, "black")
    yes = font.render(texts[LANGUAGE]["yes"], True, "black")
    no = font.render(texts[LANGUAGE]["no"], True, "black")
    settings_label = font.render(texts[LANGUAGE]["settings"], True, "black")
    pause_label = font.render(texts[LANGUAGE]["pause"], True, (255, 255, 255))
    exit_pause = font.render(texts[LANGUAGE]["exit"], True, "black")
    F1_mode = font_set.render(texts[LANGUAGE]["fullscreen"], True, "black")
    debug_label = font_set.render(texts[LANGUAGE]["debug"], True, "black")
    lose_label = font.render(texts[LANGUAGE]["lose"], True, "black")
    win = font.render(texts[LANGUAGE]["win"], True, "black")

    # Language button text
    lan_en = font_set.render(texts[LANGUAGE]["language"], True, "black")
    return current_flag


def draw_settings_menu():
    global white, white_hb
    white.fill((255, 255, 255))  # Surface
    white.blit(exit_button, (290, 5))
    white.blit(settings_label, (120, 10))
    white.blit(g_F1, (45, 70))
    white.blit(g_debug, (45, 83))
    white.blit(F1_mode, (65, 66))
    white.blit(debug_label, (65, 80))
    selected_flag = change_lan()
    white.blit(selected_flag, (45, 40))
    white.blit(lan_en, (80, 45))
    if is_F1:
        white.blit(check, (45, 70))
    if Debug:
        white.blit(check, (45, 83))


# Gameplay
# State variables
menu = True  # Main menu flag
pause = False
exit_game_flag = False  # Exit game button pressed flag
gameplay = False
is_open_setting = False
is_open_level_select_menu = False
available_jump = True
is_go = False
is_jump = False
is_F1 = True
Debug = False
death = False
complete = False  # Level complete flag
death_flag = 0
complete_flag = 0
pause_flag = 0
en = True  # English language flag

player = None
camera = None
level_data = None
CC = None  # Label "Coins Collected" in selected language

'''
Formula for converting coordinates from the white surface to the main screen:
x1 = x + 160, y1 = y + 90
x1, y1 - coordinates on the main screen
x, y - coordinates on the white surface
'''

# Create a screen
pygame.init()
screen = pygame.display.set_mode((640, 360), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("JumpOverlord")
clock = pygame.time.Clock()

pause_bg_alpha = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pause_bg_alpha.set_alpha(128)
pause_bg_alpha.fill((0, 0, 0, 128))

# Load fonts and signs

font = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 20)
font1 = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 36)
font_set = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 12)

start_button = font.render("Play", True, "black")
levels_label = font1.render("Levels", True, "white")
confirm_exit_label = font.render("Are you sure you want to leave?", True, "black")
yes = font.render("Yes", True, "black")
no = font.render("No", True, "black")
settings_label = font.render("Settings", True, "black")
pause_label = font.render("Pause", True, (255, 255, 255))
exit_pause = font.render("Exit", True, "black")
F1_mode = font_set.render("Fullscreen mode", True, "black")
debug_label = font_set.render("Debug", True, "black")

lose_label = font.render("You lost!", True, "black")
restart = font.render("return to Main Menu", True, "black")
win = font.render("You won!", True, "black")
lan_en = font_set.render("Language", True, "black")

# Load images
back = pygame.image.load("images/back.png").convert_alpha()
exit_button = pygame.image.load("images/exit_button.png").convert_alpha()
exit_game = pygame.image.load("images/exit_game.png").convert_alpha()
pause_button = pygame.image.load("images/pause_button.png").convert_alpha()
exit_pause_triangle = pygame.image.load("images/l_pause.png").convert_alpha()
check = pygame.image.load("images/check.png").convert_alpha()
gray = pygame.image.load("images/gray.png").convert_alpha()
retry_img = pygame.image.load("images/restart.png").convert_alpha()
setting = pygame.image.load("images/setting.png").convert_alpha()
one = pygame.image.load("images/one.png").convert_alpha()
us_uk_flag = pygame.image.load("images/US_UK_flag.png").convert_alpha()
ru_flag = pygame.image.load("images/RU_flag.jpg").convert_alpha()

level_bg = pygame.image.load("images/level_menu1.jpg").convert()
gaming_bg = pygame.image.load("images/gamingbg.jpg").convert()
# Create the surface "white" (surface for a background when opening widgets)
white = pygame.Surface((320, 180))
white.fill((255, 255, 255))
white_hb = white.get_rect()
white_hb.center = (640 // 2, 360 // 2)
# Load textures
player_texture = pygame.image.load("images/player.png").convert_alpha()  # игрок
enemy = pygame.image.load("images/enemy.png").convert_alpha()  # враг
wall = pygame.image.load("images/brickwall.jpg").convert_alpha()  # стена
every_platform = pygame.image.load(
    "images/platform.jpg").convert_alpha()
spikes = pygame.image.load("images/spikes.png").convert_alpha()
money = pygame.image.load("images/money.png")
door = pygame.image.load("images/door.png")
cp0 = pygame.image.load("images/checkpoint0.png").convert_alpha()
cp1 = pygame.image.load("images/checkpoint1.png").convert_alpha()
start_end = pygame.image.load("images/startend.png").convert_alpha()
chest = pygame.image.load("images/chest.png").convert_alpha()
FAK = pygame.image.load("images/FAK.png").convert_alpha()  # First aid kit
button = pygame.image.load("images/button0.png").convert_alpha()

# Load player textures
player_right = [
    pygame.image.load('pright/sprite_13.png').convert_alpha(),
    pygame.image.load('pright/sprite_14.png').convert_alpha(),
    pygame.image.load('pright/sprite_15.png').convert_alpha(),
    pygame.image.load('pright/sprite_16.png').convert_alpha()
]
player_left = [
    pygame.image.load('pleft/sprite_9.png').convert_alpha(),
    pygame.image.load('pleft/sprite_10.png').convert_alpha(),
    pygame.image.load('pleft/sprite_11.png').convert_alpha(),
    pygame.image.load('pleft/sprite_12.png').convert_alpha()
]
# Create simple figures
Start_button = pygame.rect.Rect((270, 130, 100, 50))  # Start button
setting_rect = pygame.rect.Rect((580, 300, 60, 60))

# Create select markers (in settings)
g_F1 = gray
g_debug = gray

running = True
while running:
    mouse = pygame.mouse.get_pos()
    if not gameplay:
        # Draw the main menu
        screen.fill((37, 150, 190))

        # Create a start button
        pygame.draw.rect(screen, (255, 255, 255), Start_button, border_radius=10)
        pygame.draw.rect(screen, (158, 158, 158), (270, 130, 100, 50), border_radius=10, width=3)
        screen.blit(start_button, (290, 140))
        # Create a settings button
        pygame.draw.rect(screen, (255, 255, 255), setting_rect)
        screen.blit(setting, (587, 307))
        # Create an exit game button
        screen.blit(exit_game, (0, 0))

        # Update the surface
        if not is_open_setting and not exit_game_flag:
            white.fill((255, 255, 255))

        # Initialize settings menu
        if is_open_setting and not exit_game_flag:
            screen.blit(white, white_hb)
            draw_settings_menu()

        # Initialize exit game menu
        if exit_game_flag and not is_open_setting:
            screen.blit(white, white_hb)  # Create a settings surface
            # Create a game exit confirmation
            white.blit(exit_button, (290, 5))
            white.blit(confirm_exit_label, (20, 20))
            white.blit(yes, (120, 130))
            white.blit(no, (180, 130))
        # Initialize select level menu
        if is_open_level_select_menu:
            screen.blit(level_bg, (0, 0))
            screen.blit(exit_button, (0, 0))
            screen.blit(levels_label, (280, 20))
            screen.blit(one, (50, 50))  # Create the first level label
            pygame.display.update()
            # TODO: add more levels
    else:
        # Initialize game
        if player and camera and level_data:
            if not pause and not death and not complete:
                # Reset flags
                death_flag = 0
                pause_flag = 0
                complete_flag = 0

                keys = pygame.key.get_pressed()
                if player:
                    player.move(keys, level_data)
                    camera.update(player)

                # Draw game
                screen.blit(gaming_bg, (0, 0))
                if camera:
                    draw_level(screen, level_data, camera)
                player.draw(screen, camera.x, camera.y)
                screen.blit(pause_button, (0, 0))

            elif pause:
                # Create exit pause button surface
                exit_pause = pygame.Surface((25, 25))
                exit_pause.fill((255, 255, 255))
                # Render pause menu static UI elements once
                if pause_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    screen.blit(pause_label, (SCREEN_WIDTH // 2 - pause_label.get_width() // 2, 10))  # Center the label
                    screen.blit(exit_pause_triangle,
                                (SCREEN_WIDTH // 2 - pause_label.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - pause_label.get_height()))
                    # Render alternative exit UI buttons
                    screen.blit(exit_pause, (0, 0))
                    screen.blit(exit_button, (0, 0))
                    # Render resume game icon
                    screen.blit(pygame.transform.flip(back, True, False), (610, 5))
                    pause_flag = 1

            elif death:
                pause = False
                pause_flag = 0
                # Render Game Over UI elements once
                if death_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    # Center and render the UI elements
                    screen.blit(lose_label, (SCREEN_WIDTH // 2 - 60, 25))
                    screen.blit(retry_img, (SCREEN_WIDTH // 2 + 30, 250))
                    # Center and render the exit button
                    screen.blit(pygame.transform.scale(exit_button, (45, 45)), (SCREEN_WIDTH // 2 - 30, 250))
                    death_flag = 1
            # Render Victory Screen UI elements once
            elif complete:
                pause = False
                pause_flag = 0
                if complete_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    screen.blit(win, (SCREEN_WIDTH // 2 - 60, 25))
                    screen.blit(pygame.transform.scale(exit_button, (45, 45)), (SCREEN_WIDTH // 2 - 60, 250))

                    # Render and draw collected coins counter
                    coin_c = font.render(f"{CC}: {coin}/{coins_level}", True, "black")
                    screen.blit(coin_c, (SCREEN_WIDTH // 2 - 60, 100))

                    complete_flag = 1

    clock.tick(FPS)
    pygame.display.update()
    # Main event loop
    for event in pygame.event.get():
        # Exit the game
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard input events
        if event.type == pygame.KEYDOWN:
            # Handle "ESCAPE" input events
            if event.key == pygame.K_ESCAPE and gameplay:  # Toggle pause mode
                pause = not pause
            elif event.key == pygame.K_ESCAPE and not gameplay and menu and not is_open_setting and not exit_game_flag and not is_open_level_select_menu:
                # Trigger exit confirmation dialog from the game
                exit_game_flag = True
            elif event.key == pygame.K_ESCAPE and not gameplay and is_open_level_select_menu:
                # Close level selection menu and return to main menu
                is_open_level_select_menu = False
            elif event.key == pygame.K_ESCAPE and exit_game_flag and not is_open_setting:
                # Quit the game entirely from exit confirmation screen
                running = False
            # Toggle fullscreen mode
            if event.key == pygame.K_F1 and not gameplay:
                pygame.display.toggle_fullscreen()

            if player and gameplay and not pause:
                player.jump(event)

        # Handle mouse input events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos  # Get current mouse cursor coordinates on click

            # Main Menu navigation
            if not gameplay and not is_open_level_select_menu:
                # Handle "Play" button click to open level selection
                if Start_button.collidepoint(mouse_pos) and not is_open_setting and not exit_game_flag:
                    is_open_level_select_menu = True

                # Handle "Settings" button click to open settings
                elif setting_rect.collidepoint(mouse_pos) and not exit_game_flag:
                    is_open_setting = True
                # Toggle fullscreen mode in settings
                elif is_open_setting and g_F1.get_rect(topleft=(205, 160)).collidepoint(mouse_pos):
                    pygame.display.toggle_fullscreen()
                    is_F1 = not is_F1
                # Toggle debug mode
                elif is_open_setting and g_debug.get_rect(topleft=(205, 173)).collidepoint(mouse_pos):
                    Debug = not Debug

                # Handle "Close Settings" button click
                elif is_open_setting and exit_button.get_rect(topleft=(450, 95)).collidepoint(mouse_pos):
                    is_open_setting = False

                # Handle "Exit Game" button click
                elif exit_game.get_rect(topleft=(0, 0)).collidepoint(mouse_pos) and not is_open_setting:
                    exit_game_flag = True

                # Handle "Change Language (flag)" button click
                elif us_uk_flag.get_rect(topleft=(205, 130)).collidepoint(mouse_pos) and is_open_setting:
                    en = not en
                    draw_settings_menu()

                # Handle exit confirmation input
                elif exit_game_flag:
                    if yes.get_rect(topleft=(280, 220)).collidepoint(mouse_pos):
                        running = False
                    elif no.get_rect(topleft=(340, 220)).collidepoint(mouse_pos) or \
                            exit_button.get_rect(topleft=(450, 95)).collidepoint(mouse_pos):
                        exit_game_flag = False

            # Level Selection menu navigation
            elif is_open_level_select_menu:
                # Handle "Back to Main Menu" button click
                if exit_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                    is_open_level_select_menu = False
                # Launch Level 1 using the universal reset function
                elif one.get_rect(topleft=(50, 50)).collidepoint(mouse_pos):
                    reset_level(1)

            # Gameplay UI navigation
            elif gameplay:
                if not pause and not death and not complete:
                    # Handle pause button click in the corner
                    if pause_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                        pause = True

                elif pause:
                    # Pause menu navigation
                    # Handle "Resume" button click
                    if exit_pause_triangle.get_rect(topleft=(SCREEN_WIDTH // 2 - pause_label.get_width() // 2,
                                                             SCREEN_HEIGHT // 2 - pause_label.get_height())).collidepoint(
                        mouse_pos):
                        pause = False
                    # Handle "Return to Main Menu" button click
                    if back.get_rect(topleft=(610, 5)).collidepoint(mouse_pos):
                        # Reset game state flags
                        gameplay = False
                        pause = False
                        death = False
                        complete = False
                        death_flag = 0
                        complete_flag = 0
                        is_open_level_select_menu = False
                        timer = 0
                    # Handle "Close pause" button click
                    elif exit_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                        pause = False
            if death:
                # Death screen navigation
                # Handle Exit to Main Menu button click
                if pygame.transform.scale(exit_button, (45, 45)).get_rect(
                        topleft=(SCREEN_WIDTH // 2 - 30, 250)).collidepoint(mouse_pos):
                    # Reset game state flags
                    gameplay = False
                    death = False
                    death_flag = 0
                    complete = False
                    complete_flag = 0
                    coin = 0
                # Handle retry button click
                elif retry_img.get_rect(topleft=(SCREEN_WIDTH // 2 + 30, 250)).collidepoint(mouse_pos):
                    reset_level(int(Level_path))
            elif complete:
                # Victory screen navigation
                if pygame.transform.scale(exit_button, (45, 45)).get_rect(
                        topleft=(SCREEN_WIDTH // 2 - 60, 250)).collidepoint(mouse_pos):
                    # Reset game state flags
                    complete = False
                    gameplay = False
                    is_open_level_select_menu = False
                    complete_flag = 0
                    death_flag = 0
                    coin = 0
                    # timer = 0
