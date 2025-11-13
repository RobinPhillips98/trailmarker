import Encounter from "./Encounter";
import { useState, useEffect } from "react";
import { Button, Modal, Card } from "antd";
import api from "../../../api";

function SavedEncounters({ handleLoad }) {
  const [encounters, setEncounters] = useState([]);

  async function fetchEncounters() {
    try {
      const response = await api.get("/encounters");
      setEncounters(response.data.encounters);
    } catch (error) {
      console.error("Error fetching encounters", error);
    }
  }

  async function deleteEncounter(encounter) {
    await api.delete(`encounters/${encounter.id}`);
    setEncounters((prev) =>
      prev.filter((currentEncounter) => currentEncounter !== encounter)
    );
  }

  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    fetchEncounters();
  }, [isModalOpen]);

  return (
    <div>
      <Button style={{ marginBottom: 10 }} type="primary" onClick={showModal}>
        Open Saved Encounters
      </Button>
      <Modal
        title="Saved Encounters"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        {encounters.map((encounter) => (
          <Card
            size="small"
            title={encounter.name}
            style={{ marginBottom: 10 }}
          >
            <Encounter
              encounter={encounter}
              handleLoad={handleLoad}
              handleDelete={deleteEncounter}
            />
          </Card>
        ))}
      </Modal>
    </div>
  );
}

export default SavedEncounters;
