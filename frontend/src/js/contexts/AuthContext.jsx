import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  loginUser,
  registerUser,
  fetchUserProfile,
} from "../services/AuthHelpers";

const AuthContext = createContext({});

function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      const getUser = async () => {
        const user = await fetchUserProfile(token);
        setUser(user);
      };
      getUser();
    }
  }, [token]);

  async function login(username, password) {
    try {
      const response = await loginUser({ username, password });
      if (response?.access_token) {
        setToken(response.access_token);
        localStorage.setItem("token", response.access_token);
        const userProfile = await fetchUserProfile(response.access_token);
        setUser(userProfile);
        navigate("/");
      }
    } catch (error) {
      alert(error.response.data.detail);
    }
  }

  async function register(username, password) {
    try {
      await registerUser({ username, password });
      navigate("/login");
    } catch (error) {
      alert(error.response.data.detail);
    }
  }

  function logout() {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    alert("Logged out!");
    navigate("/login");
  }

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthProvider, AuthContext };
