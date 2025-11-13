import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const MainLayout = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div style={styles.container}>
      <Sidebar collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} />
      
      <div 
        style={{
          ...styles.mainContent,
          marginLeft: sidebarCollapsed ? '80px' : '260px',
        }}
      >
        <Topbar />
        <div style={styles.content}>
          {children}
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    minHeight: '100vh',
    background: '#f8f9fa',
  },
  mainContent: {
    flex: 1,
    transition: 'margin-left 0.3s ease',
  },
  content: {
    minHeight: 'calc(100vh - 70px)',
  },
};

export default MainLayout;
