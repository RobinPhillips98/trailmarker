import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ConfigProvider, Flex, Layout, theme } from "antd";

import { AuthProvider } from "./contexts/AuthContext.jsx";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import Homepage from "./components/homepage/Homepage.jsx";
import NavBar from "./components/NavBar.jsx";
import Characters from "./components/characters/Characters.jsx";
import CharacterCreationForm from "./components/characters/character_creation_form/CharacterCreationForm.jsx";
import Simulation from "./components/simulation/Simulation.jsx";

export default function App() {
  const { Header, Content } = Layout;
  const themeConfig = {
    token: {
      colorPrimary: "#5B2D86",

      colorBgLayout: "#0f1418",
      colorBgContainer: "#15181c",
      colorBgBase: "#0b0f12",

      colorText: "#E9E7E2",
      colorTextSecondary: "#B9B7B2",

      colorBorder: "#26292d",
      colorSplit: "#1d2124",

      colorInfo: "#5B2D86",
      colorWarning: "#D17E1A",
      colorError: "#E65353",
      colorSuccess: "#2F9D7E",

      borderRadius: 6
    },
    algorithm: theme.darkAlgorithm
  };

  return (
    <Router>
      <AuthProvider>
        <ConfigProvider theme={themeConfig}>
          <Flex>
            <Layout>
              <Header style={{ background: themeConfig.token.colorBgContainer, marginBottom: 10 }}>
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
                  <Route path="/simulation" element={<Simulation />} />
                </Routes>
              </Content>
            </Layout>
          </Flex>
        </ConfigProvider>
      </AuthProvider>
    </Router>
  );
}
