import { createContext, useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import {
  loginUser,
  registerUser,
  fetchUserProfile,
} from "../services/AuthHelpers";
import { errorAlert } from "../services/helpers";
import api, { setupAuthInterceptor } from "../api";

const AuthContext = createContext({});

/**
 * Decodes a JSON web token and returns it as a parsed object
 *
 * @param {string} token
 * @returns {object}
 */
function decodeTokenPayload(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

/**
 * Returns true if the token is expired, false if not
 *
 * @param {string} token
 * @returns {boolean}
 */
function isTokenExpired(token) {
  const payload = decodeTokenPayload(token);
  if (!payload?.exp) return true;
  return Date.now() >= payload.exp * 1000;
}

/**
 * A context provider to let all child components access the AuthContext
 *
 * @param {React.ReactElement} children The components this context is wrapping
 * @returns
 */
function AuthProvider({ children }) {
  const storedToken = localStorage.getItem("token");
  const [token, setToken] = useState(
    storedToken && !isTokenExpired(storedToken) ? storedToken : null,
  );
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const interceptorIdRef = useRef(null);

  // If there was a stored token but it's already expired on load, clear it
  useEffect(() => {
    if (storedToken && isTokenExpired(storedToken)) {
      localStorage.removeItem("token");
    }
  }, []);

  // Fetch user profile whenever the token changes
  useEffect(() => {
    if (token) {
      const getUser = async () => {
        const user = await fetchUserProfile(token);
        setUser(user);
      };
      getUser();
    }
  }, [token]);

  // Set up the Axios interceptor to catch 401s (e.g. token expired mid-session)
  useEffect(() => {
    interceptorIdRef.current = setupAuthInterceptor(() => {
      setToken(null);
      setUser(null);
      localStorage.removeItem("token");
      alert("Your session has expired. Please log in again.");
      navigate("/login");
    });

    return () => {
      if (interceptorIdRef.current !== null) {
        api.interceptors.response.eject(interceptorIdRef.current);
      }
    };
  }, [navigate]);

  // Proactively log the user out when the token's expiration time is reached
  useEffect(() => {
    if (!token) return;

    const payload = decodeTokenPayload(token);
    if (!payload?.exp) return;

    const msUntilExpiry = payload.exp * 1000 - Date.now();
    if (msUntilExpiry <= 0) return; // Already expired — handled elsewhere

    const timer = setTimeout(() => {
      setToken(null);
      setUser(null);
      localStorage.removeItem("token");
      alert("Your session has expired. Please log in again.");
      navigate("/login");
    }, msUntilExpiry);

    // Clear the timer if the token changes before it fires (e.g. logout)
    return () => clearTimeout(timer);
  }, [token, navigate]);

  /**
   * Attempts to log the user in and saves their JWT in local storage
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
   * Attempts to register a new user with the given username and password
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
   * Logs the user out, removing their token and setting user to null
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
