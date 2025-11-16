import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api/v1";

// -------------------------
// AREA ENDPOINTS
// -------------------------

export const getAreas = async () =>
  (await axios.get(`${BASE_URL}/areas/areas/`)).data;

export const addArea = async (data) =>
  (await axios.post(`${BASE_URL}/areas/areas/`, data)).data;

export const getAreaById = async (id) =>
  (await axios.get(`${BASE_URL}/areas/areas/${id}`)).data;

export const updateArea = async (id, data) =>
  (await axios.put(`${BASE_URL}/areas/areas/${id}`, data)).data;

export const deleteArea = async (id) =>
  (await axios.delete(`${BASE_URL}/areas/areas/${id}`)).data;


// -------------------------
// LEGION ENDPOINTS
// -------------------------

export const getLegions = async () =>
  (await axios.get(`${BASE_URL}/legions/legions/`)).data;

export const addLegion = async (data) =>
  (await axios.post(`${BASE_URL}/legions/legions/`, data)).data;

export const getLegionById = async (id) =>
  (await axios.get(`${BASE_URL}/legions/legions/${id}`)).data;

export const updateLegion = async (id, data) =>
  (await axios.put(`${BASE_URL}/legions/legions/${id}`, data)).data;

export const deleteLegion = async (id) =>
  (await axios.delete(`${BASE_URL}/legions/legions/${id}`)).data;
