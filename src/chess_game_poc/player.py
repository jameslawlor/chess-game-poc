from typing import List
from chess_game_poc.powers import Power


class Player:
    def __init__(self, powers: List[Power] = None):
        self.score = 0  # Initialize player score