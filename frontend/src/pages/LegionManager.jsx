import React, { useEffect, useState } from "react";
import { getLegions, addLegion, updateLegion, deleteLegion, getAreas } from "../services/areaLegionAPI";

export default function LegionManager() {
  const [legions, setLegions] = useState([]);
  const [areas, setAreas] = useState([]);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ name: "", area_id: "", prefix: "" });

  async function load() {
    setLegions(await getLegions());
    setAreas(await getAreas());
    setEditId(null);
    setForm({ name: "", area_id: "", prefix: "" });
  }

  useEffect(() => { load(); }, []);

  async function handleAdd(e) {
    e.preventDefault();
    await addLegion(form);
    load();
  }

  async function handleEdit(leg) {
    setEditId(leg.id);
    setForm({ name: leg.name, area_id: leg.area_id, prefix: leg.prefix });
  }

  async function handleUpdate(e) {
    e.preventDefault();
    await updateLegion(editId, form);
    load();
  }

  async function handleDelete(id) {
    if (window.confirm("Delete this legion?")) {
      await deleteLegion(id);
      load();
    }
  }

  return (
    <div>
      <h2>Legions</h2>
      <form onSubmit={editId ? handleUpdate : handleAdd}>
        <select
          required
          value={form.area_id}
          onChange={e => setForm(f => ({ ...f, area_id: e.target.value }))}
        >
          <option value="">Select area</option>
          {areas.map(a => (
            <option key={a.id} value={a.id}>{a.name}</option>
          ))}
        </select>
        <input
          required
          placeholder="Legion name"
          value={form.name}
          onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
        />
        <input
          required
          placeholder="Prefix"
          value={form.prefix}
          onChange={e => setForm(f => ({ ...f, prefix: e.target.value }))}
        />
        {editId ? (
          <>
            <button type="submit">Update</button>
            <button type="button" onClick={load}>Cancel</button>
          </>
        ) : (
          <button type="submit">Add Legion</button>
        )}
      </form>
      <ul>
        {legions.map(l => (
          <li key={l.id}>
            #{l.id} {l.prefix} {l.name} (Area ID: {l.area_id})
            <button onClick={() => handleEdit(l)}>Edit</button>
            <button onClick={() => handleDelete(l.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
