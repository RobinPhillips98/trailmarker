import { Button, Card, Descriptions, List } from "antd";
import { splitCamelCase, toTitleCase } from "./characterHelpers";
export default function CharacterDisplay({ character, deleteCharacter }) {
  function handleClick() {
    deleteCharacter(character);
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
      key: "attributes",
      label: "Attribute Modifiers",
      children: (
        <List size="small">
          {Object.keys(character.attribute_modifiers).map((attribute) => {
            return (
              <List.Item>
                {toTitleCase(attribute)}:{" "}
                {character.attribute_modifiers[attribute]}
              </List.Item>
            );
          })}
        </List>
      ),
      span: 2,
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
          grid={{ gutter: 16, column: 5 }}
          dataSource={character.actions.attacks}
          renderItem={(attack) => (
            <List.Item>
              <Card title={attack.name} style={{ maxWidth: 300 }}>
                <List
                  size="small"
                  dataSource={Object.keys(attack).slice(1)}
                  renderItem={(item) => (
                    <List.Item>
                      {toTitleCase(splitCamelCase(item))}: {attack[item]}
                    </List.Item>
                  )}
                ></List>
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
      <Button danger onClick={handleClick}>
        Delete Character
      </Button>
    </>
  );
}
