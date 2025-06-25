import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Waterfall")
clock = pygame.time.Clock()

# Load seamless image (replace with your own seamless texture)
# For testing, you can create a simple gradient image
image = pygame.Surface((WIDTH, 200))  # Temporary gradient for demo
for y in range(200):
    if y < 100:
        color = (0, 100, 255 * ((200 - y) / 200))  # Blue gradient
    else:
        color = (0, 100, 255 * (y / 200))  # Blue gradient
    pygame.draw.line(image, color, (0, y), (WIDTH, y))

# Variables for scrolling
scroll_y = 0
scroll_speed = 2  # Pixels per frame
image_height = image.get_height()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update scroll position
    scroll_y = (scroll_y + scroll_speed) % image_height

    # Clear screen
    screen.fill((0, 0, 0), (0, 200, WIDTH, HEIGHT))

    # Draw the image twice to create seamless scrolling
    screen.blit(image, (0, scroll_y + image_height * 2))  # bottom image
    screen.blit(image, (0, scroll_y + image_height))  # mittle 2 image
    screen.blit(image, (0, scroll_y))  # mittle image
    screen.blit(image, (0, scroll_y - image_height))  # Top image

    # Clear screen
    # screen.fill((0, 0, 0), (0, 200, WIDTH, HEIGHT))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()