import api from "../api";

/**
 * Attempts to retrieve a JSON Web Token from the API using the given credentials
 * 
 * @param {object} credentials An object containing the username and password given
 * @returns 
 */
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

/**
 * Attempts to post the given user to the API, which will add it to the database
 * if successful
 * 
 * @param {object} userData An object containing the data to register a given user
 */
async function registerUser(userData) {
  try {
    await api.post("/auth/register", userData);
  } catch (error) {
    console.error("Registration error:", error);
    throw error;
  }
}

/**
 * Attempts to fetch the current user from the database using the currently
 * stored JSON web token
 * 
 * @param {string} token The currently stored JWT
 * @returns 
 */
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
