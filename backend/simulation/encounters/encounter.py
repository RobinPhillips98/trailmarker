from ..creatures.creature import Creature
from ..creatures.enemy import Enemy
from ..creatures.player import Player


class Encounter:
    def __init__(self, players: list[Player], enemies: list[Enemy]):
        self.players: list[Player] = players
        self.enemies: list[Enemy] = enemies
        self.creatures: list[Creature] = self.players + self.enemies
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
        print("Party: ")
        for player in self.players:
            print(f"* {player.long_description()}")

        print("Enemies:")
        for enemy in self.enemies:
            print(f"* {enemy.long_description()}")
        print()

        print("Initiative order: ")
        for i in range(len(self.creatures)):
            print(f"{i + 1}. {self.creatures[i]}")
        print()

        print("Running encounter...")
        rounds = 0
        while not self.check_winner():
            rounds += 1
            print(f"Round {rounds}:")
            self.run_round()
            print()

        print(f"{self.winner.capitalize()} won in {rounds} rounds!")
        return self.winner

    def run_round(self):
        # Already sorted by initiative
        for creature in self.creatures:
            if self.check_winner():
                return
            creature.take_turn()

    def remove_creature(self, creature: Creature):
        # print(f"Removing {creature} from encounter")
        if creature.team == 1:
            self.players.remove(creature)
        elif creature.team == 2:
            self.enemies.remove(creature)

        self.creatures.remove(creature)
