import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800

# Colors
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circular Wave Animation")

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Variables for wave animation
center_x, center_y = WIDTH // 2, HEIGHT // 2
max_radius = math.hypot(WIDTH, HEIGHT) / 2
frequency = 1.0  # Wave frequency (repetitions per second)
speed = 100.0  # Wave propagation speed (pixels per second)
last_tap_time = None
beat_intervals = []

# Function to map brightness based on wave height
def calculate_brightness(radius, time_offset):
    # Calculate wave height using a sine function
    wave = math.sin(2 * math.pi * frequency * (radius - speed * time_offset) / max_radius)
    brightness = int((wave + 1) / 2 * 255)  # Normalize to [0, 255]
    return brightness

# Main loop
running = True
start_time = time.time()
while running:
    screen.fill(BLACK)
    current_time = time.time() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            tap_time = time.time()
            if last_tap_time:
                interval = tap_time - last_tap_time
                beat_intervals.append(interval)
                if len(beat_intervals) > 5:  # Use last 5 intervals for smoothing
                    beat_intervals.pop(0)
                average_interval = sum(beat_intervals) / len(beat_intervals)
                frequency = 1 / average_interval
                speed = max_radius / average_interval
            last_tap_time = tap_time

    # Draw the wave
    for x in range(WIDTH):
        for y in range(HEIGHT):
            radius = math.hypot(x - center_x, y - center_y)
            brightness = calculate_brightness(radius, current_time)
            color = (brightness, brightness, brightness)
            screen.set_at((x, y), color)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
