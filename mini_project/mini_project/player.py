from pygame.transform import scale
from pygame import Surface, key, K_UP, K_DOWN, K_LEFT, K_RIGHT, Rect, image
from .target import Target


# Player class
class Player:
    def __init__(self, screen_width: float, screen_height: float, image_path: str):
        self.width: int = 30
        self.max_width: int = 100
        self.x: int = screen_width // 2
        self.y: int = screen_height // 2
        self.move_speed: int = 5

        self.score: int = 0
        
        self.image: Surface = image.load(image_path).convert_alpha()
        self.scaled_image: Surface = scale(self.image, (self.width, self.width))
        self.hit_box: Rect = self.get_hit_box(x=self.x, y=self.y)
        
    def get_hit_box(self, x: int, y: int) -> Rect:
        return self.scaled_image.get_rect(center=(x, y))

    def reset(self,screen_width: float, screen_height: float):
        self.width = 30
        self.score = 0
        self.move_speed = 5
        self.scaled_image = scale(self.image, (self.width, self.width))
        self.hit_box = self.get_hit_box(x=screen_width // 2, y=screen_height // 2)

    def is_colliding_with(self, target: Target) -> bool:
        return self.hit_box.colliderect(target.hit_box)
    
    def is_larger_than(self, target: Target) -> bool:
        return self.hit_box.width >= target.hit_box.width

    def draw(self, screen: Surface) -> None:
        screen.blit(self.scaled_image, self.hit_box.topleft)

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


    def move(self, screen: Surface) -> None:
        if self.try_move(screen.get_width(), screen.get_height()):
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
