import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext.jsx";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import Homepage from "./components/homepage/Homepage.jsx";
import { Anchor, ConfigProvider, Layout, theme } from "antd";
import AnchorLink from "antd/es/anchor/AnchorLink.js";
import NavBar from "./components/NavBar.jsx";
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
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Homepage />} />
          </Routes>
        </ConfigProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
