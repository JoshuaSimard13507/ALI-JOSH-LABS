class Player:
    def __init__(self, username: str, is_ai: bool = False):
        self.username = username
        self.lifetime_score = 0
        self.wins = 0
        self.games = 0
        self.is_ai = is_ai
        self.points = 0

    def win(self):
        self.wins += 1
        self.games += 1

    def lose(self):
        self.games += 1

    def bank_points(self, points: int):
        self.points += points
    
    def get_points(self):
        return self.points