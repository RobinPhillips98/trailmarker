import { Button, Descriptions, List } from "antd";
export default function CharacterDisplay({ character, deleteCharacter }) {
  function handleClick() {
    deleteCharacter(character);
  }

  const items = [
    {
      key: "name",
      label: "Name",
      children: character.name,
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
      children: character.ancestry,
    },
    {
      key: "background",
      label: "Background",
      children: character.background,
    },
    {
      key: "class",
      label: "Class",
      children: character.class,
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
                {attribute}: {character.attribute_modifiers[attribute]}
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
                {save}: {character.defenses.saves[save]}
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
              {skill}: {character.skills[skill]}
            </List.Item>
          )}
        />
      ),
      span: 2,
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
