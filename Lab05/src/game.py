import time
import random
from .player import Player
from .dice import DicePool, Die
from collections import Counter
from itertools import cycle
import math



class Game:
    def __init__(self, players: list[Player] = (Player("P1"), Player("BOT", is_ai=True)),
                 target_score: int = 10000, num_dice: int = 6, hot_dice_enabled: bool = True):
        self.players: list[Player] = players
        self.target_score: int = target_score
        self.dice_pool: DicePool = DicePool(num_dice)
        self.current_round: int = 0
        self.hot_dice_enabled: bool = hot_dice_enabled
        self.game_running: bool = True
        self.tentative_score: int = 0

    def run(self) -> bool:
        winner: Player | None = None

        print("==== New Farkle Match ====")
        print("Type 'q' to quit")

        for player in cycle(self.players):
            self.play_turn(player)

            if not self.game_running:
                return False

            if player.points >= self.target_score:
                winner = player
                break

        for player in self.players:
            player.lifetime_score += player.points if not player.is_ai else 0
            if player is winner:
                player.win()
                print(f"{player.username} wins!")
            else:
                player.lose()
        return True

    def get_player_choice(self, player: Player) -> str:
        if player.is_ai:
            time.sleep(random.uniform(.5, 1.5))
            if self.dice_pool.remaining_dice != 6 and (self.tentative_score >= 500 or self.dice_pool.remaining_dice <= 3):
                choice = "b"
            else:
                choice = "r"
            print(f"AI decision → {'Bank' if choice == 'b' else 'Roll again'}")
            return choice

        while True:
            choice = input(f"{self.dice_pool.remaining_dice} dice left. Bank points (b) or roll again (r)? ").strip().lower()
            if choice in ("b", "r", "q"):
                return choice

    def record_roll(self, score: int, used: int):
        self.tentative_score += score
        self.dice_pool.remaining_dice -= used
        print(f"Scored {score}  |  Tentative this turn: {self.tentative_score}")

        if self.hot_dice_enabled and self.dice_pool.remaining_dice == 0:
            print("Hot Dice! All dice scored. You may roll all six again.")
            self.dice_pool.reset()

    def play_turn(self, player: Player):
        self.tentative_score = 0
        self.dice_pool.reset()

        print(f"\n-- {player.username}'s turn (Total: {player.points}) --")
        while True:
            rolled: list[Die] = self.dice_pool.roll()
            print(f"Rolled: {[d.value for d in rolled]}")
            score, used = self.calculate_score(rolled)

            if score == 0:
                self.tentative_score = 0
                print("Farkle! No scoring dice.")
                break

            self.record_roll(score, used)

            if self.dice_pool.remaining_dice == 0:
                print("All dice scored; Hot Dice is off → banking automatically.")
                break

            choice = self.get_player_choice(player)
            if choice == "b":
                break
            elif choice == "q":
                self.game_running = False
                return

        player.bank_points(self.tentative_score)

    def calculate_score(selection: list[Die]) -> tuple[int, int]:
        """Compute the score for a set of dice according to this variant.

        The algorithm:
          1) Score triples or higher first (with 4/5/6-kind multipliers).
          2) Score leftover single 1s and 5s.
          3) Track how many dice were *consumed* in scoring.

        :param selection: Dice to score (typically the full roll).
        :type selection: list[Die]
        :return: A pair ``(score, used)``, where ``score`` is the awarded points
                 and ``used`` is the number of dice consumed by scoring.
        :rtype: tuple[int, int]
        """
        counts = Counter(d.value for d in selection)
        score = 0
        used = 0

        for face in range(1, 7):
            n = counts[face]
            if n >= 3:
                base = 1000 if face == 1 else face * 100
                # 3 -> x1, 4 -> x2, 5 -> x3, 6 -> x4
                mult = (n - 2)
                score += base * mult
                used += n
                counts[face] = 0  # consumed
                print(f"Found {face} rolled {n} times → adding +{base * mult}")

        if counts[1] > 0:
            base = 100
            score += base * counts[1]
            used += counts[1]
            print(f"Found 1 rolled {counts[1]} times → adding +{base * counts[1]}")
        if counts[5] > 0:
            base = 50
            score += base * counts[5]
            used += counts[5]
            print(f"Found 5 rolled {counts[5]} times → adding +{base * counts[5]}")

        return score, used

