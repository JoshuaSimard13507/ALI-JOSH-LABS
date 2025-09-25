import os
import json

class Player:
    def __init__(self, username: str, is_ai: bool = False):
        self.username: str = username
        self.lifetime_score: int = 0
        self.wins: int = 0
        self.games: int = 0
        self.is_ai: bool = is_ai
        self.points: int = 0

    def win(self):
        self.wins += 1
        self.games += 1

    def lose(self):
        self.games += 1

    def bank_points(self, points: int):
        self.points += points

    def save(self):
        os.makedirs("players", exist_ok=True)
        path = f"players/{self.username.lower()}.json"
        data_dict = {
            "username": self.username.lower(),
            "lifetime_score": self.lifetime_score,
            "wins": self.wins,
            "games": self.games,
            "is_ai": self.is_ai
        }
        with open(path, "w") as f:
            json.dump(data_dict, f)

    def load(self) -> bool:
        path = f"players/{self.username.lower()}.json"
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            data_dict = json.load(f)

        self.lifetime_score = data_dict.get("lifetime_score", 0)
        self.wins = data_dict.get("wins", 0)
        self.games = data_dict.get("games", 0)
        self.is_ai = data_dict.get("is_ai", False)
        return True
