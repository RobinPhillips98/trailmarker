// Third-party libraries
import { useContext, useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { App, Button, FloatButton, Space, Spin, Tabs, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";

// Personal helpers
import api from "../../api";
import useErrorMessage from "../../services/hooks/useErrorMessage";

// Contexts
import { AuthContext } from "../../contexts/AuthContext";

// Components
import CharacterDisplay from "./character_display/CharacterDisplay";
import NotAuthorized from "../status_pages/NotAuthorized";
import CharacterImport from "./CharacterImport";

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
  const [loading, setLoading] = useState(true);

  // Other variables
  const navigate = useNavigate();
  const location = useLocation();
  const { message } = App.useApp();
  const { token } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();

  const { Title } = Typography;

  const characterTabs = characters.map((character) => ({
    key: character.id,
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
   * Adds `character` to the display, sorts the display, and shows `character`
   *
   * @param {object} character The character to be added
   */
  function addCharacter(character) {
    const newCharacters = characters.slice();
    newCharacters.push(character);
    const sortedCharacters = sortCharacters(newCharacters);
    setCharacters(sortedCharacters);
    setActiveTab(character.id);
  }

  /**
   * Returns a copy of `characters` sorted by the `name` key of each character
   *
   * @param {object[]} characters The character array to be sorted
   * @returns {object[]}
   */
  function sortCharacters(characters) {
    return characters.sort((a, b) => a.name.localeCompare(b.name));
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
      const newCharacters = characters.filter(
        (currentCharacter) => currentCharacter !== character,
      );
      const sortedCharacters = sortCharacters(newCharacters);
      setCharacters(sortedCharacters);
      if (sortedCharacters.length > 0) {
        setActiveTab(sortedCharacters[0].id);
      }
      message.success("Character deleted!");
    } catch (error) {
      errorMessage("Error deleting character", error);
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
        const sortedCharacters = sortCharacters(response.data.characters);
        setCharacters(sortedCharacters);
        setLoading(false);

        // Set active tab to the character from navigation state if available
        if (location.state?.selectedCharacter) {
          setActiveTab(location.state.selectedCharacter);
        } else if (sortedCharacters.length > 0) {
          setActiveTab(sortedCharacters[0].id);
        }
      } catch (error) {
        errorMessage("Error fetching characters", error);
      }
    }
    if (token) fetchCharacters();
  }, [location.state, token, navigate]);

  if (token)
    return (
      <>
        <Title level={1}>Saved Characters</Title>

        <Space style={{ marginBottom: 10 }}>
          <Button type="primary" onClick={handleClick} icon={<PlusOutlined />}>
            Create Character
          </Button>
          <CharacterImport addCharacter={addCharacter} />
        </Space>
        <Spin spinning={loading}>
          <Tabs
            type="card"
            size="large"
            items={characterTabs}
            className="character-tabs"
            activeKey={activeTab}
            onChange={setActiveTab}
          />
        </Spin>
        <FloatButton.BackTop />
      </>
    );
  else {
    return <NotAuthorized />;
  }
}
