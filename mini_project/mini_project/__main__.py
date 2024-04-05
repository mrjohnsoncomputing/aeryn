from pygame import quit

from .game_engine import GameEngine
from .player import Player

game_engine = GameEngine(screen_width=640, screen_height=480)

# Initialise Game Engine
game_engine.setup()

# Initialize player
player = Player(
    screen_width=game_engine.screen_width, 
    screen_height=game_engine.screen_height,
    image_path='assets/player_IMG.png'
    )

# Run Game
game_engine.run(player=player)

# Quit Game
quit()
