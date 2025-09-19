from CalculateScore import CalculateScore
from Player import Player


### DEPRECATED ###
class Setup:
    def __init__(self):
        self.calculate_score = CalculateScore.default
        self.running = True
        self.players = [Player("P1"), Player("AI", is_ai=True)]
        self.target_score = 10000

    def run(self): 
        while self.running:
            user_in = input("> ").split()
            if user_in[0] == "help":
                pass # display commands
            elif user_in[0] == "scoring":
                if len(user_in) != 2:
                    print("Bad input")
                elif user_in[1] in self.scoring_methods:
                    self.calculate_score = self.scoring_methods[user_in[1]]
                else:
                    print("Not a scoring method")
            elif user_in[0] == "toggle-ai":
                if len(user_in) != 2:
                    print("Bad input")
                elif not self.toggle_ai(user_in[1]):
                    print("Not a player")
            elif user_in[0] == "toggle-hot-dice":
                self.hot_dice_enabled = not self.hot_dice_enabled

    def toggle_ai(self, username: str) -> bool:
        for player in self.players:
            if player.username == username:
                player.is_ai = not player.is_ai
                return True
        return False

    def rename(self, username: str, new: str) -> bool:
        for player in self.players:
            if player.username == new: # only rename uniquely
                return False
            if player.username == username:
                player.username = new
                return True
        return False

    def add_player(self, username: str):
        pass

    def remove_player(self, username: str):
        pass

    def create_game(self):
        game = Game(self, self.players)
        game.run()