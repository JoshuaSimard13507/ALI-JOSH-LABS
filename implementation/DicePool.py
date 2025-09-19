from Die import Die
class DicePool:

    def __init__(self, length: int = 6):
        self.dice: list[Die] = [Die() for _ in range(length)]
        self.remaining_dice = length

    def roll(self):
        for i in range(self.remaining_dice):
            self.dice[i].roll()
        return self.remaining_dice[:self.remaining_dice]

    def reset(self):
        self.remaining_dice = len(self.dice)

    def get_dice(self):
        return self.dice[:self.remaining_dice]