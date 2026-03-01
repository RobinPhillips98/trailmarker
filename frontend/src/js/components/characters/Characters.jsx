// Third-party libraries
import { useContext, useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button, FloatButton, Tabs, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";

// Personal helpers
import api from "../../api";
import { errorAlert } from "../../services/helpers";

// Contexts
import { AuthContext } from "../../contexts/AuthContext";

// Components
import CharacterDisplay from "./character_display/CharacterDisplay";

/**
 * The page for displaying saved characters, with options to edit saved
 * characters and create new characters
 *
 * @returns {React.ReactElement}
 */
export default function Characters() {
  // State variables
  const [characters, setCharacters] = useState([]);
  const [activeTab, setActiveTab] = useState(null);

  // Other variables
  const navigate = useNavigate();
  const location = useLocation();
  const { token } = useContext(AuthContext);

  const { Title } = Typography;

  const characterTabs = characters.map((character) => ({
    key: character.name,
    label: character.name,
    children: (
      <CharacterDisplay
        character={character}
        deleteCharacter={deleteCharacter}
      />
    ),
  }));

  // Functions

  /**
   * Opens character creation page when the create character button is clicked
   */
  function handleClick() {
    navigate("/characters/create", {
      state: { editing: false, savedCharacter: null },
    });
  }

  /**
   * Deletes a character from the database and from the character list.
   *
   * @param {object} character
   */
  async function deleteCharacter(character) {
    try {
      await api.delete(`characters/${character.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCharacters((prev) =>
        prev.filter((currentCharacter) => currentCharacter !== character),
      );
    } catch (error) {
      errorAlert("Error deleting character", error);
    }
  }

  useEffect(() => {
    /**
     * Fetches all characters for the current user from the database
     */
    async function fetchCharacters() {
      try {
        const response = await api.get("/characters", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const sortedCharacters = response.data.characters.sort((a, b) =>
          a.name.localeCompare(b.name),
        );
        setCharacters(sortedCharacters);

        // Set active tab to the character from navigation state if available
        if (location.state?.selectedCharacter) {
          setActiveTab(location.state.selectedCharacter);
        } else if (sortedCharacters.length > 0) {
          setActiveTab(sortedCharacters[0].name);
        }
      } catch (error) {
        errorAlert("Error fetching characters", error);
      }
    }
    if (token) fetchCharacters();
    else {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [location.state, token, navigate]);

  if (token)
    return (
      <>
        <Title level={1}>Saved Characters</Title>
        <Button
          type="primary"
          onClick={handleClick}
          style={{ marginBottom: 10 }}
          icon={<PlusOutlined />}
        >
          Create Character
        </Button>
        <Tabs
          type="card"
          size="large"
          items={characterTabs}
          className="character-tabs"
          activeKey={activeTab}
          onChange={setActiveTab}
        />
        <FloatButton.BackTop />
      </>
    );
  else {
    return null;
  }
}
