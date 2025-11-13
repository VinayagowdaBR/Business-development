import React, { useState, useEffect } from 'react';
import { Shield, Plus, Edit, Trash2, X, Check } from 'lucide-react';
import { rbacAPI } from '../services/api';

const RoleManagement = () => {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingRole, setEditingRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    permission_ids: []
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rolesData, permsData] = await Promise.all([
        rbacAPI.getAllRoles(),
        rbacAPI.getAllPermissions()
      ]);
      setRoles(rolesData);
      setPermissions(permsData);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRole = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      if (editingRole) {
        await rbacAPI.updateRole(editingRole.id, formData);
        setSuccess('Role updated successfully!');
      } else {
        await rbacAPI.createRole(formData);
        setSuccess('Role created successfully!');
      }
      
      setShowCreateModal(false);
      setEditingRole(null);
      setFormData({ name: '', description: '', permission_ids: [] });
      loadData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save role');
    }
  };

  const handleEditRole = (role) => {
    setEditingRole(role);
    setFormData({
      name: role.name,
      description: role.description || '',
      permission_ids: role.permissions.map(p => p.id)
    });
    setShowCreateModal(true);
  };

  const handleDeleteRole = async (roleId) => {
    if (!window.confirm('Are you sure you want to delete this role?')) return;
    
    try {
      await rbacAPI.deleteRole(roleId);
      setSuccess('Role deleted successfully!');
      loadData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete role');
    }
  };

  const togglePermission = (permId) => {
    setFormData(prev => ({
      ...prev,
      permission_ids: prev.permission_ids.includes(permId)
        ? prev.permission_ids.filter(id => id !== permId)
        : [...prev.permission_ids, permId]
    }));
  };

  const closeModal = () => {
    setShowCreateModal(false);
    setEditingRole(null);
    setFormData({ name: '', description: '', permission_ids: [] });
  };

  // Group permissions by resource
  const groupedPermissions = permissions.reduce((acc, perm) => {
    if (!acc[perm.resource]) acc[perm.resource] = [];
    acc[perm.resource].push(perm);
    return acc;
  }, {});

  if (loading) {
    return <div style={styles.loading}>Loading roles...</div>;
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>Role Management</h2>
          <p style={styles.subtitle}>Create and manage roles with custom permissions</p>
        </div>
        <button onClick={() => setShowCreateModal(true)} style={styles.createButton}>
          <Plus size={20} /> Create Role
        </button>
      </div>

      {/* Alerts */}
      {error && (
        <div style={styles.error}>
          {error}
          <button onClick={() => setError('')} style={styles.closeAlert}>×</button>
        </div>
      )}
      {success && (
        <div style={styles.success}>
          {success}
          <button onClick={() => setSuccess('')} style={styles.closeAlert}>×</button>
        </div>
      )}

      {/* Roles Grid */}
      <div style={styles.rolesGrid}>
        {roles.map(role => (
          <div key={role.id} style={styles.roleCard}>
            <div style={styles.roleHeader}>
              <Shield size={24} color="#6366f1" />
              <div style={{ flex: 1 }}>
                <h3 style={styles.roleName}>{role.name}</h3>
                {role.is_system_role && (
                  <span style={styles.systemBadge}>System Role</span>
                )}
              </div>
            </div>
            
            <p style={styles.roleDescription}>
              {role.description || 'No description provided'}
            </p>
            
            <div style={styles.permissionsList}>
              <strong style={styles.permissionsTitle}>
                Permissions ({role.permissions?.length || 0})
              </strong>
              <div style={styles.permissionTags}>
                {role.permissions?.slice(0, 6).map((perm, idx) => (
                  <span key={idx} style={styles.permissionBadge}>
                    {perm.resource}:{perm.action}
                  </span>
                ))}
                {role.permissions?.length > 6 && (
                  <span style={styles.permissionBadge}>
                    +{role.permissions.length - 6} more
                  </span>
                )}
              </div>
            </div>
            
            {!role.is_system_role && (
              <div style={styles.roleActions}>
                <button onClick={() => handleEditRole(role)} style={styles.editButton}>
                  <Edit size={16} /> Edit
                </button>
                <button onClick={() => handleDeleteRole(role.id)} style={styles.deleteButton}>
                  <Trash2 size={16} /> Delete
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Create/Edit Role Modal */}
      {showCreateModal && (
        <div style={styles.modal} onClick={closeModal}>
          <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <div style={styles.modalHeader}>
              <h3>{editingRole ? 'Edit Role' : 'Create New Role'}</h3>
              <button onClick={closeModal} style={styles.closeButton}>
                <X size={24} />
              </button>
            </div>
            
            <form onSubmit={handleCreateRole}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Role Name *</label>
                <input
                  type="text"
                  placeholder="e.g., Sales Manager"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                  style={styles.input}
                />
              </div>
              
              <div style={styles.formGroup}>
                <label style={styles.label}>Description</label>
                <textarea
                  placeholder="Brief description of this role..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  style={styles.textarea}
                  rows="3"
                />
              </div>
              
              <div style={styles.formGroup}>
                <label style={styles.label}>Permissions</label>
                <div style={styles.permissionsContainer}>
                  {Object.entries(groupedPermissions).map(([resource, perms]) => (
                    <div key={resource} style={styles.permissionGroup}>
                      <div style={styles.resourceHeader}>
                        <strong style={styles.resourceName}>{resource}</strong>
                      </div>
                      {perms.map(perm => (
                        <label key={perm.id} style={styles.checkboxLabel}>
                          <input
                            type="checkbox"
                            checked={formData.permission_ids.includes(perm.id)}
                            onChange={() => togglePermission(perm.id)}
                            style={styles.checkbox}
                          />
                          <div>
                            <strong>{perm.action}</strong>
                            <span style={styles.permDesc}> - {perm.description}</span>
                          </div>
                        </label>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
              
              <div style={styles.modalActions}>
                <button type="button" onClick={closeModal} style={styles.cancelButton}>
                  Cancel
                </button>
                <button type="submit" style={styles.submitButton}>
                  <Check size={18} />
                  {editingRole ? 'Update Role' : 'Create Role'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '30px',
    maxWidth: '1400px',
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
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    margin: '0 0 5px 0',
    color: '#1a1a1a',
  },
  subtitle: {
    color: '#666',
    margin: 0,
    fontSize: '14px',
  },
  createButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 24px',
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)',
    transition: 'transform 0.2s',
  },
  error: {
    background: '#fee2e2',
    color: '#dc2626',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  success: {
    background: '#d1fae5',
    color: '#065f46',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  closeAlert: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    padding: '0 8px',
    color: 'inherit',
  },
  rolesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '24px',
  },
  roleCard: {
    background: 'white',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'default',
  },
  roleHeader: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    marginBottom: '12px',
  },
  roleName: {
    fontSize: '18px',
    fontWeight: '600',
    margin: '0 0 4px 0',
    color: '#1a1a1a',
  },
  systemBadge: {
    display: 'inline-block',
    padding: '3px 8px',
    background: '#fef3c7',
    color: '#92400e',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  roleDescription: {
    color: '#666',
    fontSize: '14px',
    marginBottom: '16px',
    lineHeight: '1.5',
  },
  permissionsList: {
    marginBottom: '16px',
  },
  permissionsTitle: {
    fontSize: '13px',
    color: '#666',
    display: 'block',
    marginBottom: '8px',
  },
  permissionTags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '6px',
  },
  permissionBadge: {
    display: 'inline-block',
    padding: '4px 10px',
    background: '#e0e7ff',
    color: '#4f46e5',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '500',
  },
  roleActions: {
    display: 'flex',
    gap: '8px',
    paddingTop: '12px',
    borderTop: '1px solid #f0f0f0',
  },
  editButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    padding: '8px 16px',
    background: '#f3f4f6',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '500',
    color: '#374151',
    flex: 1,
    justifyContent: 'center',
    transition: 'background 0.2s',
  },
  deleteButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    padding: '8px 16px',
    background: '#fee2e2',
    color: '#dc2626',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '500',
    flex: 1,
    justifyContent: 'center',
    transition: 'background 0.2s',
  },
  modal: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
    backdropFilter: 'blur(4px)',
  },
  modalContent: {
    background: 'white',
    borderRadius: '16px',
    width: '90%',
    maxWidth: '700px',
    maxHeight: '85vh',
    overflowY: 'auto',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  modalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '24px 24px 16px',
    borderBottom: '1px solid #e5e5e5',
  },
  closeButton: {
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '4px',
    color: '#666',
    borderRadius: '6px',
    transition: 'background 0.2s',
  },
  formGroup: {
    padding: '20px 24px',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#374151',
  },
  input: {
    width: '100%',
    padding: '10px 12px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '14px',
    boxSizing: 'border-box',
    transition: 'border-color 0.2s',
  },
  textarea: {
    width: '100%',
    padding: '10px 12px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '14px',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
    resize: 'vertical',
  },
  permissionsContainer: {
    maxHeight: '400px',
    overflowY: 'auto',
    border: '1px solid #e5e5e5',
    borderRadius: '8px',
    padding: '12px',
  },
  permissionGroup: {
    marginBottom: '16px',
    padding: '12px',
    background: '#f9fafb',
    borderRadius: '8px',
  },
  resourceHeader: {
    marginBottom: '12px',
    paddingBottom: '8px',
    borderBottom: '2px solid #e5e5e5',
  },
  resourceName: {
    color: '#1f2937',
    textTransform: 'capitalize',
    fontSize: '14px',
    fontWeight: '600',
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '10px',
    padding: '8px',
    marginBottom: '4px',
    cursor: 'pointer',
    borderRadius: '6px',
    transition: 'background 0.2s',
    fontSize: '14px',
  },
  checkbox: {
    marginTop: '2px',
    cursor: 'pointer',
  },
  permDesc: {
    color: '#6b7280',
  },
  modalActions: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'flex-end',
    padding: '16px 24px 24px',
    borderTop: '1px solid #e5e5e5',
  },
  cancelButton: {
    padding: '10px 20px',
    background: '#f3f4f6',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
  },
  submitButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 24px',
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
};

export default RoleManagement;
