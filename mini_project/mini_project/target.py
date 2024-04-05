from random import randint
from pygame.transform import scale
from pygame import Surface, Rect

class Target:
    def __init__(self, screen_width: float, screen_height: float, image: Surface):
        self.width = randint(20, 40)  # Random size for variety
        self.x: float = randint(0, screen_width - self.width)
        self.y: float = randint(0, screen_height - self.width)
        self.x_speed: int = randint(-3, 3)
        self.y_speed: int = randint(-3, 3)
        self.target_image: Surface = scale(image, (self.width, self.width))
        self.hit_box: Rect = self.get_hit_box()
        self.is_eaten = False

    def get_eaten(self):
        self.is_eaten = True

    def get_hit_box(self):
        return self.target_image.get_rect(center=(self.x, self.y))

    def draw(self, screen: Surface):
        self.hit_box = self.get_hit_box()
        screen.blit(self.target_image, self.hit_box.topleft)


    def move(self, screen_width: float, screen_height: float):
        self.x += self.x_speed
        self.y += self.y_speed
        
        # Reverse direction upon hitting a wall
        if self.x <= 0 or self.x >= screen_width:
            self.x_speed = -self.x_speed
        if self.y <= 0 or self.y >= screen_height:
            self.y_speed = -self.y_speed