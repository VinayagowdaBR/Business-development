import React from 'react';
import { Search, Bell, Mail, User, LogOut } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Topbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={styles.topbar}>
      <div style={styles.searchSection}>
        <Search size={20} style={styles.searchIcon} />
        <input 
          type="text" 
          placeholder="Search..." 
          style={styles.searchInput}
        />
      </div>

      <div style={styles.rightSection}>
        <button style={styles.iconButton}>
          <Mail size={20} />
        </button>
        <button style={styles.iconButton}>
          <Bell size={20} />
          <span style={styles.badge}>3</span>
        </button>
        
        <div style={styles.userSection}>
          <div style={styles.avatar}>
            <User size={20} />
          </div>
          <div style={styles.userInfo}>
            <span style={styles.userName}>{user?.username}</span>
            <span style={styles.userRole}>{user?.role}</span>
          </div>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

const styles = {
  topbar: {
    height: '70px',
    background: 'white',
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 30px',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  searchSection: {
    display: 'flex',
    alignItems: 'center',
    background: '#f5f5f5',
    padding: '10px 15px',
    borderRadius: '8px',
    width: '400px',
  },
  searchIcon: {
    color: '#999',
    marginRight: '10px',
  },
  searchInput: {
    border: 'none',
    background: 'transparent',
    outline: 'none',
    flex: 1,
    fontSize: '14px',
  },
  rightSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  iconButton: {
    background: 'transparent',
    border: 'none',
    padding: '10px',
    cursor: 'pointer',
    borderRadius: '8px',
    position: 'relative',
    color: '#666',
    transition: 'background 0.2s',
  },
  badge: {
    position: 'absolute',
    top: '5px',
    right: '5px',
    background: '#ef4444',
    color: 'white',
    fontSize: '10px',
    padding: '2px 5px',
    borderRadius: '10px',
    fontWeight: 'bold',
  },
  userSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginLeft: '15px',
    paddingLeft: '15px',
    borderLeft: '1px solid #e5e5e5',
  },
  avatar: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
  },
  userInfo: {
    display: 'flex',
    flexDirection: 'column',
  },
  userName: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
  },
  userRole: {
    fontSize: '12px',
    color: '#999',
    textTransform: 'capitalize',
  },
  logoutBtn: {
    background: 'transparent',
    border: 'none',
    padding: '8px',
    cursor: 'pointer',
    color: '#666',
    borderRadius: '6px',
    transition: 'all 0.2s',
  },
};

export default Topbar;
