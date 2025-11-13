import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import OrganizationDashboard from './OrganizationDashboard';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h2>Welcome, {user?.username}! 👋</h2>
          <p style={styles.subtitle}>{user?.email}</p>
        </div>
        <button onClick={handleLogout} style={styles.logoutButton}>
          Logout
        </button>
      </div>

      {/* User Info Card */}
      <div style={styles.card}>
        <h3>Your Profile</h3>
        <div style={styles.infoGrid}>
          <div>
            <p><strong>Username:</strong> {user?.username}</p>
            <p><strong>Email:</strong> {user?.email}</p>
          </div>
          <div>
            <p><strong>Role:</strong> <span style={styles.badge}>{user?.role}</span></p>
            <p><strong>User ID:</strong> {user?.id}</p>
          </div>
        </div>
      </div>

      {/* Organization Dashboard */}
      <OrganizationDashboard />
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    maxWidth: '1000px',
    margin: '0 auto 20px',
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  subtitle: {
    color: '#666',
    margin: '5px 0 0 0',
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  card: {
    maxWidth: '1000px',
    margin: '0 auto 20px',
    padding: '30px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  infoGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
    marginTop: '15px',
  },
  badge: {
    padding: '5px 10px',
    backgroundColor: '#007bff',
    color: 'white',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 'bold',
  },
};

export default Dashboard;
