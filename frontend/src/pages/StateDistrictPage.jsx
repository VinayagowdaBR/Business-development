import React, { useState, useEffect } from 'react';
import { Map, MapPin, Search, Plus, Trash2, Edit } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

const StateDistrictPage = () => {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // State form
  const [stateName, setStateName] = useState('');
  const [stateCode, setStateCode] = useState('');
  const [stateDesc, setStateDesc] = useState('');
  
  // District form
  const [districtName, setDistrictName] = useState('');
  const [districtPrefix, setDistrictPrefix] = useState('');
  const [districtStateId, setDistrictStateId] = useState('');
  const [districtDesc, setDistrictDesc] = useState('');

  // Filters
  const [filterStateId, setFilterStateId] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    fetchDistricts();
  }, [filterStateId]);

  const loadData = async () => {
    try {
      setLoading(true);
      await Promise.all([fetchStates(), fetchDistricts()]);
    } catch (err) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const fetchStates = async () => {
    try {
      const response = await axios.get(`${API_BASE}/states/`);
      setStates(response.data);
    } catch (error) {
      console.error('Error fetching states:', error);
    }
  };

  const fetchDistricts = async () => {
    try {
      const url = filterStateId 
        ? `${API_BASE}/districts/?state_id=${filterStateId}`
        : `${API_BASE}/districts/`;
      const response = await axios.get(url);
      setDistricts(response.data);
    } catch (error) {
      console.error('Error fetching districts:', error);
    }
  };

  const handleCreateState = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', stateName);
    formData.append('code', stateCode);
    if (stateDesc) formData.append('description', stateDesc);

    try {
      await axios.post(`${API_BASE}/states/`, formData);
      setStateName('');
      setStateCode('');
      setStateDesc('');
      fetchStates();
      setError('');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error creating state');
    }
  };

  const handleCreateDistrict = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', districtName);
    formData.append('prefix', districtPrefix);
    formData.append('state_id', districtStateId);
    if (districtDesc) formData.append('description', districtDesc);

    try {
      await axios.post(`${API_BASE}/districts/`, formData);
      setDistrictName('');
      setDistrictPrefix('');
      setDistrictStateId('');
      setDistrictDesc('');
      fetchDistricts();
      setError('');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error creating district');
    }
  };

  const handleDeleteState = async (stateId) => {
    if (!confirm('Are you sure you want to delete this state?')) return;
    
    try {
      await axios.delete(`${API_BASE}/states/${stateId}`);
      fetchStates();
      fetchDistricts();
    } catch (error) {
      setError(error.response?.data?.detail || 'Error deleting state');
    }
  };

  const handleDeleteDistrict = async (districtId) => {
    if (!confirm('Are you sure you want to delete this district?')) return;
    
    try {
      await axios.delete(`${API_BASE}/districts/${districtId}`);
      fetchDistricts();
    } catch (error) {
      setError(error.response?.data?.detail || 'Error deleting district');
    }
  };

  const filteredStates = states.filter(state =>
    state.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    state.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredDistricts = districts.filter(district =>
    district.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    district.prefix.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>
            <Map size={28} style={{ marginRight: '12px' }} />
            State & District Management
          </h2>
          <p style={styles.subtitle}>
            {states.length} States • {districts.length} Districts
          </p>
        </div>
      </div>

      {error && (
        <div style={styles.error}>
          {error}
          <button onClick={() => setError('')} style={styles.closeBtn}>×</button>
        </div>
      )}

      {/* Create Forms */}
      <div style={styles.formsGrid}>
        {/* Create State Form */}
        <div style={styles.formCard}>
          <div style={styles.formHeader}>
            <Map size={20} style={{ marginRight: '8px', color: '#6366f1' }} />
            <h3 style={styles.formTitle}>Create State</h3>
          </div>
          <form onSubmit={handleCreateState} style={styles.form}>
            <div style={styles.formGroup}>
              <label style={styles.label}>State Name *</label>
              <input
                type="text"
                placeholder="e.g., Maharashtra"
                value={stateName}
                onChange={(e) => setStateName(e.target.value)}
                required
                style={styles.input}
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>State Code *</label>
              <input
                type="text"
                placeholder="e.g., MH"
                value={stateCode}
                onChange={(e) => setStateCode(e.target.value.toUpperCase())}
                required
                maxLength="10"
                style={styles.input}
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Description</label>
              <textarea
                placeholder="Optional description"
                value={stateDesc}
                onChange={(e) => setStateDesc(e.target.value)}
                rows="3"
                style={styles.textarea}
              />
            </div>
            
            <button type="submit" style={styles.submitBtn}>
              <Plus size={18} style={{ marginRight: '6px' }} />
              Create State
            </button>
          </form>
        </div>

        {/* Create District Form */}
        <div style={styles.formCard}>
          <div style={styles.formHeader}>
            <MapPin size={20} style={{ marginRight: '8px', color: '#10b981' }} />
            <h3 style={styles.formTitle}>Create District</h3>
          </div>
          <form onSubmit={handleCreateDistrict} style={styles.form}>
            <div style={styles.formGroup}>
              <label style={styles.label}>District Name *</label>
              <input
                type="text"
                placeholder="e.g., Pune"
                value={districtName}
                onChange={(e) => setDistrictName(e.target.value)}
                required
                style={styles.input}
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>District Prefix *</label>
              <input
                type="text"
                placeholder="e.g., MH_PUNE"
                value={districtPrefix}
                onChange={(e) => setDistrictPrefix(e.target.value.toUpperCase())}
                required
                style={styles.input}
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Select State *</label>
              <select
                value={districtStateId}
                onChange={(e) => setDistrictStateId(e.target.value)}
                required
                style={styles.select}
              >
                <option value="">-- Choose State --</option>
                {states.map(state => (
                  <option key={state.id} value={state.id}>
                    {state.name} ({state.code})
                  </option>
                ))}
              </select>
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Description</label>
              <textarea
                placeholder="Optional description"
                value={districtDesc}
                onChange={(e) => setDistrictDesc(e.target.value)}
                rows="3"
                style={styles.textarea}
              />
            </div>
            
            <button type="submit" style={{...styles.submitBtn, backgroundColor: '#10b981'}}>
              <Plus size={18} style={{ marginRight: '6px' }} />
              Create District
            </button>
          </form>
        </div>
      </div>

      {/* Search Bar */}
      <div style={styles.searchContainer}>
        <Search size={20} style={styles.searchIcon} />
        <input
          type="text"
          placeholder="Search states and districts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={styles.searchInput}
        />
        <select
          value={filterStateId}
          onChange={(e) => setFilterStateId(e.target.value)}
          style={styles.filterSelect}
        >
          <option value="">All States</option>
          {states.map(state => (
            <option key={state.id} value={state.id}>{state.name}</option>
          ))}
        </select>
      </div>

      {/* States Grid */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>States ({filteredStates.length})</h3>
        <div style={styles.cardsGrid}>
          {filteredStates.length > 0 ? (
            filteredStates.map((state) => (
              <div key={state.id} style={styles.card}>
                <div style={styles.cardHeader}>
                  <div style={{...styles.avatar, background: 'linear-gradient(135deg, #6366f1, #8b5cf6)'}}>
                    <Map size={24} color="white" />
                  </div>
                  <div style={styles.cardInfo}>
                    <h3 style={styles.cardName}>{state.name}</h3>
                    <span style={styles.codeBadge}>{state.code}</span>
                  </div>
                </div>

                <div style={styles.cardDetails}>
                  <div style={styles.detailItem}>
                    <div style={styles.detailLabel}>Description</div>
                    <div style={styles.detailValue}>{state.description || 'No description'}</div>
                  </div>

                  <div style={styles.cardFooter}>
                    <span style={state.is_active ? styles.statusActive : styles.statusInactive}>
                      ● {state.is_active ? 'Active' : 'Inactive'}
                    </span>
                    <button 
                      onClick={() => handleDeleteState(state.id)}
                      style={styles.deleteBtn}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div style={styles.noResults}>
              <Map size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
              <p>No states found</p>
            </div>
          )}
        </div>
      </div>

      {/* Districts Grid */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Districts ({filteredDistricts.length})</h3>
        <div style={styles.cardsGrid}>
          {filteredDistricts.length > 0 ? (
            filteredDistricts.map((district) => {
              const state = states.find(s => s.id === district.state_id);
              return (
                <div key={district.id} style={styles.card}>
                  <div style={styles.cardHeader}>
                    <div style={{...styles.avatar, background: 'linear-gradient(135deg, #10b981, #059669)'}}>
                      <MapPin size={24} color="white" />
                    </div>
                    <div style={styles.cardInfo}>
                      <h3 style={styles.cardName}>{district.name}</h3>
                      <span style={{...styles.codeBadge, backgroundColor: '#d1fae5', color: '#065f46'}}>
                        {district.prefix}
                      </span>
                    </div>
                  </div>

                  <div style={styles.cardDetails}>
                    <div style={styles.detailItem}>
                      <div style={styles.detailLabel}>State</div>
                      <div style={styles.detailValue}>{state?.name || `State #${district.state_id}`}</div>
                    </div>

                    <div style={styles.detailItem}>
                      <div style={styles.detailLabel}>Description</div>
                      <div style={styles.detailValue}>{district.description || 'No description'}</div>
                    </div>

                    <div style={styles.cardFooter}>
                      <span style={district.is_active ? styles.statusActive : styles.statusInactive}>
                        ● {district.is_active ? 'Active' : 'Inactive'}
                      </span>
                      <button 
                        onClick={() => handleDeleteDistrict(district.id)}
                        style={styles.deleteBtn}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div style={styles.noResults}>
              <MapPin size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
              <p>No districts found</p>
            </div>
          )}
        </div>
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
  formsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
    gap: '24px',
    marginBottom: '30px',
  },
  formCard: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
  formHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '20px',
    paddingBottom: '16px',
    borderBottom: '1px solid #f0f0f0',
  },
  formTitle: {
    fontSize: '18px',
    fontWeight: '600',
    margin: 0,
    color: '#1f2937',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '13px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '6px',
  },
  input: {
    padding: '10px 12px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  },
  select: {
    padding: '10px 12px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px',
    backgroundColor: 'white',
    cursor: 'pointer',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  },
  textarea: {
    padding: '10px 12px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px',
    resize: 'none',
    fontFamily: 'inherit',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  },
  submitBtn: {
    padding: '12px',
    backgroundColor: '#6366f1',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'background-color 0.2s',
  },
  searchContainer: {
    position: 'relative',
    marginBottom: '30px',
    display: 'flex',
    gap: '12px',
  },
  searchIcon: {
    position: 'absolute',
    left: '16px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#9ca3af',
    pointerEvents: 'none',
  },
  searchInput: {
    flex: 1,
    padding: '12px 16px 12px 48px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    fontSize: '14px',
    backgroundColor: 'white',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  },
  filterSelect: {
    padding: '12px 16px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    fontSize: '14px',
    backgroundColor: 'white',
    cursor: 'pointer',
    minWidth: '200px',
  },
  section: {
    marginBottom: '40px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: '20px',
  },
  cardsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '24px',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  cardHeader: {
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
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  cardInfo: {
    flex: 1,
    minWidth: 0,
  },
  cardName: {
    fontSize: '18px',
    fontWeight: '600',
    margin: '0 0 6px 0',
    color: '#1f2937',
  },
  codeBadge: {
    display: 'inline-block',
    padding: '4px 10px',
    backgroundColor: '#e0e7ff',
    color: '#4f46e5',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '600',
  },
  cardDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  detailItem: {
    display: 'flex',
    flexDirection: 'column',
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
  cardFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: '8px',
  },
  statusActive: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#10b981',
  },
  statusInactive: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#ef4444',
  },
  deleteBtn: {
    background: 'none',
    border: 'none',
    color: '#ef4444',
    cursor: 'pointer',
    padding: '8px',
    borderRadius: '6px',
    transition: 'background-color 0.2s',
    display: 'flex',
    alignItems: 'center',
  },
  noResults: {
    gridColumn: '1 / -1',
    textAlign: 'center',
    padding: '60px 20px',
    color: '#6b7280',
  },
};

export default StateDistrictPage;
