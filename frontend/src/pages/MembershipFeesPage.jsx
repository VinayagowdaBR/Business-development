import React, { useEffect, useState } from 'react';
import { Package, DollarSign, Calendar, Edit2, Trash2, X, Plus, Upload } from 'lucide-react';
import { 
  getMembershipFees, 
  addMembershipFee, 
  updateMembershipFee, 
  deleteMembershipFee,
  uploadImage 
} from '../services/membershipFeesAPI';

export default function MembershipFeesPage() {
  const [fees, setFees] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingFee, setEditingFee] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [formData, setFormData] = useState({
    package_name: '',
    base_amount: '',
    gst_percentage: 18,
    include_gst: true,
    start_date: '',
    end_date: '',
    package_image: ''
  });

  const [calculatedAmounts, setCalculatedAmounts] = useState({
    gst_amount: 0,
    total_amount: 0
  });

  useEffect(() => {
    loadFees();
  }, []);

  // Calculate GST whenever relevant fields change
  useEffect(() => {
    calculateGST();
  }, [formData.base_amount, formData.gst_percentage, formData.include_gst]);

  function calculateGST() {
    const base = parseFloat(formData.base_amount) || 0;
    const gstPercent = parseFloat(formData.gst_percentage) || 0;
    
    if (formData.include_gst) {
      const gstAmount = (base * gstPercent) / 100;
      const totalAmount = base + gstAmount;
      setCalculatedAmounts({
        gst_amount: gstAmount.toFixed(2),
        total_amount: totalAmount.toFixed(2)
      });
    } else {
      setCalculatedAmounts({
        gst_amount: 0,
        total_amount: base.toFixed(2)
      });
    }
  }

  async function loadFees() {
    try {
      const data = await getMembershipFees();
      setFees(data);
    } catch (err) {
      console.error('Error loading fees:', err);
      alert('Failed to load membership fees');
    }
  }

  async function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }

    // Validate file type
    if (!['image/jpeg', 'image/png', 'image/jpg', 'image/webp'].includes(file.type)) {
      alert('Only JPEG, PNG, and WebP images are allowed');
      return;
    }

    setUploading(true);
    try {
      const result = await uploadImage(file);
      setFormData(prev => ({ ...prev, package_image: result.url }));
      alert('Image uploaded successfully!');
    } catch (err) {
      console.error('Upload error:', err);
      alert('Failed to upload image');
    } finally {
      setUploading(false);
    }
  }

  function openAddModal() {
    setEditingFee(null);
    setFormData({
      package_name: '',
      base_amount: '',
      gst_percentage: 18,
      include_gst: true,
      start_date: '',
      end_date: '',
      package_image: ''
    });
    setShowModal(true);
  }

  function openEditModal(fee) {
    setEditingFee(fee);
    setFormData({
      package_name: fee.package_name,
      base_amount: fee.base_amount,
      gst_percentage: fee.gst_percentage,
      include_gst: fee.include_gst,
      start_date: fee.start_date,
      end_date: fee.end_date,
      package_image: fee.package_image || ''
    });
    setShowModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (editingFee) {
        await updateMembershipFee(editingFee.id, formData);
      } else {
        await addMembershipFee(formData);
      }
      setShowModal(false);
      loadFees();
    } catch (err) {
      console.error('Error saving fee:', err);
      alert('Failed to save membership fee');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this membership fee package?')) return;
    try {
      await deleteMembershipFee(id);
      loadFees();
    } catch (err) {
      console.error('Error deleting fee:', err);
      alert('Failed to delete membership fee');
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
          <Package size={32} style={{ color: '#6366f1' }} />
          <h2 style={{ fontSize: 26, fontWeight: 700, color: '#18181b', margin: 0 }}>
            Membership Fees
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
          <Plus size={20} /> Add Package
        </button>
      </div>

      {/* Fee Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: 24
      }}>
        {fees.map(fee => (
          <div
            key={fee.id}
            style={{
              background: 'white',
              borderRadius: 16,
              padding: 24,
              boxShadow: '0 2px 16px rgba(0,0,0,0.08)',
              border: '1px solid #e5e7eb'
            }}
          >
            {/* Package Image - UPDATED */}
<div style={{
  width: '100%',
  height: 200,
  borderRadius: 12,
  marginBottom: 16,
  overflow: 'hidden',
  background: fee.package_image 
    ? '#f3f4f6' 
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
}}>
  {fee.package_image ? (
    <img
      src={`http://127.0.0.1:8000${fee.package_image}`}
      alt={fee.package_name}
      style={{
        width: '100%',
        height: '100%',
        objectFit: 'cover'
      }}
      onError={(e) => {
        e.target.style.display = 'none';
        e.target.parentElement.innerHTML = `
          <div style="color: #9ca3af; font-size: 14px; text-align: center;">
            Image not found
          </div>
        `;
      }}
    />
  ) : (
    <div style={{ 
      color: 'white', 
      fontSize: 48, 
      fontWeight: 700,
      textTransform: 'uppercase'
    }}>
      {fee.package_name.charAt(0)}
    </div>
  )}
</div>


            {/* Package Name */}
            <h3 style={{ fontSize: 20, fontWeight: 700, color: '#18181b', marginBottom: 12 }}>
              {fee.package_name}
            </h3>

            {/* Amounts */}
            <div style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 14, color: '#6b7280', marginBottom: 4 }}>
                Base Amount: ₹{fee.base_amount}
              </div>
              {fee.include_gst && (
                <>
                  <div style={{ fontSize: 14, color: '#10b981', marginBottom: 4 }}>
                    GST ({fee.gst_percentage}%): ₹{fee.gst_amount}
                  </div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: '#18181b' }}>
                    Total: ₹{fee.total_amount}
                  </div>
                </>
              )}
              {!fee.include_gst && (
                <div style={{ fontSize: 20, fontWeight: 700, color: '#18181b' }}>
                  Total: ₹{fee.base_amount}
                </div>
              )}
            </div>

            {/* Dates */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14, color: '#6b7280' }}>
                <Calendar size={16} />
                <span>{fee.start_date} to {fee.end_date}</span>
              </div>
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: 8 }}>
              <button onClick={() => openEditModal(fee)} style={{
                flex: 1, background: '#f59e0b', color: 'white', border: 'none',
                borderRadius: 8, padding: '10px', fontWeight: 600, cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6
              }}>
                <Edit2 size={16} /> Edit
              </button>
              <button onClick={() => handleDelete(fee.id)} style={{
                flex: 1, background: '#ef4444', color: 'white', border: 'none',
                borderRadius: 8, padding: '10px', fontWeight: 600, cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6
              }}>
                <Trash2 size={16} /> Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center',
          justifyContent: 'center', zIndex: 1000, padding: 20
        }}>
          <div style={{
            background: 'white', borderRadius: 16, padding: 32,
            maxWidth: 600, width: '100%', maxHeight: '90vh', overflowY: 'auto'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
              <h3 style={{ fontSize: 22, fontWeight: 700, margin: 0 }}>
                {editingFee ? 'Edit Package' : 'Add Package'}
              </h3>
              <button onClick={() => setShowModal(false)} style={{
                background: 'transparent', border: 'none', cursor: 'pointer', padding: 4
              }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              {/* Package Name */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Package Name *
                </label>
                <input
                  type="text"
                  name="package_name"
                  value={formData.package_name}
                  onChange={handleChange}
                  required
                  style={{
                    width: '100%', padding: 12, border: '2px solid #e5e7eb',
                    borderRadius: 8, fontSize: 16
                  }}
                />
              </div>

              {/* Base Amount */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Base Amount (₹) *
                </label>
                <input
                  type="number"
                  name="base_amount"
                  value={formData.base_amount}
                  onChange={handleChange}
                  required
                  min="0"
                  step="0.01"
                  style={{
                    width: '100%', padding: 12, border: '2px solid #e5e7eb',
                    borderRadius: 8, fontSize: 16
                  }}
                />
              </div>

              {/* Include GST Toggle */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    name="include_gst"
                    checked={formData.include_gst}
                    onChange={handleChange}
                    style={{ width: 20, height: 20, cursor: 'pointer' }}
                  />
                  <span style={{ fontWeight: 600, fontSize: 14 }}>Include GST</span>
                </label>
              </div>

              {/* GST Percentage */}
              {formData.include_gst && (
                <div style={{ marginBottom: 16 }}>
                  <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                    GST Percentage (%)
                  </label>
                  <input
                    type="number"
                    name="gst_percentage"
                    value={formData.gst_percentage}
                    onChange={handleChange}
                    min="0"
                    max="100"
                    step="0.01"
                    style={{
                      width: '100%', padding: 12, border: '2px solid #e5e7eb',
                      borderRadius: 8, fontSize: 16
                    }}
                  />
                </div>
              )}

              {/* GST Calculation Display */}
              {formData.base_amount && (
                <div style={{
                  marginBottom: 16, padding: 16, background: '#f3f4f6',
                  borderRadius: 8, border: '1px solid #e5e7eb'
                }}>
                  <div style={{ marginBottom: 8 }}>
                    <strong>Base Amount:</strong> ₹{formData.base_amount}
                  </div>
                  {formData.include_gst && (
                    <>
                      <div style={{ marginBottom: 8, color: '#10b981' }}>
                        <strong>GST ({formData.gst_percentage}%):</strong> ₹{calculatedAmounts.gst_amount}
                      </div>
                      <div style={{ fontSize: 18, fontWeight: 700, color: '#6366f1' }}>
                        <strong>Total Amount:</strong> ₹{calculatedAmounts.total_amount}
                      </div>
                    </>
                  )}
                  {!formData.include_gst && (
                    <div style={{ fontSize: 18, fontWeight: 700, color: '#6366f1' }}>
                      <strong>Total Amount:</strong> ₹{formData.base_amount}
                    </div>
                  )}
                </div>
              )}

              {/* Start Date */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Start Date *
                </label>
                <input
                  type="date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleChange}
                  required
                  style={{
                    width: '100%', padding: 12, border: '2px solid #e5e7eb',
                    borderRadius: 8, fontSize: 16
                  }}
                />
              </div>

              {/* End Date */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  End Date *
                </label>
                <input
                  type="date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  required
                  style={{
                    width: '100%', padding: 12, border: '2px solid #e5e7eb',
                    borderRadius: 8, fontSize: 16
                  }}
                />
              </div>

              {/* Image Upload */}
              <div style={{ marginBottom: 24 }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 8, fontSize: 14 }}>
                  Package Image (Max 10MB)
                </label>
                <div style={{
                  border: '2px dashed #e5e7eb', borderRadius: 8, padding: 20,
                  textAlign: 'center', cursor: 'pointer', position: 'relative'
                }}>
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/jpg,image/webp"
                    onChange={handleImageUpload}
                    style={{
                      position: 'absolute', top: 0, left: 0, width: '100%',
                      height: '100%', opacity: 0, cursor: 'pointer'
                    }}
                  />
                  <Upload size={32} style={{ margin: '0 auto 8px', color: '#6366f1' }} />
                  <div style={{ fontWeight: 600, marginBottom: 4 }}>
                    {uploading ? 'Uploading...' : 'Click to upload image'}
                  </div>
                  <div style={{ fontSize: 12, color: '#6b7280' }}>
                    JPEG, PNG, WebP (Max 10MB)
                  </div>
                  {formData.package_image && (
                    <div style={{ marginTop: 12, fontSize: 14, color: '#10b981' }}>
                      ✓ Image uploaded
                    </div>
                  )}
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                style={{
                  width: '100%',
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  color: 'white', border: 'none', borderRadius: 10,
                  padding: 14, fontWeight: 600, fontSize: 16, cursor: 'pointer'
                }}
              >
                {editingFee ? 'Update Package' : 'Create Package'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
