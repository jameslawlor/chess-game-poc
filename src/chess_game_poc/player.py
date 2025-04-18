from typing import List
from chess_game_poc.powers import Power

class Player:
    def __init__(self, powers: List[Power] = None):
        self.score = 0  # Initialize player score
        self.powers = powers if powers else []  # List of powers

    def add_score(self, points: int):
        """Increase the player's score."""
        self.score += points

    def add_power(self, power: Power):
        """Add a new power to the player."""
        self.powers.append(power)

    def remove_power(self, power: Power):
        """Add a new power to the player."""
        self.powers.remove(power)

    def use_power(self, power_name: str) -> bool:
        """Use a power if available."""
        for power in self.powers:
            if power.name == power_name and power.is_available():
                power.activate()
                return True
        return False