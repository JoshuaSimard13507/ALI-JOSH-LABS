from Die import Die

class DicePool:

    def __init__(self):
        self.dice: list[Die] = [Die() for _ in range(6)]
        self.length = 6

    def roll(self, inp_length):
        for i in range(self.length):
            self.dice[i].roll()
        return self.dice[:inp_length]

    def get_remaining(self, inp_length):
        return self.dice[:inp_length]
    
    def get_dice(self):
        return self.dice
    
    def get_dice_raw(self, inp_length):
        return [d.value for d in self.dice[:inp_length]]