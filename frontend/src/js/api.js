import axios from "axios";

/**
 * An axios instance used for handling API calls
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

/**
 * Sets up an Axios response interceptor that calls the provided logout
 * function whenever a 401 Unauthorized response is received
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

export default api;
