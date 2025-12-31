def get_test_creature():
    return {
        "name": "Test Creature",
        "level": 3,
        "perception": 5,
        "skills": {
            "athletics": 4,
        },
        "attribute_modifiers": {
            "strength": 5,
            "constitution": 3,
            "dexterity": 2,
            "intelligence": 1,
            "wisdom": -1,
            "charisma": 0,
        },
        "defenses": {
            "armor_class": 12,
            "saves": {
                "fortitude": 4,
                "reflex": 3,
                "will": 2,
            },
        },
        "max_hit_points": 10,
        "speed": 25,
    }


def get_test_player():
    return {
        "id": 1,
        "name": "Valeros",
        "level": 1,
        "perception": 5,
        "skills": {
            "acrobatics": 5,
            "arcana": 1,
            "athletics": 7,
            "crafting": 4,
            "deception": 0,
            "diplomacy": 3,
            "intimidation": 3,
            "lore": 4,
            "medicine": 0,
            "nature": 0,
            "occultism": 1,
            "performance": 0,
            "religion": 0,
            "society": 1,
            "stealth": 2,
            "survival": 3,
            "thievery": 2,
        },
        "attribute_modifiers": {
            "strength": 4,
            "constitution": 2,
            "dexterity": 2,
            "intelligence": 1,
            "wisdom": 0,
            "charisma": 0,
        },
        "defenses": {
            "armor_class": 18,
            "saves": {"fortitude": 7, "reflex": 7, "will": 3},
        },
        "max_hit_points": 24,
        "speed": 25,
        "actions": {
            "attacks": [
                {
                    "name": "Longsword",
                    "attackBonus": 9,
                    "damage": "1d8+4",
                    "damageType": "slashing",
                },
                {
                    "name": "Dagger",
                    "attackBonus": 9,
                    "damage": "1d4+4",
                    "damageType": "piercing",
                },
                {
                    "name": "Shortbow",
                    "attackBonus": 7,
                    "damage": "1d6",
                    "damageType": "piercing",
                },
            ]
        },
        "user_id": 1,
        "player": "Robin",
        "xp": 0,
        "ancestry": "human",
        "background": "farmhand",
        "class": "fighter",
    }


def get_test_enemy():
    return {
        "id": 25,
        "name": "Goblin Warrior",
        "level": -1,
        "perception": 2,
        "skills": {
            "acrobatics": 5,
            "arcana": None,
            "athletics": 2,
            "crafting": None,
            "deception": None,
            "diplomacy": None,
            "intimidation": None,
            "lore": None,
            "medicine": None,
            "nature": 1,
            "occultism": None,
            "performance": None,
            "religion": None,
            "society": None,
            "stealth": 5,
            "survival": None,
            "thievery": None,
        },
        "attribute_modifiers": {
            "strength": 0,
            "constitution": 1,
            "dexterity": 3,
            "intelligence": 0,
            "wisdom": -1,
            "charisma": 1,
        },
        "defenses": {
            "armor_class": 16,
            "saves": {"fortitude": 5, "reflex": 7, "will": 3},
        },
        "max_hit_points": 6,
        "speed": 25,
        "actions": {
            "attacks": [
                {
                    "name": "Shortsword",
                    "attackBonus": 7,
                    "damage": "1d6",
                    "damageType": "slashing",
                },
                {
                    "name": "Shortbow",
                    "attackBonus": 7,
                    "damage": "1d6",
                    "damageType": "piercing",
                },
            ]
        },
        "traits": ["common", "sm", "goblin", "humanoid"],
        "immunities": [],
    }
