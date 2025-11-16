import React, { useEffect, useState } from "react";
import { getAreas, addArea, updateArea, deleteArea } from "../services/areaLegionAPI";

export default function AreaManager() {
  const [areas, setAreas] = useState([]);
  const [editId, setEditId] = useState(null);
  const [name, setName] = useState("");

  async function load() {
    setAreas(await getAreas());
    setEditId(null);
    setName("");
  }

  useEffect(() => { load(); }, []);

  async function handleAdd(e) {
    e.preventDefault();
    if (!name.trim()) return;
    await addArea({ name });
    load();
  }

  async function handleEdit(id, name) {
    setEditId(id);
    setName(name);
  }

  async function handleUpdate(e) {
    e.preventDefault();
    if (!name.trim() || editId == null) return;
    await updateArea(editId, { name });
    load();
  }

  async function handleDelete(id) {
    if (window.confirm("Delete this area?")) {
      await deleteArea(id);
      load();
    }
  }

  return (
    <div>
      <h2>Areas</h2>
      <form onSubmit={editId ? handleUpdate : handleAdd}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Area name"
        />
        {editId ? (
          <>
            <button type="submit">Update</button>
            <button type="button" onClick={() => { setEditId(null); setName(""); }}>Cancel</button>
          </>
        ) : (
          <button type="submit">Add Area</button>
        )}
      </form>
      <ul>
        {areas.map(a => (
          <li key={a.id}>
            #{a.id} {a.name}
            <button onClick={() => handleEdit(a.id, a.name)}>Edit</button>
            <button onClick={() => handleDelete(a.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
