from ..simulation.creatures.creature import Creature
from ..simulation.creatures.enemy import Enemy
from ..simulation.creatures.player import Player
from .sample_data import test_creature, test_enemy, test_player


class TestCreature:
    creature = Creature(test_creature)

    def test_basic_stats(self):
        assert self.creature.name == "Test Creature"
        assert self.creature.level == 3
        assert self.creature.perception == 5
        assert self.creature.max_hit_points == 10
        assert self.creature.hit_points == self.creature.max_hit_points
        assert self.creature.armor_class == 12
        assert self.creature.speed == 25
        assert self.creature.initiative == 0
        assert not self.creature.is_dead
        assert self.creature.attacks is None
        assert self.creature.team is None
        assert self.creature.encounter is None

    def test_attribute_modifiers(self):
        assert self.creature.strength == 5
        assert self.creature.constitution == 3
        assert self.creature.dexterity == 2
        assert self.creature.intelligence == 1
        assert self.creature.wisdom == -1
        assert self.creature.charisma == 0

    def test_skills(self):
        assert self.creature.acrobatics == self.creature.dexterity
        assert self.creature.arcana == self.creature.intelligence
        assert self.creature.athletics == 4
        assert self.creature.crafting == self.creature.intelligence
        assert self.creature.deception == self.creature.charisma
        assert self.creature.diplomacy == self.creature.charisma
        assert self.creature.intimidation == self.creature.charisma
        assert self.creature.lore == self.creature.intelligence
        assert self.creature.medicine == self.creature.wisdom
        assert self.creature.nature == self.creature.wisdom
        assert self.creature.occultism == self.creature.intelligence
        assert self.creature.performance == self.creature.charisma
        assert self.creature.religion == self.creature.wisdom
        assert self.creature.society == self.creature.intelligence
        assert self.creature.stealth == self.creature.dexterity
        assert self.creature.survival == self.creature.wisdom
        assert self.creature.thievery == self.creature.dexterity

    def test_saves(self):
        assert self.creature.fortitude == 4
        assert self.creature.reflex == 3
        assert self.creature.will == 2


class TestPlayer:
    player = Player(test_player)

    def test_basic_stats(self):
        assert self.player.name == "Valeros"
        assert self.player.level == 1
        assert self.player.perception == 5
        assert self.player.max_hit_points == 24
        assert self.player.hit_points == self.player.max_hit_points
        assert self.player.armor_class == 18
        assert self.player.speed == 25
        assert self.player.initiative == 0
        assert not self.player.is_dead
        assert self.player.team == 1
        assert self.player.ancestry == "human"
        assert self.player.class_ == "fighter"
        assert self.player.encounter is None

    def test_attribute_modifiers(self):
        assert self.player.strength == 4
        assert self.player.constitution == 2
        assert self.player.dexterity == 2
        assert self.player.intelligence == 1
        assert self.player.wisdom == 0
        assert self.player.charisma == 0

    def test_skills(self):
        assert self.player.acrobatics == 5
        assert self.player.arcana == 1
        assert self.player.athletics == 7
        assert self.player.crafting == 4
        assert self.player.deception == 0
        assert self.player.diplomacy == 3
        assert self.player.intimidation == 3
        assert self.player.lore == 4
        assert self.player.medicine == 0
        assert self.player.nature == 0
        assert self.player.occultism == 1
        assert self.player.performance == 0
        assert self.player.religion == 0
        assert self.player.society == 1
        assert self.player.stealth == 2
        assert self.player.survival == 3
        assert self.player.thievery == 2

    def test_saves(self):
        assert self.player.fortitude == 7
        assert self.player.reflex == 7
        assert self.player.will == 3

    def test_attacks(self):
        longsword = self.player.attacks[0]
        assert longsword.name == "Longsword"
        assert longsword.attack_bonus == 9
        assert longsword.num_dice == 1
        assert longsword.die_size == 8
        assert longsword.damage_bonus == 4
        assert longsword.damage_type == "slashing"

        dagger = self.player.attacks[1]
        assert dagger.name == "Dagger"
        assert dagger.attack_bonus == 9
        assert dagger.num_dice == 1
        assert dagger.die_size == 4
        assert dagger.damage_bonus == 4
        assert dagger.damage_type == "piercing"

        shortbow = self.player.attacks[2]
        assert shortbow.name == "Shortbow"
        assert shortbow.attack_bonus == 7
        assert shortbow.num_dice == 1
        assert shortbow.die_size == 6
        assert shortbow.damage_type == "piercing"


