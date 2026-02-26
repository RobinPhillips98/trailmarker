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

function decodeTokenPayload(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

function isTokenExpired(token) {
  const payload = decodeTokenPayload(token);
  if (!payload?.exp) return true;
  return Date.now() >= payload.exp * 1000;
}

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
      alert("Your session has expired. Please log in again.");
      navigate("/login");
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

  async function register(username, password) {
    try {
      await registerUser({ username, password });
      navigate("/login");
    } catch (error) {
      errorAlert("Error registering", error);
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
