import axios from "axios";

// Create an instance of axios with the base URL
const api = axios.create({
  baseURL: "http://localhost:8000",
});

/**
 * Sets up an Axios response interceptor that calls the provided logout
 * function whenever a 401 Unauthorized response is received.
 *
 * @param {function} onUnauthorized - Callback to invoke on 401 responses
 * @returns {number} The interceptor ID (can be used to eject it later)
 */
export function setupAuthInterceptor(onUnauthorized) {
  return api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        onUnauthorized();
      }
      return Promise.reject(error);
    },
  );
}

// Export the Axios instance
export default api;
