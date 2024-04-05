from pygame import init, display, time, image, event
from pygame import Surface, Rect
from pygame import USEREVENT, QUIT
from pygame.transform import scale
from pygame.font import SysFont
from random import randint

from .target import Target
from .player import Player


class GameEngine:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

        self.screen: Surface = None
        self.target_image: Surface = None
        
        self.is_running: bool = False
        self.counter: int = 0

        self.max_targets: int = 5

    def setup(self) -> None:
        init()
        self.screen = display.set_mode((self.screen_width, self.screen_height))
        # Timer setup
        self.counter = 120
        time.set_timer(USEREVENT, 1000)
    
    def create_targets(self, count: int = 5) -> list[Target]:
        return [
            self.create_target() 
            for _ in range(count)
            ]

    def create_target(self) -> Target:
        if self.target_image is None:
            self.target_image = scale(image.load('assets/target_IMG.png').convert_alpha(), (30, 30))

        return Target(
            screen_height=self.screen_height, 
            screen_width=self.screen_width, 
            image=self.target_image)

    def display_score_and_timer(self, player: Player) -> None:
        # Display score and timer
        font = SysFont(None, 36)
        score_text = font.render('Score: {}'.format(player.score), True, "WHITE")
        timer_text = font.render('Timer: {}'.format(self.counter), True, "WHITE")
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (10, 50))

    def display_debug_info(self, entity: Player | Target, offset: int = 0) -> None:
        font = SysFont(None, 15)
        name = type(entity).__name__
        coords = font.render(f'{name} Coords: x: {entity.x}, y: {entity.y}', True, "WHITE")
        size = font.render(f'{name} Size: {entity.width}', True, "WHITE")
        self.screen.blit(coords, (10, 90 + offset))
        self.screen.blit(size, (10, 100 + offset))


    def get_surviving_targets(self, targets: list[Target]) -> list[Target]:
        surviving_targets = []
        for target in targets:
            if not target.is_eaten:
                surviving_targets.append(target)
        return surviving_targets

    def add_new_target(self, player: Player) -> Target:
        # Add a new target making sure it does not collide with the player immediately
        colliding = True
        while colliding:
            new_target = self.create_target()
            colliding = player.is_colliding_with(new_target)
        return new_target

    def run(self, player: Player) -> None:
        # Main game loop
        self.is_running = True
        targets = self.create_targets(count=self.max_targets) # Initialize/reinitialize targets here for fresh start on game reset
        while self.is_running:
            
            clock = time.Clock()

            for pygame_event in event.get():
                if pygame_event.type == USEREVENT:
                    self.counter -= 1
                    if self.counter <= 0:
                        # Game reset logic
                        self.counter = 120  # Reset counter
                        player.reset(
                            screen_width=self.screen_width, 
                            screen_height=self.screen_height)
                        
                        targets = self.create_targets(count=5)  # Reinitialize targets

                if pygame_event.type == QUIT:
                    self.is_running = False

            self.screen.fill((0, 0, 0))
            player.move(self.screen)
            player.draw(self.screen)

            offset_multiplier = 1 # This is just for debug - not for the actual gameplay
            for target in targets:
                target.move(screen_height=self.screen_height, screen_width=self.screen_width)
                target.draw(screen=self.screen)
                
                self.display_debug_info(entity=target, offset=30 * offset_multiplier)
                offset_multiplier += 1

                if player.is_colliding_with(target):
                    if player.is_larger_than(target):
                        player.grow()
                        target.get_eaten()
            
            targets = self.get_surviving_targets(targets=targets)
            
            if len(targets) < self.max_targets:
                rng = randint(1,100)
                # 1% chance a new target will spawn - adjust the number below to improve the chances
                if rng > 99:
                    targets.append(self.add_new_target(player=player))

            self.display_score_and_timer(player=player)
            self.display_debug_info(entity=player)
            
            display.flip()
            clock.tick(60)
