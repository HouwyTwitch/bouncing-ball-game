import pygame
import random
import configparser

# Initialize Pygame
pygame.init()

# Load configuration from INI file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up the display
width = config.getint('Display', 'width')
height = config.getint('Display', 'height')
fps = config.getint('Display', 'fps')

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Ball with Gravity, Damping, Friction, and Compression")

# Load ball texture with alpha support
ball_texture = pygame.image.load('assets/ball.png').convert_alpha()
ball_texture = pygame.transform.scale(ball_texture, (config.getint('Ball', 'initial_size'), config.getint('Ball', 'initial_size')))
ball_radius = ball_texture.get_width() // 2

# Ball position initialization
ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = random.randint(ball_radius, height - ball_radius)

# Initial velocity
velocity_x = random.choice([-2, 2])
velocity_y = 0

# Score variable
score = 0
font = pygame.font.Font(None, 36)  # Set up font for score display

# Ground contact tracking
on_ground = False  # Track if the ball is on the ground
is_grabbed = False

# Rotation variables
angle = 0  # Angle of rotation for the ball

# For limiting the ball trail
trail_length = 30  # Increase the number of previous positions to keep
ball_trail = []

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Window resizing
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (mouse_x - ball_x) ** 2 + (mouse_y - ball_y) ** 2 <= ball_radius ** 2:
                is_grabbed = True
                previous_mouse_x, previous_mouse_y = mouse_x, mouse_y
        
        # Mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            if is_grabbed:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                velocity_x = (mouse_x - previous_mouse_x) * 0.5
                velocity_y = (mouse_y - previous_mouse_y) * 0.5
                is_grabbed = False

    # Move the ball if it's being grabbed
    if is_grabbed:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ball_x = max(ball_radius, min(mouse_x, width - ball_radius))
        ball_y = max(ball_radius, min(mouse_y, height - ball_radius))
        previous_mouse_x, previous_mouse_y = mouse_x, mouse_y
    else:
        velocity_y += config.getfloat('Ball', 'gravity')
        ball_x += velocity_x
        ball_y += velocity_y

        # Apply friction
        velocity_x *= config.getfloat('Ball', 'friction')

        # Check for collision with edges and update score
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
            velocity_x = -velocity_x * config.getfloat('Ball', 'damping_factor')
            ball_x = max(ball_radius, min(ball_x, width - ball_radius))
            score += config.getint('Scoring', 'increment_on_wall_collision')
            
        # Check if the ball hits the ground
        if ball_y + ball_radius >= height:
            ball_y = height - ball_radius
            if velocity_y >= 0 and not on_ground and velocity_y >= config.getint('Scoring', 'threshold_velocity'):
                score += config.getint('Scoring', 'increment_on_ground_hit')
                on_ground = True
            velocity_y = -velocity_y * config.getfloat('Ball', 'damping_factor')
            
        elif ball_y - ball_radius <= 0:
            ball_y = ball_radius
            velocity_y = -velocity_y * config.getfloat('Ball', 'damping_factor')
            on_ground = False

        else:
            if ball_y + ball_radius < height:
                on_ground = False

    # Store the current position of the ball for the trail effect
    ball_trail.append((ball_x, ball_y))
    if len(ball_trail) > trail_length:
        ball_trail.pop(0)

    # Clear the screen
    screen.fill((0, 0, 0))  # Clear with a solid color

    # Draw ball trail
    for i, (trail_x, trail_y) in enumerate(ball_trail):
        alpha = 255 - (255 // trail_length) * i  # Gradually decrease alpha
        ball_texture_trail = ball_texture.copy()
        ball_texture_trail.set_alpha(alpha)
        trail_rect = ball_texture_trail.get_rect(center=(trail_x, trail_y))
        screen.blit(ball_texture_trail, trail_rect)

    # Rotate the ball texture based on its velocity
    if velocity_x != 0:  # Rotate only if the ball is moving
        angle += velocity_x * -1
    ball_texture_rotated = pygame.transform.rotate(ball_texture, angle)  # Rotate the texture
    ball_rect = ball_texture_rotated.get_rect(center=(int(ball_x), int(ball_y)))  # Get the new rect
    screen.blit(ball_texture_rotated, ball_rect)  # Draw the ball

    # Render the score
    score_surface = font.render(f"{score}", True, (255, 255, 255))  # Render only the score
    screen.blit(score_surface, (10, 10))  # Display score in the top-left corner

    # Update the display
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
