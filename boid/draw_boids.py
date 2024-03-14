# Example file showing a circle moving on screen
import numpy as np
import pygame
from boid_group import Boids
import os


def draw_arrow(
    surface: pygame.Surface,
    start: pygame.Vector2,
    end: pygame.Vector2,
    color: pygame.Color,
    body_width: int = 2,
    head_width: int = 4,
    head_height: int = 2,
):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(
        0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'boid_img.png')

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
dt = 0

width = 1280
height = 720

screen = pygame.display.set_mode((width, height))


flock = Boids(width, height, deterence_border=80, deterence_force=50, num=50, 
              separation_radius=50, alignment_raduis=200, cohesion_radius=250,
              starting_velo_range=400, max_velo=500, separation_weight=0.5, alignment_weight=0.002, cohesion_weight=0.05, attraction_weight=0.01)
'''
flock = Boids(width, height, deterence_border=80, deterence_force=50, num=50, 
              separation_radius=50, alignment_raduis=200, cohesion_radius=250,
              starting_velo_range=400, max_velo=500, separation_weight=0.5, alignment_weight=0.2, cohesion_weight=0.05, attraction_weight=0.01)
'''

boid_img = pygame.image.load(filename)
draw_vectors = False
attraction_point = None
attraction = False
moving = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                attraction = not attraction
                if attraction:
                    attraction_point = event.pos
                else:
                    attraction_point = None
            if event.button == 3: # right click
                moving = not moving
                if moving:
                    attraction_point = event.pos

        if event.type == pygame.MOUSEMOTION and moving and attraction_point:
            attraction_point = event.pos


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if type(attraction_point) != type(None):
        pygame.draw.circle(screen, pygame.Color('red'), attraction_point, 10)

    flock.update_velocities(attraction_point)
    flock.update_positions(dt)

    for i, pos in enumerate(flock.boid_positions):
        if draw_vectors:
            start = pygame.Vector2(
                flock.boid_positions[i][0], flock.boid_positions[i][1])
            end = start + \
                pygame.Vector2(
                    flock.separation_vectors[i][0], flock.separation_vectors[i][1])
            draw_arrow(screen, start, end, pygame.Color("dodgerblue"), 4, 8, 4)

            start = pygame.Vector2(
                flock.boid_positions[i][0], flock.boid_positions[i][1])
            end = start + \
                pygame.Vector2(
                    flock.alignment_vectors[i][0], flock.alignment_vectors[i][1])
            draw_arrow(screen, start, end, pygame.Color("red"), 4, 8, 4)

            start = pygame.Vector2(
                flock.boid_positions[i][0], flock.boid_positions[i][1])
            end = start + \
                pygame.Vector2(
                    flock.cohesion_vectors[i][0], flock.cohesion_vectors[i][1])
            draw_arrow(screen, start, end, pygame.Color("green"), 4, 8, 4)

            start = pygame.Vector2(pos[0], pos[1])
            end = start + \
                pygame.Vector2(
                    flock.boid_velocities[i][0], flock.boid_velocities[i][1])
            draw_arrow(screen, start, end, pygame.Color("purple"), 8, 12, 8)

        rotated_img = pygame.transform.rotate(boid_img, np.arctan2(
            *flock.boid_velocities[i]) * 180 / np.pi + 180)
        scaled_img = pygame.transform.scale(rotated_img, (16, 16))
        screen.blit(scaled_img, pos-8)
        pygame.draw.circle(screen, pygame.Color('green'), pos, 3)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
