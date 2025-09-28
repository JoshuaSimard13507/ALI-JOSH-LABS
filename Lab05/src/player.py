import os
import json

class Player:
    """Represents a single player in the game.


    Attributes:
    username (str): The player's name.
    points (int): The player's current score in the ongoing game.
    wins (int): Lifetime win count.
    games (int): Total games played.
    lifetime_score (int): Total points scored across all games.
    is_ai (bool): Whether the player is an AI.
    """
    def __init__(self, username: str, is_ai: bool = False):
        """Create a player.


        :param username: The player's username.
        :type username: str
        :param is_ai: True if the player should take automated turns.
        :type is_ai: bool
        """
        self.username: str = username
        self.lifetime_score: int = 0
        self.wins: int = 0
        self.games: int = 0
        self.is_ai: bool = is_ai
        self.points: int = 0

    def win(self):
        """Record a win for this player and increment games played."""
        self.wins += 1
        self.games += 1

    def lose(self):
        """Record a loss for this player (increments games only)."""
        self.games += 1

    def bank_points(self, points: int):
        """Add scored points to the player's round total.


        :param score: Points to add.
        :type score: int
        """
        self.points += points

    def save(self):
        """Persist the player's stats to a JSON file under data/players.


        Creates the folder if necessary.
        """
        os.makedirs("data/players", exist_ok=True)
        path = f"data/players/{self.username.lower()}.json"
        data_dict = {
            "username": self.username.lower(),
            "lifetime_score": self.lifetime_score,
            "wins": self.wins,
            "games": self.games,
            "is_ai": self.is_ai
        }
        with open(path, "w") as f:
            json.dump(data_dict, f)

    def load(self, username_to_load: str | None = None) -> bool:
        """Load stats from a saved player file.


        :param username: Username (case-insensitive) whose stats to load.
        :type username: str
        :return: True if load succeeded, False otherwise.
        :rtype: bool
        """
        path = f"data/players/{self.username.lower() if username_to_load is None else username_to_load.lower()}.json"

        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            data_dict = json.load(f)

        self.username = data_dict.get("username", "PLAYER").upper()
        self.lifetime_score = data_dict.get("lifetime_score", 0)
        self.wins = data_dict.get("wins", 0)
        self.games = data_dict.get("games", 0)
        self.is_ai = data_dict.get("is_ai", False)
        return True