class TestEnemy:
    enemy = Enemy(test_enemy)

    def test_basic_stats(self):
        assert self.enemy.name == "Goblin Warrior"
        assert self.enemy.level == -1
        assert self.enemy.perception == 2
        assert self.enemy.max_hit_points == 6
        assert self.enemy.hit_points == self.enemy.max_hit_points
        assert self.enemy.armor_class == 16
        assert self.enemy.speed == 25
        assert self.enemy.initiative == 0
        assert not self.enemy.is_dead
        assert self.enemy.team == 2
        assert self.enemy.encounter is None

    def test_attribute_modifiers(self):
        assert self.enemy.strength == 0
        assert self.enemy.constitution == 1
        assert self.enemy.dexterity == 3
        assert self.enemy.intelligence == 0
        assert self.enemy.wisdom == -1
        assert self.enemy.charisma == 1

    def test_skills(self):
        assert self.enemy.acrobatics == 5
        assert self.enemy.arcana == self.enemy.intelligence
        assert self.enemy.athletics == 2
        assert self.enemy.crafting == self.enemy.intelligence
        assert self.enemy.deception == self.enemy.charisma
        assert self.enemy.diplomacy == self.enemy.charisma
        assert self.enemy.intimidation == self.enemy.charisma
        assert self.enemy.lore is None
        assert self.enemy.medicine == self.enemy.wisdom
        assert self.enemy.nature == 1
        assert self.enemy.occultism == self.enemy.intelligence
        assert self.enemy.performance == self.enemy.charisma
        assert self.enemy.religion == self.enemy.wisdom
        assert self.enemy.society == self.enemy.intelligence
        assert self.enemy.stealth == 5
        assert self.enemy.survival == self.enemy.wisdom
        assert self.enemy.thievery == self.enemy.dexterity

    def test_saves(self):
        assert self.enemy.fortitude == 5
        assert self.enemy.reflex == 7
        assert self.enemy.will == 3

    def test_enemy_stats(self):
        assert self.enemy.traits == ["common", "sm", "goblin", "humanoid"]
        assert self.enemy.immunities == []

    def test_attacks(self):
        shortsword = self.enemy.attacks[0]
        assert shortsword.name == "Shortsword"
        assert shortsword.attack_bonus == 7
        assert shortsword.num_dice == 1
        assert shortsword.die_size == 6
        assert shortsword.damage_type == "slashing"

        shortbow = self.enemy.attacks[1]
        assert shortbow.name == "Shortbow"
        assert shortbow.attack_bonus == 7
        assert shortbow.num_dice == 1
        assert shortbow.die_size == 6
        assert shortbow.damage_type == "piercing"


class TestCreatureMethods:
    player = Player(test_player)
    enemy = Enemy(test_enemy)

    def test_initiative(self):
        assert self.player.initiative == 0
        assert self.enemy.initiative == 0

        self.player._roll_initiative()
        assert self.player.initiative > 0
        assert self.player.initiative <= 20 + self.player.perception

        self.enemy._roll_initiative()
        assert self.enemy.initiative > 0
        assert self.enemy.initiative <= 20 + self.player.perception

    def test_attack_and_damage(self):
        player_weapon = self.player.attacks[0]
        enemy_weapon = self.enemy.attacks[0]

        assert not self.player.is_dead
        assert not self.enemy.is_dead

        if self.player._attack(player_weapon, self.enemy):
            assert self.enemy.hit_points < self.enemy.max_hit_points
        else:
            assert self.enemy.hit_points == self.enemy.max_hit_points

        if self.enemy._attack(enemy_weapon, self.player):
            assert self.player.hit_points < self.player.max_hit_points
        else:
            assert self.player.hit_points == self.player.max_hit_points

        while not self.enemy.is_dead:
            prev_hp = self.enemy.hit_points
            if self.player._attack(player_weapon, self.enemy):
                assert self.enemy.hit_points < prev_hp

        assert self.enemy.is_dead
