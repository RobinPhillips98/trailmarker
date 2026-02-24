import random
from enum import IntEnum


class Die:
    def __init__(self, num_sides: int):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


class Degree(IntEnum):
    CRITICAL_FAILURE = 0
    FAILURE = 1
    SUCCESS = 2
    CRITICAL_SUCCESS = 3


# Initializing some common dice so other modules can import them
d100 = Die(100)
d20 = Die(20)
d12 = Die(12)
d10 = Die(10)
d8 = Die(8)
d6 = Die(6)
d4 = Die(4)

# TODO: Conditions
