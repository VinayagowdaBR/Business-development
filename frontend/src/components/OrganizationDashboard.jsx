import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { organizationAPI, rbacAPI } from '../services/api';
import { Users, Plus, Edit, Trash2, Shield, X } from 'lucide-react';

const OrganizationDashboard = () => {
  const { user } = useAuth();
  const [orgData, setOrgData] = useState(null);
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [showAddUser, setShowAddUser] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'Admin'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const isAdmin = orgData?.user_role === 'Admin';

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const org = await organizationAPI.getMyOrganization();
      setOrgData(org);
      
      // Load roles
      const rolesData = await rbacAPI.getAllRoles();
      setRoles(rolesData);
      
      // Only load users if admin
      if (org.user_role === 'Admin') {
        const usersList = await organizationAPI.getOrganizationUsers();
        setUsers(usersList);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddUser = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      await organizationAPI.createUser(newUser);
      setSuccess('User added successfully!');
      setNewUser({ username: '', email: '', password: '', role: 'Admin' });
      setShowAddUser(false);
      loadData();
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add user');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to remove this user?')) {
      return;
    }
    
    try {
      await organizationAPI.deleteUser(userId);
      setSuccess('User removed successfully!');
      loadData();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to remove user');
    }
  };

  const handleAssignRoles = async (userId, roleNames) => {
    try {
      const roleIds = roles
        .filter(r => roleNames.includes(r.name))
        .map(r => r.id);
      
      await rbacAPI.assignRoles(userId, roleIds);
      setSuccess('Roles updated successfully!');
      loadData();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update roles');
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Organization Dashboard</h2>
        
        {error && (
          <div style={styles.error}>
            {error}
            <button onClick={() => setError('')} style={styles.closeBtn}>×</button>
          </div>
        )}
        {success && (
          <div style={styles.success}>
            {success}
            <button onClick={() => setSuccess('')} style={styles.closeBtn}>×</button>
          </div>
        )}
        
        {/* Organization Info */}
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Organization Information</h3>
          <div style={styles.infoGrid}>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Name:</span>
              <span style={styles.infoValue}>{orgData?.organization_name}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Your Role:</span>
              <span style={{...styles.badge, ...styles.badgeAdmin}}>{orgData?.user_role}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Total Members:</span>
              <span style={styles.infoValue}>{orgData?.user_count}</span>
            </div>
          </div>
        </div>

        {/* Admin-only: Team Management */}
        {isAdmin ? (
          <div style={styles.section}>
            <div style={styles.sectionHeader}>
              <h3 style={styles.sectionTitle}>
                <Users size={20} style={{ marginRight: '8px' }} />
                Team Members
              </h3>
              <button 
                style={styles.addButton} 
                onClick={() => setShowAddUser(!showAddUser)}
              >
                <Plus size={18} />
                {showAddUser ? 'Cancel' : 'Add Member'}
              </button>
            </div>

            {/* Add User Form */}
            {showAddUser && (
              <form onSubmit={handleAddUser} style={styles.form}>
                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>Username</label>
                    <input
                      type="text"
                      placeholder="john_doe"
                      value={newUser.username}
                      onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                      required
                      style={styles.input}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>Email</label>
                    <input
                      type="email"
                      placeholder="john@example.com"
                      value={newUser.email}
                      onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                      required
                      style={styles.input}
                    />
                  </div>
                </div>
                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>Password</label>
                    <input
                      type="password"
                      placeholder="••••••••"
                      value={newUser.password}
                      onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                      required
                      style={styles.input}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>Role</label>
                    <select
                      value={newUser.role}
                      onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                      style={styles.select}
                    >
                      {roles.map(role => (
                        <option key={role.id} value={role.name}>
                          {role.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <button type="submit" style={styles.submitButton}>
                  <Plus size={18} />
                  Create User
                </button>
              </form>
            )}

            {/* Users Table */}
            {users.length > 0 ? (
              <div style={styles.tableContainer}>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>Username</th>
                      <th style={styles.th}>Email</th>
                      <th style={styles.th}>Roles</th>
                      <th style={styles.th}>Status</th>
                      <th style={styles.th}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u.id} style={styles.tr}>
                        <td style={styles.td}>
                          <strong>{u.username}</strong>
                        </td>
                        <td style={styles.td}>{u.email}</td>
                        <td style={styles.td}>
                          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                            {u.roles?.map((role, idx) => (
                              <span 
                                key={idx} 
                                style={role === 'Admin' ? styles.badgeAdmin : styles.badgeMember}
                              >
                                {role}
                              </span>
                            ))}
                            {(!u.roles || u.roles.length === 0) && (
                              <span style={styles.badgeNone}>No Role</span>
                            )}
                          </div>
                        </td>
                        <td style={styles.td}>
                          <span style={u.is_active ? styles.statusActive : styles.statusInactive}>
                            {u.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td style={styles.td}>
                          <div style={styles.actionButtons}>
                            <button
                              onClick={() => handleDeleteUser(u.id)}
                              style={styles.deleteBtn}
                              disabled={u.id === user?.id}
                              title={u.id === user?.id ? "Cannot delete yourself" : "Remove user"}
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p style={styles.noData}>No team members found.</p>
            )}
          </div>
        ) : (
          /* Member view */
          <div style={styles.section}>
            <p style={styles.memberMessage}>
              You are a member of <strong>{orgData?.organization_name}</strong>.
            </p>
            <p style={styles.memberMessage}>
              Contact your administrator for access management.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '30px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '400px',
    fontSize: '16px',
    color: '#666',
  },
  card: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '24px',
    color: '#1a1a1a',
  },
  error: {
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  success: {
    backgroundColor: '#d1fae5',
    color: '#065f46',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  closeBtn: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    padding: '0 8px',
    color: 'inherit',
  },
  section: {
    marginBottom: '30px',
    padding: '20px',
    backgroundColor: '#f9fafb',
    borderRadius: '8px',
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: '600',
    margin: 0,
    display: 'flex',
    alignItems: 'center',
    color: '#374151',
  },
  infoGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  infoLabel: {
    fontSize: '13px',
    color: '#6b7280',
    fontWeight: '500',
  },
  infoValue: {
    fontSize: '16px',
    color: '#1f2937',
    fontWeight: '600',
  },
  badge: {
    display: 'inline-block',
    padding: '4px 12px',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '600',
    width: 'fit-content',
  },
  badgeAdmin: {
    backgroundColor: '#dbeafe',
    color: '#1e40af',
  },
  badgeMember: {
    backgroundColor: '#e0e7ff',
    color: '#4f46e5',
  },
  badgeNone: {
    display: 'inline-block',
    padding: '4px 12px',
    backgroundColor: '#f3f4f6',
    color: '#6b7280',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '500',
  },
  addButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 20px',
    backgroundColor: '#6366f1',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    transition: 'background 0.2s',
  },
  form: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    marginBottom: '20px',
    border: '2px solid #e5e7eb',
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '16px',
    marginBottom: '16px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '6px',
  },
  input: {
    padding: '10px 12px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '14px',
    transition: 'border-color 0.2s',
  },
  select: {
    padding: '10px 12px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '14px',
    backgroundColor: 'white',
    cursor: 'pointer',
  },
  submitButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    padding: '12px 24px',
    backgroundColor: '#10b981',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    width: '100%',
  },
  tableContainer: {
    overflowX: 'auto',
    backgroundColor: 'white',
    borderRadius: '8px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    padding: '12px 16px',
    textAlign: 'left',
    backgroundColor: '#f9fafb',
    borderBottom: '2px solid #e5e7eb',
    fontSize: '13px',
    fontWeight: '600',
    color: '#374151',
  },
  td: {
    padding: '12px 16px',
    borderBottom: '1px solid #e5e7eb',
    fontSize: '14px',
    color: '#1f2937',
  },
  tr: {
    transition: 'background 0.2s',
  },
  statusActive: {
    display: 'inline-block',
    padding: '4px 8px',
    backgroundColor: '#d1fae5',
    color: '#065f46',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
  },
  statusInactive: {
    display: 'inline-block',
    padding: '4px 8px',
    backgroundColor: '#fee2e2',
    color: '#991b1b',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
  },
  actionButtons: {
    display: 'flex',
    gap: '8px',
  },
  deleteBtn: {
    padding: '6px 12px',
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    transition: 'background 0.2s',
  },
  noData: {
    textAlign: 'center',
    padding: '40px',
    color: '#6b7280',
    fontSize: '14px',
  },
  memberMessage: {
    fontSize: '14px',
    color: '#4b5563',
    lineHeight: '1.6',
    margin: '8px 0',
  },
};

export default OrganizationDashboard;
