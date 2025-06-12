import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import { API_ENDPOINTS } from '../../utils/api';
const RouteLoader = ({ setIsLoading }) => {
  const location = useLocation();

  useEffect(() => {
    setIsLoading(true);

    const timer = setTimeout(() => setIsLoading(false), 500);

    return () => clearTimeout(timer);
  }, [location, setIsLoading]);

  return null;
};

export default RouteLoader;
