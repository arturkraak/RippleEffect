import pygame as pg
import numpy as np
from os import listdir
import random

pg.init()
pg.mixer.init()  # Initialize the mixer module.
# drip_snd = pg.mixer.Sound('drip.ogg')  # Load a sound.

SIZE = WIDTH, HEIGHT = 1280, 720
screen = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
run = True

WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 35, 255)
LIGHT_BLUE = (20, 55, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BOX_SIZE = 50
FPS = 120

# Tiles (Square)
TILE_WIDTH = 16
SCALE = 7.5
UNIT = TILE_WIDTH * SCALE

# Load sounds
drip_sounds = []
snd_dir = "snd/drip"
for sound_file in listdir(snd_dir):
    drip_sounds.append(pg.mixer.Sound(f"{snd_dir}/{sound_file}"))

# Load images
tiles = pg.image.load("tiles.png")
tiles_rect = tiles.get_rect()
tileset_array = pg.surfarray.array3d(tiles)
# print(tiles_rect)

# Find out how many tiles in the image per column (x) and row (y)
tiles_x = (tiles_rect.width // TILE_WIDTH) 
tiles_y = (tiles_rect.height // TILE_WIDTH)
tiles_total = tiles_x * tiles_y
print(f"Num of total tiles: {tiles_total}")

tiles_off_x = 3
tiles_off_y = 0
tiles_id = 3

# Reserve the last tile as empty, any other tile that matches the last tile should also be empty.
# Count the filled tiles.

# Empty tile in the bottom right corner
empty_tile_x = (tiles_y - 1) * TILE_WIDTH
empty_tile_y = (tiles_x - 1) * TILE_WIDTH
empty_tile_array = tileset_array[empty_tile_x:empty_tile_x+TILE_WIDTH, empty_tile_y:empty_tile_y+TILE_WIDTH, :]

# Check if a tile matches the empty tile
def is_tile_empty(tile_array, empty_tile_array):
    return np.array_equal(tile_array, empty_tile_array)

# Camera
cam_off_x = 0
cam_off_y = 0
cam_speed = 10

def find_first_empty_tile():
    for row in range(tiles_y):
        for col in range(tiles_x):
            # Extract tile at (col, row)
            x = col * TILE_WIDTH
            y = row * TILE_WIDTH
            tile_array = tileset_array[x:x+TILE_WIDTH, y:y+TILE_WIDTH, :]
            
            # Compare with empty tile
            if is_tile_empty(tile_array, empty_tile_array):
                return row * tiles_x + col

filled_tiles = find_first_empty_tile()
print(f"Num of filled tiles: {filled_tiles}")
print(f"Num of empty tiles: {tiles_total - filled_tiles}")

# Time
flip_interval = 500
last_flip = pg.time.get_ticks()

mirrored = False

ripples = []
ripple_size = 8
ripple_speed = 5
ripple_shrink_rate = 1
ripple_spawn_rate = 300
create_ripple_rate = 200

last_ripple = pg.time.get_ticks()

class Ripple:
    def __init__(self, x, y, r, w, t, color = LIGHT_BLUE, spawned = False):
        self.x = x
        self.y = y
        self.r = r
        self.w = w
        self.t = t
        self.color = color
        self.spawned = spawned
        ripples.append(self)
        # print(self)

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x + cam_off_x, self.y + cam_off_y), self.r, width=self.w)

    def update(self, current_time):
        if self.r > WIDTH // 2:
            ripples.remove(self)
            # print(len(ripples))
        self.r += ripple_speed
        if not self.spawned:
            if current_time > self.t + ripple_spawn_rate:
                if self.w > ripple_shrink_rate:
                    Ripple(self.x, self.y, 1, self.w - ripple_shrink_rate, current_time)
                    self.spawned = True

while run:
    current_time = pg.time.get_ticks()
    mouse_x, mouse_y = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            Ripple(mouse_x - cam_off_x, mouse_y - cam_off_y, 1, ripple_size, current_time)
            last_ripple = current_time + create_ripple_rate
            drip_sound = random.choice(drip_sounds)
            print(f"drip{drip_sounds.index(drip_sound)+1}.ogg")
            drip_sound.play()
        # Quit game
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False

            if event.key == pg.K_r:
                cam_off_x = 0
                cam_off_y = 0

            if filled_tiles:
                if event.key == pg.K_RIGHT:
                    # increment tile_id, else roll over
                    tiles_id = (tiles_id + 1) % filled_tiles
                            
                if event.key == pg.K_LEFT:
                    # decrement tile_id, else roll over
                    tiles_id = (tiles_id - 1) % filled_tiles

            # How many columns per row?
            # Divide tile_id by columns (x) to get the y-offset and the remaider will be the x-offset
            tiles_off_y, tiles_off_x = divmod(tiles_id, tiles_x) 
            print(f"tile_id: {tiles_id}")

        if event.type == pg.QUIT:
            run = False

    # Camera controls
    keys=pg.key.get_pressed()
    if keys[pg.K_w]:
        cam_off_y += cam_speed
    if keys[pg.K_s]:
        cam_off_y -= cam_speed
    if keys[pg.K_a]:
        cam_off_x += cam_speed
    if keys[pg.K_d]:
        cam_off_x -= cam_speed

    # Flip image periodically
    if current_time - last_flip >= flip_interval:
        tiles = pg.transform.flip(tiles, True, False)
        mirrored = not mirrored
        last_flip = current_time  # Reset timer

    # Refresh screen by drawing over it
    screen.fill(BLUE)

    # Draw Tiles
    for i in range(11):
        for j in range(6):
            if mirrored:
                screen.blit(pg.transform.scale(tiles, (tiles_rect.width * SCALE, tiles_rect.height * SCALE)), (i * UNIT + cam_off_x, j * UNIT + cam_off_y), ((tiles_x - 1 - tiles_off_x) * UNIT, tiles_off_y * UNIT, UNIT, UNIT))
            else:
                screen.blit(pg.transform.scale(tiles, (tiles_rect.width * SCALE, tiles_rect.height * SCALE)), (i * UNIT + cam_off_x, j * UNIT + cam_off_y), (tiles_off_x * UNIT, tiles_off_y * UNIT, UNIT, UNIT))


    # "Player"
    # pg.draw.circle(screen, RED, (WIDTH//2, HEIGHT//2), 200, width=10)

    # if pg.mouse.get_pressed()[0] and current_time - last_ripple >= create_ripple_rate:
    #     Ripple(mouse_x - cam_off_x, mouse_y - cam_off_y, 1, ripple_size, current_time)
    #     last_ripple = current_time + create_ripple_rate
    #     drip_snd.play()
    
    for ripple in ripples:
        ripple.draw(screen)
        ripple.update(current_time)
    #     pg.draw.rect(screen, GREEN, (mouse_x - BOX_SIZE//2, mouse_y - BOX_SIZE//2, BOX_SIZE, BOX_SIZE))
    # if pg.mouse.get_pressed()[2]:
    #     pg.draw.rect(screen, RED, (mouse_x - BOX_SIZE//2, mouse_y - BOX_SIZE//2, BOX_SIZE, BOX_SIZE))

    pg.display.update()
    clock.tick(FPS)