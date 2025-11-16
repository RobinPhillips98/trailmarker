import { Button, Tabs } from "antd";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import CharacterDisplay from "./CharacterDisplay";

export default function Characters() {
  const [characters, setCharacters] = useState([]);
  const navigate = useNavigate();

  const { token, user } = useContext(AuthContext);

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
      }
    }
    if (token && user) fetchCharacters();
    else {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [token, user, navigate]);

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
        <Tabs items={characterTabs}/>
        <br />
        <Button type="primary" onClick={handleClick}>
          Create New Character
        </Button>
      </>
    );
}
