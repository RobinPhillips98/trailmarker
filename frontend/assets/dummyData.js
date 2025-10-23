export const enemies = [
  {
    id: 1,
    name: "Animated Armor",
    level: 2,
    traits: ["common", "med", "construct", "mindless"],
    perception: 6,
    skills: {
      athletics: 9,
    },
    attributeModifiers: {
      str: 3,
      dex: -3,
      con: 4,
      int: -5,
      wis: 0,
      cha: -5,
    },
    defenses: {
      armorClass: 17,
      saves: {
        fortitude: 10,
        reflex: 3,
        will: 4,
      },
    },
    maxHitPoints: 20,
    immunities: ["vitality", "void"],
    speed: 20,
    actions: {
      attacks: {
        Longsword: {
          attackBonus: 11,
          damage: "1d8+4",
          damageType: "slashing",
        },
        Armored_Fist: {
          attackBonus: 9,
          damage: "1d6+4",
          damageType: "bludgeoning",
        },
      },
    },
  },
  {
    id: 2,
    name: "Cinder Rat",
    level: 3,
    traits: ["common", "sm", "elemental", "fire"],
    perception: 9,
    skills: {
      acrobatics: 10,
      stealth: 10,
      survival: 9,
    },
    attributeModifiers: {
      str: 2,
      dex: 3,
      con: 2,
      int: -4,
      wis: 2,
      cha: 0,
    },
    defenses: {
      armorClass: 18,
      saves: {
        fortitude: 9,
        reflex: 12,
        will: 6,
      },
    },
    maxHitPoints: 45,
    immunities: ["bleed", "fire", "poison", "sleep"],
    speed: 40,
    actions: {
      attacks: {
        Jaws: {
          attackBonus: 10,
          damage: "1d8+4",
          damageType: "fire",
        },
      },
    },
  },
  {
    id: 3,
    name: "Drow Warrior",
    level: 1,
    traits: ["common", "med", "chaotic", "drow", "elf", "evil", "humanoid"],
    perception: 6,
    skills: {
      acrobatics: 7,
      athletics: 5,
      intimidation: 3,
      stealth: 7,
    },
    attributeModifiers: {
      str: 2,
      dex: 4,
      con: 2,
      int: 0,
      wis: 1,
      cha: 0,
    },
    defenses: {
      armorClass: 18,
      saves: {
        fortitude: 7,
        reflex: 9,
        will: 4,
      },
    },
    maxHitPoints: 18,
    immunities: ["sleep"],
    speed: 30,
    actions: {
      attacks: {
        Rapier: {
          attackBonus: 9,
          damage: "1d6+2",
          damageType: "piercing",
        },
        Dagger: {
          attackBonus: 9,
          damage: "1d4+2",
          damageType: "piercing",
        },
        Hand_Crossbow: {
          attackBonus: 9,
          damage: "1d6+1",
          damageType: "piercing",
        },
      },
    },
  },
  {
    id: 4,
    name: "Horned Dragon (Juvenile)",
    level: 4,
    traits: ["common", "med", "amphibious", "dragon"],
    perception: 11,
    skills: {
      acrobatics: 8,
      arcana: 11,
      athletics: 12,
      deception: 9,
      diplomacy: 11,
      intimidation: 11,
      nature: 9,
      occultism: 12,
      society: 9,
      stealth: 10,
    },
    attributeModifiers: {
      str: 4,
      dex: 1,
      con: 3,
      int: 1,
      wis: 1,
      cha: 3,
    },
    defenses: {
      armorClass: 20,
      saves: {
        fortitude: 11,
        reflex: 11,
        will: 9,
      },
    },
    maxHitPoints: 60,
    immunities: ["sleep", "poison"],
    speed: 25,
    actions: {
      attacks: {
        Jaws: {
          attackBonus: 14,
          damage: "2d6+4",
          damageType: "piercing",
        },
        Claw: {
          attackBonus: 14,
          damage: "2d6+4",
          damageType: "slashing",
        },
        Tail: {
          attackBonus: 12,
          damage: "1d8+4",
          damageType: "bludgeoning",
        },
        Horn: {
          attackBonus: 12,
          damage: "1d12+4",
          damageType: "bludgeoning",
        },
      },
    },
  },
  {
    id: 5,
    name: "Kobold Warrior",
    level: -1,
    traits: ["common", "sm", "humanoid", "kobold"],
    perception: 3,
    skills: {
      acrobatics: 5,
      crafting: 2,
      stealth: 5,
    },
    attributeModifiers: {
      str: 1,
      dex: 3,
      con: 0,
      int: 0,
      wis: 1,
      cha: -1,
    },
    defenses: {
      armorClass: 16,
      saves: {
        fortitude: 4,
        reflex: 7,
        will: 3,
      },
    },
    maxHitPoints: 7,
    immunities: [],
    speed: 25,
    actions: {
      attacks: {
        Spear: {
          attackBonus: 5,
          damage: "1d6+1",
          damageType: "piercing",
        },
      },
    },
  },
  {
    id: 6,
    name: "Orc Scrapper",
    level: 0,
    traits: ["common", "med", "humanoid", "orc"],
    perception: 5,
    skills: {
      athletics: 5,
      intimidation: 2,
    },
    attributeModifiers: {
      str: 3,
      dex: 2,
      con: 2,
      int: 0,
      wis: 1,
      cha: 0,
    },
    defenses: {
      armorClass: 14,
      saves: {
        fortitude: 5,
        reflex: 4,
        will: 2,
      },
    },
    maxHitPoints: 18,
    immunities: [],
    speed: 25,
    actions: {
      attacks: {
        Battle_Axe: {
          attackBonus: 7,
          damage: "1d8+3",
          damageType: "piercing",
        },
        Fist: {
          attackBonus: 7,
          damage: "1d4+3",
          damageType: "bludgeoning",
        },
        Javelin: {
          attackBonus: 4,
          damage: "1d6+3",
          damageType: "piercing",
        },
      },
    },
  },
];
