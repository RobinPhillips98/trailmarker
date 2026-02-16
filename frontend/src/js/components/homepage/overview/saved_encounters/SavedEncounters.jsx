import { useContext, useEffect, useState } from "react";
import { Button, Modal, Card } from "antd";

import api from "../../../../api";
import { AuthContext } from "../../../../contexts/AuthContext";

import Encounter from "./Encounter";

/**
 * A component that displays a list of saved encounters
 *
 * @param {object} props
 * @param {function} props.handleLoad The function to select this encounter's enemies
 * @returns {JSX.Element}
 */
export default function SavedEncounters({ handleLoad }) {
  const [encounters, setEncounters] = useState([]);

  const { user, token } = useContext(AuthContext);

  /**
   * Deletes the given encounter from the database and removes it from the list
   * @param {object} encounter
   */
  async function deleteEncounter(encounter) {
    await api.delete(`encounters/${encounter.id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setEncounters((prev) =>
      prev.filter((currentEncounter) => currentEncounter !== encounter),
    );
  }

  const [isModalOpen, setIsModalOpen] = useState(false);
  function showModal() {
    setIsModalOpen(true);
  }

  function handleClose() {
    setIsModalOpen(false);
  }

  useEffect(() => {
    /**
     * Fetches the current list of encounters from the database
     */
    async function fetchEncounters() {
      try {
        const response = await api.get("/encounters", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setEncounters(response.data.encounters);
      } catch (error) {
        console.error("Error fetching encounters", error);
      }
    }
    fetchEncounters();
  }, [isModalOpen, token]);

  return (
    <div>
      <Button
        style={{ marginBottom: 10 }}
        type="primary"
        block
        onClick={showModal}
        disabled={!user}
      >
        Open Saved Encounters
      </Button>
      <Modal
        title="Saved Encounters"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onCancel={handleClose}
        footer={
          <Button key="close" onClick={handleClose}>
            Close
          </Button>
        }
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
