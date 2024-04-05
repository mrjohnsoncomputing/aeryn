from random import randint
from pygame.transform import scale
from pygame import Surface, Rect

from .game_config import Dimensions, TargetConfig

from .entity import Entity

class Target(Entity):
    def __init__(self, starting_position: Dimensions, config: TargetConfig):
        super().__init__(
            starting_position=starting_position,
            entity_width=randint(config.min_width, config.max_width),  # Random size for variety
            entity_max_width=config.max_width,
            image_path=config.image_path
        )
        
        self.x_speed: int = randint(config.min_speed, config.max_speed)
        self.y_speed: int = randint(config.min_speed, config.max_speed)
        
        self.is_eaten = False

    def get_eaten(self) -> None:
        self.is_eaten = True

    def move(self, screen_size: Dimensions) -> None:
        self.x += self.x_speed
        self.y += self.y_speed
        
        # Reverse direction upon hitting a wall
        if self.x <= 0 or self.x >= screen_size.x:
            self.x_speed = -self.x_speed
        if self.y <= 0 or self.y >= screen_size.y:
            self.y_speed = -self.y_speed