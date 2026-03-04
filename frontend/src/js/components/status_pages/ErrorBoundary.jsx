import React from "react";
import { Button, Result, Typography } from "antd";
import { Link, useLocation } from "react-router-dom";

/**
 * Wraps ErrorBoundaryClass to reset it whenever the route changes.
 *
 * @param {object} props
 * @param {React.ReactNode} props.children
 */
export default function ErrorBoundary({ children }) {
  const location = useLocation();
  return (
    <ErrorBoundaryClass location={location}>{children}</ErrorBoundaryClass>
  );
}

/**
 * A custom error boundary that catches uncaught errors in the component tree
 * and displays a 500-style error page using Ant Design's Result component.
 */
class ErrorBoundaryClass extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error("Uncaught error:", error, errorInfo);
  }

  componentDidUpdate(prevProps) {
    if (this.state.hasError && prevProps.location !== this.props.location) {
      this.setState({ hasError: false, error: null, errorInfo: null });
    }
  }

  render() {
    if (this.state.hasError) {
      const { error, errorInfo } = this.state;
      const { Paragraph, Text } = Typography;

      return (
        <Result
          status="500"
          title="500"
          subTitle="Sorry, something went wrong."
          extra={
            <Button type="primary">
              <Link to="/">Back to Home</Link>
            </Button>
          }
        >
          {error && (
            <Paragraph>
              <Text strong style={{ fontSize: 16 }}>
                {error.toString()}
              </Text>
            </Paragraph>
          )}
          {import.meta.env.DEV && errorInfo?.componentStack && (
            <Paragraph>{errorInfo.componentStack}</Paragraph>
          )}
        </Result>
      );
    }

    return this.props.children;
  }
}
