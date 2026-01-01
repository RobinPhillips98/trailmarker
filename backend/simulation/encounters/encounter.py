from ..creatures.creature import Creature
from ..creatures.enemy import Enemy
from ..creatures.player import Player


class Encounter:
    def __init__(self, players: list[Player], enemies: list[Enemy]):
        self.players: list[Player] = players
        self.enemies: list[Enemy] = enemies
        self.creatures: list[Creature] = self.players + self.enemies

        for creature in self.creatures:
            creature.roll_initiative()
        
        self.creatures.sort(key=lambda creature: creature.initiative, reverse=True)

    def run_encounter(self) -> str:
        rounds = 0
        while True:
            self.run_round()
            rounds += 1
            if not self.players:
                winner = "enemies"
                break
            if not self.enemies:
                winner = "players"
                break
        
        print(f"{winner.capitalize()} won in {rounds} rounds!")
        return winner
    
    def run_round(self):
        # Already sorted by initiative
        for creature in self.creatures:
            if creature.is_dead:
                self.remove_creature(creature)
            else:
                creature.take_turn(self.players, self.enemies)

    def remove_creature(self, creature: Creature):
        # print(f"Removing {creature} from encounter")
        if creature.team == 1:
            self.players.remove(creature)
        elif creature.team == 2:
            self.enemies.remove(creature)

        self.creatures.remove(creature)

