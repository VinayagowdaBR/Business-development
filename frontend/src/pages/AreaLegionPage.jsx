import React, { useEffect, useState } from 'react';
import { getAreas, addArea, updateArea, deleteArea, getLegions, addLegion, deleteLegion } from '../services/areaLegionAPI';
import { Plus, X, Trash2, Edit2, MapPin } from 'lucide-react';

export default function AreaLegionPage() {
  const [areas, setAreas] = useState([]);
  const [legions, setLegions] = useState([]);
  const [areaName, setAreaName] = useState('');
  const [editingArea, setEditingArea] = useState(null);
  const [legionForm, setLegionForm] = useState({ name: '', prefix: '', area_id: '' });
  const [legionAddRow, setLegionAddRow] = useState(null);

  useEffect(() => {
    loadAll();
  }, []);

  async function loadAll() {
    setAreas(await getAreas());
    setLegions(await getLegions());
    setLegionForm({ name: '', prefix: '', area_id: '' });
    setLegionAddRow(null);
  }

  async function handleAddArea(e) {
    e.preventDefault();
    if (!areaName.trim()) return;
    await addArea({ name: areaName.trim() });
    setAreaName('');
    loadAll();
  }
  async function handleEditArea(area) {
    setEditingArea(area.id);
    setAreaName(area.name);
  }
  async function handleUpdateArea(e) {
    e.preventDefault();
    await updateArea(editingArea, { name: areaName.trim() });
    setEditingArea(null);
    setAreaName('');
    loadAll();
  }
  async function handleDeleteArea(id) {
    if (window.confirm('Delete this area and all its legions?')) {
      await deleteArea(id);
      loadAll();
    }
  }
  async function handleAddLegion(area_id) {
    if (!legionForm.name || !legionForm.prefix) return;
    await addLegion({ ...legionForm, area_id });
    setLegionForm({ name: '', prefix: '', area_id: '' });
    setLegionAddRow(null);
    loadAll();
  }
  async function handleDeleteLegion(legion_id) {
    if (window.confirm('Delete this legion?')) {
      await deleteLegion(legion_id);
      loadAll();
    }
  }
  const legionsByArea = areaId => legions.filter(l => l.area_id === areaId);

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32 }}>
        <MapPin size={32} style={{ color: '#6366f1' }} />
        <h2 style={{ fontSize: 26, fontWeight: 700, color: '#18181b', letterSpacing: 1 }}>
          Areas & Their Legions
        </h2>
      </div>
      <div style={{
        background: 'white', borderRadius: 16,
        boxShadow: '0 2px 16px #c7d2fe44', padding: 32
      }}>
        {/* Add/Edit Area */}
        <form onSubmit={editingArea ? handleUpdateArea : handleAddArea} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 30 }}>
          <input
            value={areaName}
            onChange={e => setAreaName(e.target.value)}
            placeholder="Area name"
            style={{
              padding: 12, border: '2px solid #e5e7eb',
              borderRadius: 8, fontSize: 16, minWidth: 220
            }}
          />
          <button
            type="submit"
            style={{
              background: editingArea ? '#fde047' : 'linear-gradient(89deg,#6366f1,#8b5cf6)',
              color: editingArea ? '#92400e' : '#fff', border: 'none', borderRadius: 8,
              padding: '10px 24px', fontWeight: 600, fontSize: 16, cursor: 'pointer'
            }}
          >
            {editingArea ? (
              <> <Edit2 size={18} style={{ verticalAlign: -3, marginRight: 5 }} /> Update Area </>
            ) : (
              <> <Plus size={18} style={{ verticalAlign: -3, marginRight: 5 }} /> Add Area </>
            )}
          </button>
          {editingArea && (
            <button type="button" onClick={() => { setEditingArea(null); setAreaName(''); }}
              style={{ background: '#fff', color: '#6366f1', border: '1px solid #6366f1', borderRadius: 8, padding: '10px 24px', fontWeight: 600, marginLeft: 8, cursor: 'pointer' }}>
              <X size={18} /> Cancel
            </button>
          )}
        </form>
        {/* Area/Legion Data */}
        <div style={{ overflow: "auto" }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead style={{ background: '#f3f4f6', fontSize: 15 }}>
              <tr>
                <th style={{ padding: '10px 8px' }}>#</th>
                <th style={{ textAlign: 'left', padding: '10px 8px' }}>Area Name</th>
                <th style={{ textAlign: 'left', padding: '10px 8px' }}>Legions (Prefix - Name)</th>
                <th style={{ padding: 8 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {areas.map((area, idx) => (
                <tr key={area.id} style={{ borderBottom: '1px solid #f1f1f1', verticalAlign: 'top' }}>
                  {/* Area Info */}
                  <td style={{
                    fontWeight: 700, background: '#eef2ff', color: '#4338ca', fontSize: 20, textAlign: 'center', borderRadius: 8, width: 36
                  }}>{idx + 1}</td>
                  <td style={{ fontWeight: 600, padding: 8, fontSize: 16 }}>
                    {area.name}
                  </td>
                  {/* Legions */}
                  <td style={{ padding: 8, fontSize: 14 }}>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '7px 5px' }}>
                      {legionsByArea(area.id).map(legion => (
                        <span
                          key={legion.id}
                          style={{
                            display: 'inline-flex', alignItems: 'center', background: '#f8fafc', color: '#4f46e5',
                            border: '1px solid #a5b4fc', marginRight: 6, padding: '4px 10px', borderRadius: 7, fontWeight: 600
                          }}
                        >
                          <b>{legion.prefix}</b> - {legion.name}
                          <button title="Delete legion"
                            style={{
                              marginLeft: 8, background: '#fee2e2', color: '#dc2626', border: 'none',
                              padding: '2px 7px', borderRadius: 7, cursor: 'pointer'
                            }} onClick={() => handleDeleteLegion(legion.id)}>
                            <Trash2 size={13} />
                          </button>
                        </span>
                      ))}
                    </div>
                    {(legionAddRow === area.id) ? (
                      <form style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 4 }} onSubmit={e => {
                        e.preventDefault();
                        handleAddLegion(area.id);
                      }}>
                        <input required style={{ width: 60, fontSize: 14, padding: 5, borderRadius: 5 }} placeholder="Prefix" value={legionForm.prefix} onChange={e => setLegionForm(l => ({ ...l, area_id: area.id, prefix: e.target.value }))} />
                        <input required style={{ width: 130, fontSize: 14, padding: 5, borderRadius: 5 }} placeholder="Legion name" value={legionForm.name} onChange={e => setLegionForm(l => ({ ...l, area_id: area.id, name: e.target.value }))} />
                        <button type="submit" style={{ background: '#6366f1', color: 'white', border: 'none', borderRadius: 8, padding: '6px 14px', fontWeight: 600, fontSize: 14 }}>Add</button>
                        <button type="button" style={{ background: '#fff', color: '#6366f1', border: '1px solid #6366f1', borderRadius: 8, padding: '6px 14px', fontWeight: 600, fontSize: 14 }} onClick={() => { setLegionAddRow(null); setLegionForm({ name: '', prefix: '', area_id: '' }); }}>Cancel</button>
                      </form>
                    ) : (
                      <button style={{
                        background: '#6366f1', color: 'white', border: 'none', borderRadius: 8,
                        padding: '5px 18px', marginTop: 8, fontWeight: 600, fontSize: 14, cursor: 'pointer'
                      }} onClick={() => setLegionAddRow(area.id)}>
                        <Plus size={15} style={{ verticalAlign: -2, marginRight: 5 }} /> Add Legion
                      </button>
                    )}
                  </td>
                  <td style={{ padding: 8 }}>
                    <button style={{
                      background: '#fbbf24', color: '#78350f', border: 'none', borderRadius: 7,
                      padding: '7px 16px', fontWeight: 600, marginRight: 6, fontSize: 15, cursor: 'pointer'
                    }} onClick={() => handleEditArea(area)}>
                      <Edit2 size={16} /> Edit
                    </button>
                    <button style={{
                      background: '#ef4444', color: '#fff', border: 'none', borderRadius: 7,
                      padding: '7px 16px', fontWeight: 600, fontSize: 15, cursor: 'pointer'
                    }} onClick={() => handleDeleteArea(area.id)}>
                      <Trash2 size={16} /> Delete Area
                    </button>
                  </td>
                </tr>
              ))}
              {areas.length === 0 && (
                <tr>
                  <td colSpan={4} style={{ textAlign: 'center', color: '#666', fontStyle: 'italic', padding: 40 }}>No areas found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
