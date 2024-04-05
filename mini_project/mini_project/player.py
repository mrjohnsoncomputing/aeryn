from pygame.transform import scale
from pygame import Surface, key, K_UP, K_DOWN, K_LEFT, K_RIGHT, Rect, image
from .game_config import PlayerConfig, Dimensions
from .entity import Entity


# Player class
class Player(Entity):
    def __init__(self, starting_position: Dimensions, config: PlayerConfig):
        super().__init__(
            starting_position=starting_position,
            entity_max_width=config.max_width,
            entity_width=config.min_width,
            image_path=config.image_path
        )

        self.config: PlayerConfig = config
        self.move_speed: int = config.min_speed
        self.score: int = config.score

    def reset(self, new_position: Dimensions):
        self.width = self.config.min_width
        self.score = self.config.score
        self.move_speed = self.config.min_speed
        self.scaled_image = scale(self.image, (self.width, self.width))
        self.hit_box = self.get_hit_box(x=new_position.x, y=new_position.y)

    def try_move(self, max_width: int, max_height: int) -> bool: 
        keys = key.get_pressed()
        moved = False
        if keys[K_UP] and self.y > 0 + self.move_speed:
            self.y -= self.move_speed
            moved = True
        if keys[K_DOWN] and self.y < max_height - self.move_speed:
            self.y += self.move_speed
            moved = True
        if keys[K_LEFT] and self.x > 0 + self.move_speed:
            self.x -= self.move_speed
            moved = True
        if keys[K_RIGHT] and self.x < max_width - self.move_speed:
            self.x += self.move_speed
            moved = True
        return moved


    def move(self, screen_size: Dimensions) -> None:
        if self.try_move(screen_size.x, screen_size.y):
            # Keep player within screen bounds
            self.hit_box = self.get_hit_box(self.x, self.y)


    def grow(self) -> None:
        # Do nothing if the width is above or equal to the max
        if self.width >= self.max_width:
            return 
        
        self.width += 1
        self.score += 1
        self.scaled_image = scale(self.image, (self.width, self.width))
        self.hit_box = self.get_hit_box(x=self.x, y=self.y)
