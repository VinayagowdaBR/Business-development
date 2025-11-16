import React, { useState } from 'react';
import { 
  Home, Users, Database, Settings, ChevronDown, 
  BarChart3, FileText, Bell, Menu, X, Shield, UserCheck, Map, Share2, Tag   // Add UserCheck
} from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';



const Sidebar = ({ collapsed, setCollapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [openMenus, setOpenMenus] = useState({});

  const menuItems = [
    { id: 'dashboard', icon: Home, label: 'Dashboard', path: '/dashboard' },
    { 
      id: 'users', 
      icon: Users, 
      label: 'User Management', 
      path: '/users',
      subItems: [
        { label: 'All Users', path: '/users' },
        { label: 'Roles', path: '/users/roles' },
      ]
    },
    
    { id: 'area-legion', icon: Map, label: 'Area and Legion', path: '/areas-legions' },
    { id: 'members', icon: UserCheck, label: 'Members List', path: '/members' },
    { id: 'membership-fees', icon: Share2, label: 'Membership Fees', path: '/membership-fees' },
    { id: 'member-types', icon: Tag, label: 'Member Types', path: '/member-types' },
        
    { id: 'database', icon: Database, label: 'Database', path: '/database' },
    { id: 'reports', icon: BarChart3, label: 'Reports', path: '/reports' },
    { id: 'documents', icon: FileText, label: 'Documents', path: '/documents' },
    { id: 'notifications', icon: Bell, label: 'Notifications', path: '/notifications' },
    { id: 'settings', icon: Settings, label: 'Settings', path: '/settings' },
  ];

  const toggleSubmenu = (id) => {
    setOpenMenus(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div 
      style={{
        ...styles.sidebar,
        width: collapsed ? '80px' : '260px',
      }}
    >
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logo}>
          {!collapsed && <span style={styles.logoText}>B2B Platform</span>}
          {collapsed && <span style={styles.logoTextShort}>B2B</span>}
        </div>
        <button 
          onClick={() => setCollapsed(!collapsed)}
          style={styles.toggleBtn}
        >
          {collapsed ? <Menu size={20} /> : <X size={20} />}
        </button>
      </div>

      {/* Navigation Menu */}
      <nav style={styles.nav}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          const hasSubmenu = item.subItems && item.subItems.length > 0;
          const submenuOpen = openMenus[item.id];

          return (
            <div key={item.id}>
              <div
                onClick={() => {
                  if (hasSubmenu) {
                    toggleSubmenu(item.id);
                  } else {
                    navigate(item.path);
                  }
                }}
                style={{
                  ...styles.menuItem,
                  ...(active ? styles.menuItemActive : {}),
                }}
              >
                <Icon size={20} style={styles.menuIcon} />
                {!collapsed && (
                  <>
                    <span style={styles.menuLabel}>{item.label}</span>
                    {hasSubmenu && (
                      <ChevronDown 
                        size={16} 
                        style={{
                          ...styles.chevron,
                          transform: submenuOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                        }}
                      />
                    )}
                  </>
                )}
              </div>

              {/* Submenu */}
              {hasSubmenu && submenuOpen && !collapsed && (
                <div style={styles.submenu}>
                  {item.subItems.map((subItem, idx) => (
                    <div
                      key={idx}
                      onClick={() => navigate(subItem.path)}
                      style={{
                        ...styles.submenuItem,
                        ...(isActive(subItem.path) ? styles.submenuItemActive : {}),
                      }}
                    >
                      {subItem.label}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>
    </div>
  );
};

const styles = {
  sidebar: {
    height: '100vh',
    background: 'linear-gradient(180deg, #6366f1 0%, #4f46e5 100%)',
    color: 'white',
    display: 'flex',
    flexDirection: 'column',
    position: 'fixed',
    left: 0,
    top: 0,
    transition: 'width 0.3s ease',
    boxShadow: '4px 0 10px rgba(0,0,0,0.1)',
    zIndex: 1000,
  },
  header: {
    padding: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
  },
  logoText: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: 'white',
  },
  logoTextShort: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: 'white',
  },
  toggleBtn: {
    background: 'transparent',
    border: 'none',
    color: 'white',
    cursor: 'pointer',
    padding: '5px',
  },
  nav: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px 10px',
  },
  menuItem: {
    display: 'flex',
    alignItems: 'center',
    padding: '12px 15px',
    margin: '5px 0',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    color: 'rgba(255,255,255,0.8)',
  },
  menuItemActive: {
    background: 'rgba(255,255,255,0.15)',
    color: 'white',
    fontWeight: '500',
  },
  menuIcon: {
    minWidth: '20px',
  },
  menuLabel: {
    marginLeft: '15px',
    flex: 1,
    fontSize: '14px',
  },
  chevron: {
    transition: 'transform 0.2s',
  },
  submenu: {
    marginLeft: '35px',
    paddingLeft: '15px',
    borderLeft: '2px solid rgba(255,255,255,0.2)',
  },
  submenuItem: {
    padding: '8px 15px',
    margin: '3px 0',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    color: 'rgba(255,255,255,0.7)',
    transition: 'all 0.2s',
  },
  submenuItemActive: {
    background: 'rgba(255,255,255,0.1)',
    color: 'white',
  },
};

export default Sidebar;
