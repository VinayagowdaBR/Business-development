import React, { useState, useEffect } from 'react';
import { Users, Mail, Calendar, Shield, Search } from 'lucide-react';
import { organizationAPI } from '../services/api';

const MembersList = () => {
  const [members, setMembers] = useState([]);
  const [orgData, setOrgData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    try {
      setLoading(true);
      const [org, users] = await Promise.all([
        organizationAPI.getMyOrganization(),
        organizationAPI.getOrganizationUsers()
      ]);
      setOrgData(org);
      setMembers(users);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load members');
    } finally {
      setLoading(false);
    }
  };

  const filteredMembers = members.filter(member =>
    member.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div style={styles.loading}>Loading members...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>
            <Users size={28} style={{ marginRight: '12px' }} />
            Organization Members
          </h2>
          <p style={styles.subtitle}>
            {orgData?.organization_name} • {members.length} total members
          </p>
        </div>
      </div>

      {error && (
        <div style={styles.error}>
          {error}
          <button onClick={() => setError('')} style={styles.closeBtn}>×</button>
        </div>
      )}

      {/* Search Bar */}
      <div style={styles.searchContainer}>
        <Search size={20} style={styles.searchIcon} />
        <input
          type="text"
          placeholder="Search members by name or email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={styles.searchInput}
        />
      </div>

      {/* Members Grid */}
      <div style={styles.membersGrid}>
        {filteredMembers.length > 0 ? (
          filteredMembers.map((member) => (
            <div key={member.id} style={styles.memberCard}>
              <div style={styles.memberHeader}>
                <div style={styles.avatar}>
                  {member.username.charAt(0).toUpperCase()}
                </div>
                <div style={styles.memberInfo}>
                  <h3 style={styles.memberName}>{member.username}</h3>
                  <div style={styles.memberEmail}>
                    <Mail size={14} style={{ marginRight: '6px' }} />
                    {member.email}
                  </div>
                </div>
              </div>

              <div style={styles.memberDetails}>
                <div style={styles.detailItem}>
                  <Shield size={16} style={styles.detailIcon} />
                  <div>
                    <div style={styles.detailLabel}>Roles</div>
                    <div style={styles.rolesContainer}>
                      {member.roles?.length > 0 ? (
                        member.roles.map((role, idx) => (
                          <span key={idx} style={styles.roleBadge}>
                            {role}
                          </span>
                        ))
                      ) : (
                        <span style={styles.noRole}>No role assigned</span>
                      )}
                    </div>
                  </div>
                </div>

                <div style={styles.detailItem}>
                  <Calendar size={16} style={styles.detailIcon} />
                  <div>
                    <div style={styles.detailLabel}>Joined</div>
                    <div style={styles.detailValue}>
                      {new Date(member.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                <div style={styles.statusContainer}>
                  <span style={member.is_active ? styles.statusActive : styles.statusInactive}>
                    {member.is_active ? '● Active' : '● Inactive'}
                  </span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div style={styles.noResults}>
            <Users size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
            <p>No members found matching "{searchTerm}"</p>
          </div>
        )}
      </div>
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
    marginBottom: '30px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    margin: '0 0 8px 0',
    color: '#1a1a1a',
    display: 'flex',
    alignItems: 'center',
  },
  subtitle: {
    fontSize: '14px',
    color: '#666',
    margin: 0,
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
  closeBtn: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    padding: '0 8px',
    color: 'inherit',
  },
  searchContainer: {
    position: 'relative',
    marginBottom: '30px',
  },
  searchIcon: {
    position: 'absolute',
    left: '16px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#9ca3af',
  },
  searchInput: {
    width: '100%',
    padding: '12px 16px 12px 48px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    fontSize: '14px',
    backgroundColor: 'white',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  },
  membersGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '24px',
  },
  memberCard: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'default',
  },
  memberHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    marginBottom: '20px',
    paddingBottom: '20px',
    borderBottom: '1px solid #f0f0f0',
  },
  avatar: {
    width: '56px',
    height: '56px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '24px',
    fontWeight: 'bold',
    color: 'white',
    flexShrink: 0,
  },
  memberInfo: {
    flex: 1,
    minWidth: 0,
  },
  memberName: {
    fontSize: '18px',
    fontWeight: '600',
    margin: '0 0 6px 0',
    color: '#1f2937',
  },
  memberEmail: {
    fontSize: '13px',
    color: '#6b7280',
    display: 'flex',
    alignItems: 'center',
  },
  memberDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  detailItem: {
    display: 'flex',
    gap: '12px',
  },
  detailIcon: {
    color: '#9ca3af',
    marginTop: '2px',
    flexShrink: 0,
  },
  detailLabel: {
    fontSize: '12px',
    color: '#6b7280',
    fontWeight: '500',
    marginBottom: '4px',
  },
  detailValue: {
    fontSize: '14px',
    color: '#1f2937',
    fontWeight: '500',
  },
  rolesContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '6px',
  },
  roleBadge: {
    display: 'inline-block',
    padding: '4px 10px',
    backgroundColor: '#e0e7ff',
    color: '#4f46e5',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '600',
  },
  noRole: {
    fontSize: '13px',
    color: '#9ca3af',
    fontStyle: 'italic',
  },
  statusContainer: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  statusActive: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#10b981',
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  statusInactive: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#ef4444',
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  noResults: {
    gridColumn: '1 / -1',
    textAlign: 'center',
    padding: '60px 20px',
    color: '#6b7280',
  },
};

export default MembersList;
