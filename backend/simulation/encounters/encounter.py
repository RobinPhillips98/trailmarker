from ..creatures.creature import Creature
from ..creatures.enemy import Enemy
from ..creatures.player import Player


class Encounter:
    def __init__(
        self, players: list[Player], enemies: list[Enemy], simulation=None
    ):
        self.players: list[Player] = players
        self.enemies: list[Enemy] = enemies
        self.creatures: list[Creature] = self.players + self.enemies
        self.simulation = simulation
        self.winner = None

        for creature in self.creatures:
            creature.join_encounter(self)

        self.creatures.sort(
            key=lambda creature: creature.initiative, reverse=True
        )

    def check_winner(self):
        if not self.players:
            self.winner = "enemies"
            return True
        if not self.enemies:
            self.winner = "players"
            return True
        return False

    def run_encounter(self) -> str:
        self.log("Party:")
        for i in range(len(self.players)):
            self.log(f"{i + 1}. {self.players[i]}")

        self.log("Enemies:")
        for i in range(len(self.enemies)):
            self.log(f"{i + 1}. {self.enemies[i]}")
        self.log()

        self.log("Initiative order: ")
        for i in range(len(self.creatures)):
            self.log(f"{i + 1}. {self.creatures[i]}")
        self.log()

        print("Running encounter...")
        rounds = 0
        while not self.check_winner():
            rounds += 1
            self.log(f"Round {rounds}:")
            self.run_round()
            self.log()

        self.log(f"{self.winner.capitalize()} won in {rounds} rounds!")
        if self.simulation:
            self.simulation.rounds = rounds
        return self.winner

    def run_round(self):
        # Already sorted by initiative
        for creature in self.creatures:
            if self.check_winner():
                return
            creature.take_turn()

    def remove_creature(self, creature: Creature):
        if creature.team == 1:
            self.players.remove(creature)
        elif creature.team == 2:
            self.enemies.remove(creature)

        self.creatures.remove(creature)

    def log(self, message: str = ""):
        if self.simulation:
            self.simulation.log(message)
        else:
            print(message)
