import axios from 'axios';

// Change the base URL to include /api/v1
const API_URL = 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests automatically
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

// Organization API calls
export const organizationAPI = {
  getMyOrganization: async () => {
    const response = await api.get('/organizations/me');
    return response.data;
  },
  
  getOrganizationUsers: async () => {
    const response = await api.get('/organizations/users');
    return response.data;
  },
  
  createUser: async (userData) => {
    const response = await api.post('/organizations/users', userData);
    return response.data;
  },
  
  updateUserRole: async (userId, roleIds) => {
    const response = await api.post('/rbac/users/assign-roles', { 
      user_id: userId, 
      role_ids: roleIds 
    });
    return response.data;
  },
  
  deleteUser: async (userId) => {
    const response = await api.delete(`/organizations/users/${userId}`);
    return response.data;
  },
  
  updateOrganization: async (name) => {
    const response = await api.put('/organizations/me', { name });
    return response.data;
  },
};

// RBAC API calls
export const rbacAPI = {
  // Permissions
  getAllPermissions: async () => {
    const response = await api.get('/rbac/permissions');
    return response.data;
  },
  
  createPermission: async (permissionData) => {
    const response = await api.post('/rbac/permissions', permissionData);
    return response.data;
  },
  
  // Roles
  getAllRoles: async () => {
    const response = await api.get('/rbac/roles');
    return response.data;
  },
  
  createRole: async (roleData) => {
    const response = await api.post('/rbac/roles', roleData);
    return response.data;
  },
  
  updateRole: async (roleId, roleData) => {
    const response = await api.put(`/rbac/roles/${roleId}`, roleData);
    return response.data;
  },
  
  deleteRole: async (roleId) => {
    const response = await api.delete(`/rbac/roles/${roleId}`);
    return response.data;
  },
  
  // User Permissions
  assignRoles: async (userId, roleIds) => {
    const response = await api.post('/rbac/users/assign-roles', {
      user_id: userId,
      role_ids: roleIds
    });
    return response.data;
  },
  
  getUserPermissions: async (userId) => {
    const response = await api.get(`/rbac/users/${userId}/permissions`);
    return response.data;
  },
  
  // Row-level policies
  createRowPolicy: async (policyData) => {
    const response = await api.post('/rbac/row-policies', policyData);
    return response.data;
  },
  
  getRolePolicies: async (roleId) => {
    const response = await api.get(`/rbac/row-policies/role/${roleId}`);
    return response.data;
  },
};

// Members API calls
export const membersAPI = {
  getMyProfile: async () => {
    const response = await api.get('/members/me');
    return response.data;
  },
  
  createProfile: async (profileData) => {
    const response = await api.post('/members/', profileData);
    return response.data;
  },
  
  updateProfile: async (profileData) => {
    const response = await api.put('/members/me', profileData);
    return response.data;
  },
  
  getAllMembers: async (search = '') => {
    const params = search ? `?search=${search}` : '';
    const response = await api.get(`/members/${params}`);
    return response.data;
  },
  
  getMemberById: async (memberId) => {
    const response = await api.get(`/members/${memberId}`);
    return response.data;
  },
};

export default api;
