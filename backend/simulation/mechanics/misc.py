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


def calculate_dos(roll: int, result: int, difficulty: int) -> int:
    degree_of_success = 0
    if result >= difficulty + 10:
        degree_of_success = Degree.CRITICAL_SUCCESS
    elif result >= difficulty:
        degree_of_success = Degree.SUCCESS
    elif result <= difficulty - 10:
        degree_of_success = Degree.CRITICAL_FAILURE
    else:
        degree_of_success = Degree.FAILURE

    if roll == 20 and degree_of_success < Degree.CRITICAL_SUCCESS:
        degree_of_success += 1
    elif roll == 1 and degree_of_success > Degree.CRITICAL_FAILURE:
        degree_of_success -= 1

    return degree_of_success


# Initializing some common dice so other modules can import them
d100 = Die(100)
d20 = Die(20)
d12 = Die(12)
d10 = Die(10)
d8 = Die(8)
d6 = Die(6)
d4 = Die(4)

# TODO: Conditions
