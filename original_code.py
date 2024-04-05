import pygame
import random
import sys


# Initialization
pygame.init()


screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))


# Load and scale images
target_image = pygame.image.load('target_IMG.png').convert_alpha()
player_image = pygame.image.load('player_IMG.png').convert_alpha()
target_image = pygame.transform.scale(target_image, (30, 30))


# Timer setup
counter, text = 120, '120'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)


# Player class
class Player:
    def __init__(self):
        self.width = 30
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.score = 0
        self.player_image = pygame.transform.scale(player_image, (self.width, self.width))
        self.playerRect = self.player_image.get_rect(center=(self.x, self.y))


    def draw(self):
        screen.blit(self.player_image, self.playerRect.topleft)


    def move(self):
        keys = pygame.key.get_pressed()
        move_speed = 5


        if keys[pygame.K_UP]:
            self.playerRect.y -= move_speed
        if keys[pygame.K_DOWN]:
            self.playerRect.y += move_speed
        if keys[pygame.K_LEFT]:
            self.playerRect.x -= move_speed
        if keys[pygame.K_RIGHT]:
            self.playerRect.x += move_speed


        # Keep player within screen bounds
        self.playerRect.clamp_ip(screen.get_rect())


    def grow(self):
        # Grow only if the width is under a certain threshold.
        if self.width < 100:
            self.width += 1
            self.score += 1
            self.player_image = pygame.transform.scale(self.player_image, (self.width, self.width))
            self.playerRect = self.player_image.get_rect(center=(self.x, self.y))


class Target:
    def __init__(self):
        self.width = random.randint(20, 40)  # Random size for variety
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(0, screen_height - self.width)
        self.x_speed = random.randint(-3, 3)
        self.y_speed = random.randint(-3, 3)
        self.target_image = pygame.transform.scale(target_image, (self.width, self.width))
        self.targetRect = self.target_image.get_rect(center=(self.x, self.y))


    def draw(self):
        screen.blit(self.target_image, self.targetRect.topleft)


    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.targetRect.x += self.x_speed
        self.targetRect.y += self.y_speed
        # Reverse direction upon hitting a wall
        if self.targetRect.left <= 0 or self.targetRect.right >= screen_width:
            self.x_speed = -self.x_speed
        if self.targetRect.top <= 0 or self.targetRect.bottom >= screen_height:
            self.y_speed = -self.y_speed


def check_collision(playerRect, targetRect):
    return playerRect.colliderect(targetRect)
# Initialize player
player = Player()


# Main game loop
running = True
while running:
    targets = [Target() for _ in range(5)]  # Initialize/reinitialize targets here for fresh start on game reset
    clock = pygame.time.Clock()


    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            counter -= 1
            if counter <= 0:
                # Game reset logic
                counter = 120  # Reset counter
                player.score = 0  # Reset player score
                player.__init__()  # Reset player attributes
                targets = [Target() for _ in range(5)]  # Reinitialize targets


        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))
    player.move()
    player.draw()


    for target in list(targets):  # Create a copy of the targets list to iterate over
        target.move()
        target.draw()
        if player.playerRect.colliderect(target.targetRect):
            if player.playerRect.width >= target.targetRect.width:
                player.grow()
                targets.remove(target)
                # Add a new target making sure it does not collide with the player immediately
                while True:
                    new_target = Target()
                    if not player.playerRect.colliderect(new_target.targetRect):
                        targets.append(new_target)
                        break


    # Display score and timer
    font = pygame.font.SysFont(None, 36)
    score_text = font.render('Score: {}'.format(player.score), True, "WHITE")
    timer_text = font.render('Timer: {}'.format(counter), True, "WHITE")
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 50))


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()