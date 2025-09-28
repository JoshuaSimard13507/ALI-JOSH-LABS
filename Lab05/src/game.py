import time
import random
from .player import Player
from .dice import DicePool, Die
from collections import Counter
from itertools import cycle
import math



class Game:
    """Encapsulates one Farkle match between players.


    Attributes:
    players (list[Player]): List of participating players.
    target_score (int): Score required to win.
    hot_dice_enabled (bool): Whether hot dice rule is on.
    num_dice (int): Number of dice used.
    dice_pool (DicePool): Pool object tracking available dice.
    tentative_score (int): Points accumulated in current turn.
    """
    def __init__(self, players: list[Player] = (Player("P1"), Player("BOT", is_ai=True)),
                 target_score: int = 10000, num_dice: int = 6, hot_dice_enabled: bool = True):
        """Initialize the game state with given players and settings."""
        self.players: list[Player] = players
        self.target_score: int = target_score
        self.dice_pool: DicePool = DicePool(num_dice)
        self.current_round: int = 0
        self.hot_dice_enabled: bool = hot_dice_enabled
        self.game_running: bool = True
        self.tentative_score: int = 0

    def run(self) -> bool:
        """Run the game until one player reaches the target score.


        Evaluate winner at each loop and end game once winner is found, then announce winner.
        Update player win and lifetime score data. Return True.
        If game ends prematurely (i.e. player quits), return False.


        :return: True when game completes.
        :rtype: bool
        """
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
        """Decide whether the active player banks or rolls again.

        Behavior:
          1) If the player is AI: wait a short random delay and choose:
             - ``'b'`` (bank) when this is *not* a fresh 6-dice roll **and**
               either ``tentative_score >= 500`` or ``remaining_dice <= 3``;
             - otherwise choose ``'r'`` (roll again). Prints the decision.
          2) If the player is human: prompt until one of ``'b'``, ``'r'``,
             or ``'q'`` (quit) is entered.

        :param player: The currently active player whose decision is required.
        :type player: Player
        :return: One of ``'b'`` to bank, ``'r'`` to roll again, or ``'q'`` to quit.
        :rtype: str
        """
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
        """Apply a roll result to the game state.


        Adds score to tentative total, reduces remaining dice, resets if hot dice.


        :param score: Points scored this roll.
        :type score: int
        :param used: Dice consumed this roll.
        :type used: int
        """
        self.tentative_score += score
        self.dice_pool.remaining_dice -= used
        print(f"Scored {score}  |  Tentative this turn: {self.tentative_score}")

        if self.hot_dice_enabled and self.dice_pool.remaining_dice == 0:
            print("Hot Dice! All dice scored. You may roll all six again.")
            self.dice_pool.reset()

    def play_turn(self, player: Player):
        """Play one complete turn for ``player``, updating scores and game state.

        The algorithm:
          1) Reset the turn state: set ``tentative_score = 0`` and
             ``dice_pool`` to all dice available.
          2) Roll the remaining dice and compute ``(score, used)`` with
             :meth:`calculate_score`.
          3) If ``score == 0``: this is a *farkle* — clear the tentative score,
             announce it, and end the turn.
          4) Otherwise, call :meth:`record_roll(score, used)` to add points and
             reduce ``remaining_dice``. If **Hot Dice** is enabled and all dice
             scored, the pool is automatically reset inside ``record_roll``.
             If Hot Dice is **disabled** and no dice remain, auto-bank and end.
          5) If dice remain, ask :meth:`get_player_choice`:
             - ``'b'`` → end the loop and bank the tentative score;
             - ``'r'`` → continue rolling the remaining dice;
             - ``'q'`` → set ``game_running = False`` and return immediately.
          6) After the loop exits normally, add ``tentative_score`` to the
             player's total via :meth:`Player.bank_points`.

        :param player: The player whose turn is being executed.
        :type player: Player
        :return: ``None``. Side effects: prints to console, updates
                 ``tentative_score``, the player's points, and possibly
                 ``game_running``.
        :rtype: None
        """
        show_continue = player.is_ai
        self.tentative_score = 0
        self.dice_pool.reset()

        print(f"\n-- {player.username}'s turn (Total: {player.points}) --")
        while True:
            rolled: list[Die] = self.dice_pool.roll()
            print(f"Rolled: {[d.value for d in rolled]}")
            score, used = self.calculate_score(rolled)

            if score == 0:
                self.tentative_score = 0
                show_continue = True
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

        input("Press any key to continue. ") if show_continue else None
        player.bank_points(self.tentative_score)

    def calculate_score(self, selection: list[Die]) -> tuple[int, int]:
        """Compute the score for a set of dice according to this variant.


        The algorithm:
        1) Score triples or higher first (with 4/5/6-kind multipliers).
        2) Score leftover single 1s and 5s.
        3) Track how many dice were *consumed* in scoring.


        :param dice: Dice to score (typically the full roll).
        :type dice: list[Die]
        :return: A pair ``(score, used)``.
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
