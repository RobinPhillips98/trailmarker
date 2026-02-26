import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import {
  loginUser,
  registerUser,
  fetchUserProfile,
} from "../services/AuthHelpers";
import { errorAlert } from "../services/helpers";

const AuthContext = createContext({});

/**
 * A provider to allow components to use authentication methods
 *
 * @param {object} props
 * @param {JSX.Element} props.children The child components of the AuthProvider
 * @returns {JSX.Element}
 */
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

  /**
   * A wrapper function for loginUser that saves a JSON Web Token to local storage
   * if the login is successful, and alerts if it is not
   *
   * @param {string} username The username entered by the user
   * @param {string} password The password entered by the user
   */
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
      errorAlert("Error logging in", error);
    }
  }

  /**
   * A wrapper function for registerUser that navigates to /login if the
   * registration is successful, and alerts if it is not.
   *
   * @param {string} username The username entered by the user
   * @param {string} password The password entered by the user
   */
  async function register(username, password) {
    try {
      await registerUser({ username, password });
      navigate("/login");
    } catch (error) {
      errorAlert("Error registering", error);
    }
  }

  /**
   * Logs the user out by deleting the JSON Web Token from local storage and
   * setting token and user to null
   */
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
