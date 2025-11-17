import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Tabs } from "antd";

import { AuthContext } from "../../contexts/AuthContext";
import api from "../../api";
import CharacterDisplay from "./CharacterDisplay";

/**
 * The page for displaying saved characters, with options to edit saved characters
 * and create new characters
 *
 * @returns {JSX.element}
 */
export default function Characters() {
  const [characters, setCharacters] = useState([]);
  const navigate = useNavigate();

  const { token } = useContext(AuthContext);

  async function deleteCharacter(character) {
    await api.delete(`characters/${character.id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setCharacters((prev) =>
      prev.filter((currentCharacter) => currentCharacter !== character)
    );
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
        setCharacters(response.data.characters);
      } catch (error) {
        console.error("Error fetching characters", error);
        alert(error.response.data.detail);
      }
    }
    if (token) fetchCharacters();
    else {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [token, navigate]);

  function handleClick() {
    navigate("/characters/create");
  }

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

  if (token)
    return (
      <>
        <Tabs items={characterTabs} />
        <br />
        <Button type="primary" onClick={handleClick}>
          Create New Character
        </Button>
      </>
    );
}
