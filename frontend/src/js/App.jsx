import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext.jsx";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import Homepage from "./components/homepage/Homepage.jsx";
import { ConfigProvider, Layout, theme } from "antd";
import NavBar from "./components/NavBar.jsx";
import Characters from "./components/characters/Characters.jsx";
import CharacterCreationForm from "./components/characters/CharacterCreationForm.jsx";
const { Header, Content } = Layout;

function App() {
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
          <NavBar />
          <br />
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
        </ConfigProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
