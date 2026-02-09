import { Button, Card, Descriptions, Divider, List } from "antd";
import { useNavigate } from "react-router-dom";

import { splitCamelCase, toTitleCase } from "../../services/helpers";

/**
 * A component to display information about a given character
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @param {function} props.deleteCharacter The function to delete the displayed character
 * @returns {JSX.element}
 */
export default function CharacterDisplay({ character, deleteCharacter }) {
  const navigate = useNavigate();

  function handleDelete() {
    deleteCharacter(character);
  }

  function handleEdit() {
    navigate("/characters/create", {
      state: { editing: true, savedCharacter: character },
    });
  }

  const items = [
    {
      key: "name",
      label: "Name",
      children: toTitleCase(character.name),
      span: 2,
    },
    {
      key: "player",
      label: "Player",
      children: character.player,
    },

    {
      key: "ancestry",
      label: "Ancestry",
      children: toTitleCase(character.ancestry),
    },
    {
      key: "background",
      label: "Background",
      children: toTitleCase(character.background),
    },
    {
      key: "class",
      label: "Class",
      children: toTitleCase(character.class),
    },
    {
      key: "level",
      label: "Level",
      children: character.level,
    },
    {
      key: "xp",
      label: "XP",
      children: character.xp,
    },
    {
      key: "speed",
      label: "Speed",
      children: character.speed,
    },
    {
      key: "hit_points",
      label: "Maximum Hit Points",
      children: character.max_hit_points,
    },
    {
      key: "perception",
      label: "Perception",
      children: character.perception,
    },
    {
      key: "armor_class",
      label: "Armor Class",
      children: character.defenses.armor_class,
    },
    {
      key: "spell_attack_bonus",
      label: "Spell Attack Bonus",
      children: character.spell_attack_bonus || "None",
    },
    {
      key: "spell_dc",
      label: "Spell DC",
      children: character.spell_dc || "None",
    },
    {
      key: "saves",
      label: "Saves",
      children: (
        <List size="small">
          {Object.keys(character.defenses.saves).map((save) => {
            return (
              <List.Item>
                {toTitleCase(save)}: {character.defenses.saves[save]}
              </List.Item>
            );
          })}
        </List>
      ),
    },
    {
      key: "attributes",
      label: "Attribute Modifiers",
      children: (
        <List
          size="small"
          grid={{ gutter: 16, column: 3 }}
          dataSource={Object.keys(character.attribute_modifiers)}
          renderItem={(attribute) => (
            <List.Item>
              {toTitleCase(attribute)}:{" "}
              {character.attribute_modifiers[attribute]}
            </List.Item>
          )}
        />
      ),
      span: 3,
    },
    {
      key: "skills",
      label: "Skills",
      children: (
        <List
          size="small"
          grid={{ gutter: 16, column: 3 }}
          dataSource={Object.keys(character.skills)}
          renderItem={(skill) => (
            <List.Item>
              {toTitleCase(skill)}: {character.skills[skill]}
            </List.Item>
          )}
        />
      ),
      span: 3,
    },
    {
      key: "attacks",
      label: "Attacks",
      children: (
        <List
          size="small"
          grid={{ gutter: 16, column: 3 }}
          dataSource={character.actions?.attacks || []}
          renderItem={(attack) => (
            <List.Item key={attack.name}>
              <Card title={attack.name} style={{ maxWidth: 300 }}>
                <List
                  size="small"
                  dataSource={[
                    ["Attack Bonus", attack.attackBonus],
                    ["Damage", attack.damage],
                    ["Damage Type", toTitleCase(attack.damageType)],
                  ]}
                  renderItem={([label, value]) => (
                    <List.Item key={label}>
                      <strong>{label}</strong>: {value}
                    </List.Item>
                  )}
                />
              </Card>
            </List.Item>
          )}
        />
      ),
      span: 3,
    },
    {
      key: "spells",
      label: "Spells",
      children: (
        <List
          size="small"
          grid={{ gutter: 16, column: 3 }}
          dataSource={character.actions?.spells || []}
          renderItem={(spell) => (
            <List.Item key={spell.name}>
              <Card title={toTitleCase(spell.name)} style={{ maxWidth: 360 }}>
                <List
                  size="small"
                  dataSource={[
                    ["Slots", spell.slots],
                    ["Level", spell.level > 0 ? spell.level : "Cantrip"],
                    ["Damage Roll", spell.damage_roll],
                    ["Damage Type", toTitleCase(spell.damage_type)],
                    ["Range", spell.range],
                    ["Target", spell.target],
                    ["Actions", spell.actions],
                    ["Saving Throw", toTitleCase(spell.save)],
                    ...(spell.area && typeof spell.area === "object"
                      ? Object.keys(spell.area).map((key) => [
                          `Area ${toTitleCase(splitCamelCase(key))}`,
                          spell.area[key],
                        ])
                      : []),
                  ]}
                  renderItem={([label, value]) => (
                    <List.Item key={label}>
                      <strong>{label}:</strong> {value}
                    </List.Item>
                  )}
                />
              </Card>
            </List.Item>
          )}
        />
      ),
      span: 3,
    },
  ];

  return (
    <>
      <Descriptions
        bordered
        items={items}
        size="small"
        style={{ marginBottom: 10 }}
      />
      <Button type="primary" onClick={handleEdit}>
        Edit Character
      </Button>
      <Divider type="vertical" />
      <Button type="primary" danger onClick={handleDelete}>
        Delete Character
      </Button>
    </>
  );
}
