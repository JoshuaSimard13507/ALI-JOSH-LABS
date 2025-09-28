import random
import time

class Die:
    """Represents a single six-sided die.


    Provides functionality to roll the die and store its current value.


    Attributes:
    value (int): The current face value of the die (1-6).
    """
    def __init__(self, value: int = 1):
        """Initialize a new die with value 1 by default."""
        self.value: int = value

        # Ensure randomness
        random.seed(time.time())

    def roll(self) -> int:
        """Roll the die to produce a new value between 1 and 6.


        Uses Python's ``random.randint`` to assign a face.


        :return: The rolled integer value.
        :rtype: int
        """
        self.value = random.randint(1, 6)
        return self.value


class DicePool:
    """Represents the collection of dice currently available to roll.


    Attributes:
    length (int): Total number of dice in the pool.
    remaining_dice (int): Number of dice still available this turn.
    """
    def __init__(self, length: int = 6):
        """Initialize a new dice pool.


        :param length: Number of dice in the pool (default 6).
        :type length: int
        """
        self.dice: list[Die] = [Die() for _ in range(length)]
        self.remaining_dice: int = length

    def roll(self) -> list[Die]:
        """Roll the available dice in the pool.


        Only the remaining dice are rolled. Updates their values in place.


        :return: List of ``Die`` objects representing the rolled dice.
        :rtype: list[Die]
        """
        for i in range(self.remaining_dice):
            self.dice[i].roll()
        return self.dice[:self.remaining_dice]

    def reset(self) -> None:
        """Reset the pool so all dice are available again."""
        self.remaining_dice = len(self.dice)
