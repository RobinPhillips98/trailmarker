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
      message.error(`${msg}: ${error?.response?.data?.detail ?? error}`);
    },
    [message],
  );

  return { errorMessage };
}
