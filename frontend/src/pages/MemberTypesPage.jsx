import React, { useEffect, useState } from 'react';
import { Users, Edit2, Trash2, X, Plus, Tag } from 'lucide-react';
import {
  getMemberTypes,
  createMemberType,
  updateMemberType,
  deleteMemberType
} from '../services/memberTypesAPI';

export default function MemberTypesPage() {
  const [memberTypes, setMemberTypes] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingType, setEditingType] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    is_active: true
  });

  useEffect(() => {
    loadMemberTypes();
  }, []);

  async function loadMemberTypes() {
    try {
      const data = await getMemberTypes();
      setMemberTypes(data);
    } catch (err) {
      console.error('Error loading member types:', err);
      alert('Failed to load member types');
    }
  }

  function openAddModal() {
    setEditingType(null);
    setFormData({ name: '', code: '', description: '', is_active: true });
    setShowModal(true);
  }

  function openEditModal(type) {
    setEditingType(type);
    setFormData({
      name: type.name,
      code: type.code,
      description: type.description || '',
      is_active: type.is_active
    });
    setShowModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (editingType) {
        await updateMemberType(editingType.id, formData);
      } else {
        await createMemberType(formData);
      }
      setShowModal(false);
      loadMemberTypes();
    } catch (err) {
      console.error('Error saving member type:', err);
      alert(err.response?.data?.detail || 'Failed to save member type');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this member type?')) return;
    try {
      await deleteMemberType(id);
      loadMemberTypes();
    } catch (err) {
      console.error('Error deleting member type:', err);
      alert('Failed to delete member type');
    }
  }

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 24 }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Tag size={32} style={{ color: '#6366f1' }} />
          <h2 style={{ fontSize: 26, fontWeight: 700, color: '#18181b', margin: 0 }}>
            Member Types
          </h2>
        </div>
        <button
          onClick={openAddModal}
          style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            color: 'white',
            border: 'none',
            borderRadius: 10,
            padding: '12px 24px',
            fontWeight: 600,
            fontSize: 16,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)'
          }}
        >
          <Plus size={20} /> Add Member Type
        </button>
      </div>

      {/* Member Types Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: 24
      }}>
        {memberTypes.map(type => (
          <div
            key={type.id}
            style={{
              background: 'white',
              borderRadius: 16,
              padding: 24,
              boxShadow: '0 2px 16px rgba(0,0,0,0.08)',
              border: '1px solid #e5e7eb',
              position: 'relative'
            }}
          >
            {/* Active Badge */}
            {type.is_active && (
              <div style={{
                position: 'absolute',
                top: 16,
                right: 16,
                background: '#10b981',
                color: 'white',
                padding: '4px 12px',
                borderRadius: 20,
                fontSize: 12,
                fontWeight: 600
              }}>
                Active
              </div>
            )}

            {/* Type Icon */}
            <div style={{
              width: 60,
              height: 60,
              borderRadius: 12,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: 16
            }}>
              <Users size={32} color="white" />
            </div>

            {/* Type Name */}
            <h3 style={{ fontSize: 20, fontWeight: 700, color: '#18181b', marginBottom: 8 }}>
              {type.name}
            </h3>

            {/* Type Code */}
            <div style={{
              display: 'inline-block',
              background: '#f3f4f6',
              color: '#6b7280',
              padding: '4px 12px',
              borderRadius: 6,
              fontSize: 14,
              fontWeight: 600,
              marginBottom: 12
            }}>
              {type.code}
            </div>

            {/* Description */}
            {type.description && (
              <p style={{ fontSize: 14, color: '#6b7280', marginBottom: 16 }}>
                {type.description}
              </p>
            )}

            {/* Actions */}
            <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
              <button
                onClick={() => openEditModal(type)}
                style={{
                  flex: 1,
                  background: '#f59e0b',
                  color: 'white',
                  border: 'none',
                  borderRadius: 8,
                  padding: '10px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 6
                }}
              >
                <Edit2 size={16} /> Edit
              </button>
              <button
                onClick={() => handleDelete(type.id)}
                style={{
                  flex: 1,
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: 8,
                  padding: '10px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 6
                }}
              >
                <Trash2 size={16} /> Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div style={{
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
          padding: 20
        }}>
          <div style={{
            background: 'white',
            borderRadius: 16,
            padding: 32,
            maxWidth: 500,
            width: '100%'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
              <h3 style={{ fontSize: 22, fontWeight: 700, margin: 0 }}>
                {editingType ? 'Edit Member Type' : 'Add Member Type'}
              </h3>
              <button
                onClick={() => setShowModal(false)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: 4 }}
              >
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              {/* Name */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  placeholder="e.g., Visitors"
                  style={{
                    width: '100%',
                    padding: 12,
                    border: '2px solid #e5e7eb',
                    borderRadius: 8,
                    fontSize: 16
                  }}
                />
              </div>

              {/* Code */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Code * (Unique identifier)
                </label>
                <input
                  type="text"
                  name="code"
                  value={formData.code}
                  onChange={handleChange}
                  required
                  placeholder="e.g., VIS"
                  maxLength={10}
                  style={{
                    width: '100%',
                    padding: 12,
                    border: '2px solid #e5e7eb',
                    borderRadius: 8,
                    fontSize: 16,
                    textTransform: 'uppercase'
                  }}
                />
              </div>

              {/* Description */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Brief description of this member type"
                  rows={3}
                  style={{
                    width: '100%',
                    padding: 12,
                    border: '2px solid #e5e7eb',
                    borderRadius: 8,
                    fontSize: 16,
                    resize: 'vertical'
                  }}
                />
              </div>

              {/* Is Active */}
              <div style={{ marginBottom: 24 }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleChange}
                    style={{ width: 20, height: 20, cursor: 'pointer' }}
                  />
                  <span style={{ fontWeight: 600, fontSize: 14 }}>Active</span>
                </label>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                style={{
                  width: '100%',
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  color: 'white',
                  border: 'none',
                  borderRadius: 10,
                  padding: 14,
                  fontWeight: 600,
                  fontSize: 16,
                  cursor: 'pointer'
                }}
              >
                {editingType ? 'Update Member Type' : 'Create Member Type'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
