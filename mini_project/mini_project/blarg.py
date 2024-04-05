import pygame

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



