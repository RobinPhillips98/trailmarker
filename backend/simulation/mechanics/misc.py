"""Defines some miscellaneous functions used for rolling dice and calculating
degrees of success."""

import random
from enum import IntEnum


class Die:
    """Simple class representing a playing die with a set number of faces."""

    def __init__(self, num_sides: int):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


class Degree(IntEnum):
    """IntEnum representing the degrees of success from Pathfinder 2E."""

    CRITICAL_FAILURE = 0
    FAILURE = 1
    SUCCESS = 2
    CRITICAL_SUCCESS = 3


def calculate_dos(roll: int, result: int, difficulty: int) -> int:
    """Uses the given arguments to calculate the degree of success.

    Args:
        roll (int): The number rolled on the die
        result (int): The total result of the check
        difficulty (int): The target difficulty class to meet.

    Returns:
        int: A number from 0 to 3 representing the degree of success
    """
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
