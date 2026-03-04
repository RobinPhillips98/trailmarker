import { Link } from "react-router-dom";
import { Button, Result } from "antd";

/**
 * A 404 Not Found page shown when no routes match the current URL.
 *
 * @returns {React.ReactElement}
 */
export default function NotFound() {
  return (
    <Result
      status="404"
      title="404"
      subTitle="Sorry, the page you visited does not exist."
      extra={
        <Button type="primary">
          <Link to="/">Back to Home</Link>
        </Button>
      }
    />
  );
}
