import React from 'react';
import { Outlet } from 'react-router-dom';

const BaseLayout = () => {
  return (
    <div className="container mt-3">
      <Outlet />
    </div>
  );
};

export default BaseLayout;
