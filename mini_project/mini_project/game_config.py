from dataclasses import dataclass
from pathlib import Path


@dataclass
class Dimensions:
    x: int
    y: int

@dataclass
class EntityConfig:
    min_width: int
    max_width: int
    min_speed: int
    max_speed: int
    image_path: Path

@dataclass
class PlayerConfig(EntityConfig):
    score: int

@dataclass
class TargetConfig(EntityConfig):
    pass

@dataclass
class GameConfig:
    player_config: PlayerConfig
    target_config: TargetConfig
    screen_size: Dimensions
    max_targets: int
    game_time: int
    font_size: int

