import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ConfigProvider, Flex, Layout, theme } from "antd";

import { AuthProvider } from "./contexts/AuthContext.jsx";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import Homepage from "./components/homepage/Homepage.jsx";
import NavBar from "./components/NavBar.jsx";
import Characters from "./components/characters/Characters.jsx";
import CharacterCreationForm from "./components/characters/character_creation_form/CharacterCreationForm.jsx";

export default function App() {
  const { Header, Content } = Layout;
  const themeConfig = {
    token: {
      colorPrimary: "#722ed1",
      colorInfo: "#722ed1",
    },
    algorithm: theme.darkAlgorithm,
  };

  return (
    <Router>
      <AuthProvider>
        <ConfigProvider theme={themeConfig}>
          <Flex>
            <Layout>
              <Header style={{ backgroundColor: "#141414" }}>
                <NavBar />
              </Header>
              <Content>
                <Routes>
                  <Route path="/" element={<Homepage />} />
                  <Route path="/characters" element={<Characters />} />
                  <Route
                    path="/characters/create"
                    element={<CharacterCreationForm />}
                  />
                  <Route path="/register" element={<Register />} />
                  <Route path="/login" element={<Login />} />
                </Routes>
              </Content>
            </Layout>
          </Flex>
        </ConfigProvider>
      </AuthProvider>
    </Router>
  );
}
