// Third-party libraries
import { useEffect, useState } from "react";
import { Col, Empty, Form, Row, Spin, Typography } from "antd";

// Personal helpers
import api from "../../../api";
import { errorAlert } from "../../../services/helpers";

// Components
import Enemy from "./Enemy";
import EnemyFilterForm from "./EnemyFilterForm";

/**
 * A component to display a list of all enemies from the database
 *
 * @param {object} props
 * @param {function} props.handleAdd The function to add an enemy to the
 *  encounter
 * @returns {React.ReactElement}
 */
export default function EnemyList({ handleAdd }) {
  const [enemies, setEnemies] = useState([]);
  const [displayEnemies, setDisplayEnemies] = useState([]);
  const [loading, setLoading] = useState(true);
  const { Title } = Typography;

  const [form] = Form.useForm();
  const name = Form.useWatch("name", form);
  const minLevel = Form.useWatch("minLevel", form);
  const maxLevel = Form.useWatch("maxLevel", form);
  const traits = Form.useWatch("traits", form);
  const traitFilterMode = Form.useWatch("traitFilterMode", form);
  const immunities = Form.useWatch("immunities", form);
  const immunitiesFilterMode = Form.useWatch("immunitiesFilterMode", form);
  const weaknesses = Form.useWatch("weaknesses", form);
  const weaknessesFilterMode = Form.useWatch("weaknessesFilterMode", form);
  const resistances = Form.useWatch("resistances", form);
  const resistancesFilterMode = Form.useWatch("resistancesFilterMode", form);

  /**
   * Fetches all enemies from the database
   */
  async function fetchEnemies() {
    try {
      const response = await api.get("/enemies");
      setEnemies(response.data.enemies);
      setDisplayEnemies(response.data.enemies);
      setLoading(false);
    } catch (error) {
      errorAlert("Error fetching enemies", error);
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEnemies();
  }, []);

  /**
   * Filters enemies based on the filters entered in EnemyFilterForm
   */
  useEffect(() => {
    let filteredEnemies = enemies.filter(
      (enemy) =>
        enemy.name.toLowerCase().includes(name.toLowerCase()) &&
        enemy.level >= minLevel &&
        enemy.level <= maxLevel,
    );

    if (traits && traits.length > 0) {
      if (traitFilterMode) {
        // enemy must have ALL selected traits
        filteredEnemies = filteredEnemies.filter((enemy) =>
          traits.every((trait) => enemy.traits.includes(trait)),
        );
      } else {
        // enemy must have ANY one of the selected traits
        filteredEnemies = filteredEnemies.filter((enemy) =>
          traits.some((trait) => enemy.traits.includes(trait)),
        );
      }
    }
    if (immunities && immunities.length > 0) {
      if (immunitiesFilterMode) {
        // enemy must have ALL selected immunities
        filteredEnemies = filteredEnemies.filter((enemy) =>
          immunities.every((trait) => enemy.immunities.includes(trait)),
        );
      } else {
        // enemy must have ANY one of the selected immunities
        filteredEnemies = filteredEnemies.filter((enemy) =>
          immunities.some((trait) => enemy.immunities.includes(trait)),
        );
      }
    }
    if (weaknesses && weaknesses.length > 0) {
      if (weaknessesFilterMode) {
        // enemy must have ALL selected weaknesses
        filteredEnemies = filteredEnemies.filter((enemy) =>
          weaknesses.every((trait) =>
            Object.keys(enemy.weaknesses).includes(trait),
          ),
        );
      } else {
        // enemy must have ANY one of the selected weaknesses
        filteredEnemies = filteredEnemies.filter((enemy) =>
          weaknesses.some((trait) =>
            Object.keys(enemy.weaknesses).includes(trait),
          ),
        );
      }
    }
    if (resistances && resistances.length > 0) {
      if (resistancesFilterMode) {
        // enemy must have ALL selected resistances
        filteredEnemies = filteredEnemies.filter(
          (enemy) =>
            resistances.every((trait) =>
              Object.keys(enemy.resistances).includes(trait),
            ) || Object.keys(enemy.resistances).includes("all-damage"),
        );
      } else {
        // enemy must have ANY one of the selected resistances
        filteredEnemies = filteredEnemies.filter((enemy) =>
          resistances.some(
            (trait) =>
              Object.keys(enemy.resistances).includes(trait) ||
              Object.keys(enemy.resistances).includes("all-damage"),
          ),
        );
      }
    }
    setDisplayEnemies(filteredEnemies);
  }, [
    enemies,
    minLevel,
    maxLevel,
    name,
    traits,
    traitFilterMode,
    immunities,
    immunitiesFilterMode,
    weaknesses,
    weaknessesFilterMode,
    resistances,
    resistancesFilterMode,
  ]);

  return (
    <div style={{ width: "100%" }}>
      <Title level={3} style={{ marginTop: 0, marginBottom: 16 }}>
        Enemies
      </Title>

      <EnemyFilterForm form={form} />

      <Spin spinning={loading}>
        <div style={{ height: "60vh", overflow: "auto" }}>
          <Row gutter={[16, 16]}>
            {displayEnemies.map((enemy) => (
              <Col
                key={enemy.id}
                xs={24}
                sm={12}
                md={8}
                lg={6}
                xl={4}
                style={{ height: "400px" }}
              >
                <Enemy handleAdd={handleAdd} enemy={enemy} />
              </Col>
            ))}
          </Row>
          {displayEnemies.length === 0 && !loading && (
            <Empty description="No enemies found" />
          )}
        </div>
      </Spin>
    </div>
  );
}
