import axios from "axios";

/**
 * An axios instance used for handling API calls
 */
const api = axios.create({
  baseURL: "http://localhost:8000",
});

/**
 * Sets up an Axios response interceptor that calls the provided logout
 * function whenever a 401 Unauthorized response is received, unless the
 * request was made to the login endpoint (where a 401 is an expected
 * failure, not an expired session).
 *
 * @param {function} onUnauthorized - Callback to invoke on 401 responses
 * @returns {number} The interceptor ID (can be used to eject it later)
 */
export function setupAuthInterceptor(onUnauthorized) {
  return api.interceptors.response.use(
    (response) => response,
    (error) => {
      const isLoginRequest = error.config?.url === "/auth/token";
      if (error.response?.status === 401 && !isLoginRequest) {
        onUnauthorized();
      }
      return Promise.reject(error);
    },
  );
}

export default api;
