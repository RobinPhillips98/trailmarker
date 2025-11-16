import api from "../api";

async function loginUser(credentials) {
  try {
    const params = new URLSearchParams();
    for (const key in credentials) {
      params.append(key, credentials[key]);
    }

    const response = await api.post("/auth/token", params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Login error:", error);
    throw error;
  }
}

async function registerUser(userData) {
  try {
    await api.post("/auth/register", userData);
  } catch (error) {
    console.error("Registration error:", error);
    throw error;
  }
}

async function fetchUserProfile(token) {
  try {
    const response = await api.get("/users/me/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Fetch user profile error:", error);
    throw error;
  }
}

export { loginUser, registerUser, fetchUserProfile };
