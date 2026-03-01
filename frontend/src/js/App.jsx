// Third-party libraries
import { Alert, ConfigProvider, Flex, Layout, theme } from "antd";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

// Contexts
import { AuthProvider } from "./contexts/AuthContext.jsx";

// Components
import Register from "./components/user_authentication/Register.jsx";
import Login from "./components/user_authentication/Login.jsx";
import Homepage from "./components/homepage/Homepage.jsx";
import NavBar from "./components/NavBar.jsx";
import Characters from "./components/characters/Characters.jsx";
import CharacterCreationForm from "./components/characters/character_creation_form/CharacterCreationForm.jsx";
import Simulation from "./components/simulation/Simulation.jsx";
import PolicyNotice from "./components/PolicyNotice.jsx";

/**
 * The core app component, orchestrating all other components.
 *
 * @returns {React.ReactElement}
 */
export default function App() {
  const { Header, Content, Footer } = Layout;
  const { ErrorBoundary } = Alert;
  const themeConfig = {
    token: {
      colorBgLayout: "#0f1418",
      colorBgContainer: "#15181c",
      colorBgBase: "#0b0f12",

      colorText: "#E9E7E2",
      colorTextSecondary: "#B9B7B2",

      colorBorder: "#26292d",
      colorSplit: "#1d2124",

      colorInfo: "#00c3ff",
      colorWarning: "#D17E1A",
      colorError: "#E65353",
      colorSuccess: "#2F9D7E",

      borderRadius: 6,
    },
    algorithm: theme.darkAlgorithm,
  };

  return (
    <Router>
      <ErrorBoundary>
        <AuthProvider>
          <ConfigProvider theme={themeConfig}>
            <Flex>
              <Layout>
                <Header
                  style={{
                    background: themeConfig.token.colorBgContainer,
                    marginBottom: 10,
                  }}
                >
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
                    <Route path="/copyright" element={<PolicyNotice />} />
                  </Routes>
                </Content>
                <Footer>
                  This website is not published, endorsed, or specifically
                  approved by Paizo Inc. We are expressly prohibited from
                  charging you to use or access this content.{" "}
                  <Link to="/copyright">See more.</Link>
                </Footer>
              </Layout>
            </Flex>
          </ConfigProvider>
        </AuthProvider>
      </ErrorBoundary>
    </Router>
  );
}
