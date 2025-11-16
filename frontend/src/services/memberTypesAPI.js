import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api/v1";

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return { headers: { Authorization: `Bearer ${token}` } };
};

export const getMemberTypes = async () =>
  (await axios.get(`${BASE_URL}/member-types/`, getAuthHeaders())).data;

export const getMemberTypeById = async (id) =>
  (await axios.get(`${BASE_URL}/member-types/${id}`, getAuthHeaders())).data;

export const createMemberType = async (data) =>
  (await axios.post(`${BASE_URL}/member-types/`, data, getAuthHeaders())).data;

export const updateMemberType = async (id, data) =>
  (await axios.put(`${BASE_URL}/member-types/${id}`, data, getAuthHeaders())).data;

export const deleteMemberType = async (id) =>
  (await axios.delete(`${BASE_URL}/member-types/${id}`, getAuthHeaders())).data;
