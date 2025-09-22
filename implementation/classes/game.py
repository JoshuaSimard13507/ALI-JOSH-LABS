from .player import Player
from .calculate_score import CalculateScore
from .dice import DicePool, Die

class Game:
    def __init__(self, calculate_score = CalculateScore.doubling,
                 players: list[Player] = (Player("P1"), Player("BOT", is_ai=True)), target_score: int = 10000,
                 num_dice: int = 6, hot_dice_enabled: bool = True):
        self.calculate_score = calculate_score
        self.players: list[Player] = players
        self.target_score: int = target_score
        self.dice_pool: DicePool = DicePool(num_dice)
        self.current_round: int = 0
        self.hot_dice_enabled: bool = hot_dice_enabled
        self.game_running: bool = True

    def run(self):
        # main game loop, manage turns and rounds, do a for player in players for each turn, while game_running for rounds
        current_player: int = 0
        num_players = len(self.players)
        winner: Player | None = None

        print("=== New Farkle Match ===")

        while self.game_running:
            player: Player = self.players[current_player]
            self.play_turn(player)

            current_player += 1
            if player.points >= self.target_score:
                winner = player
                self.game_running = False
            elif current_player == num_players: # no winner, loop back to first player after last player is reached
                current_player = 0
        for player in self.players:
            player.lifetime_score += player.points
            if player is winner:
                player.win()
                print(f"{player.username} wins!")
            else:
                player.lose()

    def play_turn(self, player: Player):
        tentative_score: int = 0
        continue_turn: bool = True

        self.dice_pool.reset()
        print(f"\n-- {player.username}'s turn (Total: {player.points}) --")
        while continue_turn:
            rolled: list[Die] = self.dice_pool.roll()
            print(f"Rolled: {[d.value for d in rolled]}")
            score, used = self.calculate_score(rolled)

            # End turn if farkled
            if score == 0:
                continue_turn = False
                tentative_score = 0
                print("Farkle! No scoring dice.")

            else: # Continue otherwise

                # Update score
                tentative_score += score
                self.dice_pool.remaining_dice -= used
                print(f"Scored {score}  |  Tentative this turn: {tentative_score}")

                # Reset dice pool if Hot Dice is allowed
                if self.hot_dice_enabled and self.dice_pool.remaining_dice == 0:
                    print("Hot Dice! All dice scored. You may roll all six again.")
                    self.dice_pool.reset()

                # Get player decision
                if player.is_ai:
                    if self.dice_pool.remaining_dice != 6 and (tentative_score >= 500 or self.dice_pool.remaining_dice <= 3):
                        chose_bank = True
                    else:
                        chose_bank = False
                    print(f"AI decision → {'Bank' if chose_bank else 'Roll again'}")
                else:
                    while True:
                        choice = input(f"{self.dice_pool.remaining_dice} dice left. Bank points (b) or roll again (r)? ").strip().lower()
                        if choice == "b":
                            chose_bank = True
                            break
                        elif choice == "r":
                            chose_bank = False
                            break

                # Player chose to bank, end turn and bank points
                if chose_bank:
                    continue_turn = False

                # If all dice were used, end the turn automatically.
                # (When Hot Dice is ON, select_dice() already reset the pool, so this won't trigger.)
                if self.dice_pool.remaining_dice == 0:
                    print("All dice scored; Hot Dice is off → banking automatically.")
                    player.bank_points(tentative_score)
                    continue_turn = False

        # Turn ended, bank accumulated points
        player.bank_points(tentative_score)

    def init_game(self):
        pass # print hello message or something, setup vars/values if you need to, can remove this if useless

    def end_game(self):
        pass # same as init game, print goodbye message, final scores, determine winner? again, if unnecessary just remove it
