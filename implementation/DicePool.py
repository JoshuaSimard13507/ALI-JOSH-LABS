from Die import Die

class DicePool:

    def __init__(self, length: int = 6):
        self.dice: list[Die] = [Die() for _ in range(length)]
        self.length = length

    def roll(self):
        for i in range(self.length):
            self.dice[i].roll()
    
    def get_dice(self):
        return self.dice
    
    def get_dice_raw(self):
        return [d.value for d in self.dice]