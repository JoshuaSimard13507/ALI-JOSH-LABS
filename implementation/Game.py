class Game:
    def __init__(self, setup: Setup, players: list[Player], target_score: int = 10000, num_dice: int = 6):
        self.calculate_score = setup.calculate_score
        self.players: list[Player] = players
        self.target_score: int = target_score
        self.dice_pool: DicePool = DicePool(num_dice)
        self.current_round: int = 0
        self.game_running = True

    def run(self):
        pass # main game loop, manage turns and rounds, do a for player in players for each turn, while game_running for rounds

    def init_game(self):
        pass # print hello message or something, setup vars/values if you need to, can remove this if useless

    def end_game(self):
        pass # same as init game, print goodbye message, final scores, determine winner? again, if unnecessary just remove it