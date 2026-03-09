import { App } from "antd";
import { useCallback } from "react";

/**
 * Returns an `errorMessage` function that logs an error to the console
 * and displays an Ant Design error message toast to the user.
 *
 * @returns {{ errorMessage: function }}
 */
export default function useErrorMessage() {
  const { message } = App.useApp();

  const errorMessage = useCallback(
    (msg, error) => {
      console.error(msg, error);
      let errorString = "";
      if (typeof error?.response?.data?.detail === "object")
        errorString = `${msg}: ${error?.status ?? "500"} ${error?.response?.statusText ?? error}`;
      else {
        errorString = `${msg}: ${error?.response?.data?.detail ?? error}`;
      }
      message.error(errorString);
    },
    [message],
  );

  return { errorMessage };
}
