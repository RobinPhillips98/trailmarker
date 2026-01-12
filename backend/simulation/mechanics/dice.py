import random


class Die:
    def __init__(self, num_sides: int):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


# Initializing some common dice so other modules can import them
d100 = Die(100)
d20 = Die(20)
d12 = Die(12)
d10 = Die(10)
d8 = Die(8)
d6 = Die(6)
d4 = Die(4)
