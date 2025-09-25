from Player import Player
from DicePool import DicePool
from CalculateScore import CalculateScore
from collections import Counter

class Game:
    def __init__(self):
        self.players = [Player("AI", is_ai=True)]
        self.target_score = 10000
        self.dice_pool: DicePool = DicePool()
        self.current_round = 0
        self.game_running = True
        self.current_player = self.players[0]
        self.calculate_scoreobj = CalculateScore()


    def run_match(self):
        current_dice = 6
        self.banked_dice = []
        print("It is ", self.current_player.get_username(), "'s Turn.")
        self.run_round(current_dice)

    def run_round(self, current_dice):
        self.dice_pool.roll(current_dice)
        print("Your roll is: ", self.dice_pool.get_dice_raw(current_dice))
        self.current_player.bank_points(self.calculate_score(current_dice)[0])
        print("You've banked ", self.current_player.get_points(), " points.")


    #Selection is which dice face was selected
    #Dice count is how many of those faces exist in the pool
    def calculate_score(self, inp_length):
        selection = input("Which face would you like to bank?")

        counts = Counter(d for d in self.dice_pool.get_dice_raw(inp_length))
        dice_count = counts[selection]
        print(counts)
        print(counts[selection])
        print(dice_count)
        print(selection)
        if dice_count == 1 or dice_count == 2 and selection == 1:
            return 100*dice_count, 1
        elif dice_count == 1 or dice_count == 2 and selection == 5:
            return 50*dice_count, 1
        elif dice_count == 3 and selection == 1:
            return 1000, 3
        elif dice_count == 3:
            return selection*100, 3
        elif dice_count == 4:
            return 1000, 4
        elif dice_count == 5:
            return 2000, 5
        elif dice_count == 6:
            return 3000, 6
        else:
            return 0,0



    def init_game(self):
        print("It's time to play Farkle!")
        self.players.append(Player(input("Enter your username, player: ")))

    def end_game(self):
        pass # same as init game, print goodbye message, final scores, determine winner? again, if unnecessary just remove it