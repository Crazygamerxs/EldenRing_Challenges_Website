import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './ErrorBoundary.css';

import { API_ENDPOINTS } from '../../utils/api';
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to an error reporting service
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    this.setState({ errorInfo });
    
    // You could also log the error to a remote logging service here
    // Example: logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="error-boundary">
          <div className="error-container">
            <h2>Something went wrong</h2>
            <p>We're sorry, but an error occurred while rendering this page.</p>
            <div className="error-actions">
              <button 
                onClick={() => window.location.reload()}
                className="error-reload-btn"
              >
                Reload Page
              </button>
              <button 
                onClick={() => window.location.href = '/'}
                className="error-home-btn"
              >
                Go to Home
              </button>
            </div>
            {this.props.showDetails && (
              <details className="error-details">
                <summary>Error Details</summary>
                <p>{this.state.error && this.state.error.toString()}</p>
                <div>
                  {this.state.errorInfo && 
                    <pre>{this.state.errorInfo.componentStack}</pre>
                  }
                </div>
              </details>
            )}
          </div>
        </div>
      );
    }

    // If there's no error, render children normally
    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
  showDetails: PropTypes.bool
};

ErrorBoundary.defaultProps = {
  showDetails: false // Default to not showing technical error details
};

export default ErrorBoundary;
