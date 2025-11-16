import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api/v1";

// Helper to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };
};

// -------------------------
// MEMBERSHIP FEES ENDPOINTS
// -------------------------

export const getMembershipFees = async () =>
  (await axios.get(`${BASE_URL}/membership-fees/membership-fees/`, getAuthHeaders())).data;

export const addMembershipFee = async (data) =>
  (await axios.post(`${BASE_URL}/membership-fees/membership-fees/`, data, getAuthHeaders())).data;

export const getMembershipFeeById = async (id) =>
  (await axios.get(`${BASE_URL}/membership-fees/membership-fees/${id}`, getAuthHeaders())).data;

export const updateMembershipFee = async (id, data) =>
  (await axios.put(`${BASE_URL}/membership-fees/membership-fees/${id}`, data, getAuthHeaders())).data;

export const deleteMembershipFee = async (id) =>
  (await axios.delete(`${BASE_URL}/membership-fees/membership-fees/${id}`, getAuthHeaders())).data;

// Image Upload
export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const token = localStorage.getItem('token');
  const response = await axios.post(
    `${BASE_URL}/membership-fees/membership-fees/upload-image`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`
      }
    }
  );
  return response.data;
};
