import { useEffect, useState } from "react";
import { Typography, Empty, Spin, Row, Col, Form } from "antd";

import api from "../../../api";
import Enemy from "./Enemy";
import EnemyFilterForm from "./EnemyFilterForm";

/**
 * A component to display a list of all enemies from the database
 *
 * @param {object} props
 * @param {function} props.handleAdd The function to add an enemy to the encounter
 * @returns {JSX.Element}
 */
export default function EnemyList({ handleAdd }) {
  const [enemies, setEnemies] = useState([]);
  const [displayEnemies, setDisplayEnemies] = useState([]);
  const [loading, setLoading] = useState(true);
  const { Title } = Typography;

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
      console.error("Error fetching enemies", error);
      alert(error);
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEnemies();
  }, []);

  const [form] = Form.useForm();
  const name = Form.useWatch("name", form);
  const minLevel = Form.useWatch("minLevel", form);
  const maxLevel = Form.useWatch("maxLevel", form);
  const traits = Form.useWatch("traits", form);
  const traitFilterMode = Form.useWatch("traitFilterMode", form);

  useEffect(() => {
    console.log(traitFilterMode);

    let filteredEnemies = enemies.filter(
      (enemy) =>
        enemy.name.includes(name) &&
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
    setDisplayEnemies(filteredEnemies);
  }, [enemies, minLevel, maxLevel, name, traits, traitFilterMode]);

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
                style={{ height: "300px" }}
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
