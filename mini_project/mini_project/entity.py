from __future__ import annotations
from pathlib import Path
from pygame.transform import scale
from pygame import Surface, Rect, image

from .game_config import Dimensions

class Entity:
    def __init__(
            self, 
            starting_position: Dimensions,
            entity_width: int, 
            entity_max_width: int, 
            image_path: Path):
        
        self.width: int = entity_width
        self.max_width: int = entity_max_width
        self.x: int = starting_position.x - entity_width
        self.y: int = starting_position.y - entity_width

        self.image: Surface = image.load(image_path).convert_alpha()
        self.scaled_image: Surface = scale(self.image, (self.width, self.width))
        self.hit_box: Rect = self.get_hit_box(x=self.x, y=self.y)

    def get_hit_box(self, x: int, y: int) -> Rect:
        return self.scaled_image.get_rect(center=(x, y))
    
    def is_colliding_with(self, target: Entity) -> bool:
        return self.hit_box.colliderect(target.hit_box)
    
    def is_larger_than(self, target: Entity) -> bool:
        return self.hit_box.width >= target.hit_box.width
    
    def draw(self, screen: Surface) -> None:
        self.hit_box = self.get_hit_box(x=self.x, y=self.y)
        screen.blit(self.scaled_image, self.hit_box.topleft)