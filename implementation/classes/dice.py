import random
import time

class Die:
    """A six-sided die.

    Attributes
    ----------
    value : int
        The current face value (1–6). Initialized by rolling once.
    """
    def __init__(self, value: int = 1):
        self.value: int = value

        # Ensure randomness
        random.seed(time.time())

    def roll(self) -> int:
        """Roll the die and update its face value.

        :return: The new face value in [1, 6].
        :rtype: int
        """
        self.value = random.randint(1, 6)
        return self.value


class DicePool:
    """A pool of up to six dice with remaining-dice tracking.

    Attributes
    ----------
    dice : list[Die]
        The managed dice (default: six dice).
    remaining_dice : int
        How many dice are available to roll this turn (1–6).
    """
    def __init__(self, length: int = 6):
        self.dice: list[Die] = [Die() for _ in range(length)]
        self.remaining_dice: int = length

    def roll(self) -> list[Die]:
        """Roll `count` dice (defaults to current ``remaining_dice``) in-place.

        The first `count` dice in the pool are rolled and returned.

        :return: The list of dice objects that were rolled (first `count` dice).
        :rtype: list[Die]
        """
        for i in range(self.remaining_dice):
            self.dice[i].roll()
        # print(f"debug dice: {[die.value for die in self.dice]} | rem: {self.remaining_dice}")
        return self.dice[:self.remaining_dice]

    def reset(self) -> None:
        """Reset the pool to allow rolling all six dice again.

        Typically used when Hot Dice triggers (all dice scored).
        """
        self.remaining_dice = len(self.dice)
