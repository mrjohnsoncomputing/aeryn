from pathlib import Path
from pygame import quit

from .game_config import GameConfig, PlayerConfig, TargetConfig, Dimensions
from .game_engine import GameEngine
from .player import Player


player_config = PlayerConfig(
    min_width=30,
    max_width=100,
    image_path=Path('assets/player_IMG.png'),
    min_speed=5,
    max_speed=5,
    score=0
)

target_config = TargetConfig(
    min_width=20,
    max_width=40,
    min_speed=-3,
    max_speed=3,
    image_path=Path('assets/target_IMG.png')
)

game_config = GameConfig(
    player_config=player_config,
    target_config=target_config,
    screen_size=Dimensions(x=640, y=480),
    max_targets=5,
    game_time=10,
    font_size=36
)


game_engine = GameEngine(game_config=game_config)

# Initialise Game Engine
game_engine.setup()

# Initialize player
player = Player(
    starting_position = Dimensions(
        x = game_config.screen_size.x // 2, 
        y = game_config.screen_size.y // 2),
    config=player_config
    )

# Run Game
game_engine.run(player=player)

# Quit Game
quit()
