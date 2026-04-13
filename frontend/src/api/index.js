import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: (data) => api.post('/accounts/signup/', data),
  login: (data) => api.post('/accounts/login/', data),
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (data) => api.patch('/accounts/profile/', data),
  getSettings: () => api.get('/accounts/settings/'),
  updateSettings: (data) => api.patch('/accounts/settings/', data),
  uploadProfilePicture: (formData) => api.post('/accounts/profile/picture/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

// Token API
export const tokenAPI = {
  obtain: (data) => api.post('/token/', data),
  refresh: (data) => api.post('/token/refresh/', data),
};

// Resume API
export const resumeAPI = {
  getAll: () => api.get('/resumes/'),
  getOne: (id) => api.get(`/resumes/${id}/`),
  create: (data) => api.post('/resumes/', data),
  update: (id, data) => api.patch(`/resumes/${id}/`, data),
  delete: (id) => api.delete(`/resumes/${id}/`),

  // Education
  addEducation: (resumeId, data) => api.post(`/resumes/${resumeId}/education/`, data),
  updateEducation: (eduId, data) => api.patch(`/resumes/education/${eduId}/`, data),
  deleteEducation: (eduId) => api.delete(`/resumes/education/${eduId}/`),

  // Experience
  addExperience: (resumeId, data) => api.post(`/resumes/${resumeId}/experience/`, data),
  updateExperience: (expId, data) => api.patch(`/resumes/experience/${expId}/`, data),
  deleteExperience: (expId) => api.delete(`/resumes/experience/${expId}/`),

  // Skills
  addSkill: (resumeId, data) => api.post(`/resumes/${resumeId}/skills/`, data),
  deleteSkill: (skillId) => api.delete(`/resumes/skills/${skillId}/`),

  // Projects
  addProject: (resumeId, data) => api.post(`/resumes/${resumeId}/projects/`, data),
  updateProject: (projectId, data) => api.patch(`/resumes/projects/${projectId}/`, data),
  deleteProject: (projectId) => api.delete(`/resumes/projects/${projectId}/`),

  // Templates
  getTemplates: () => api.get('/resumes/templates/'),
  setTemplate: (resumeId, templateId) => api.post(`/resumes/${resumeId}/template/`, { template_id: templateId }),

  // Sharing
  generateShareLink: (resumeId) => api.post(`/resumes/${resumeId}/share/`),
  revokeShareLink: (resumeId) => api.post(`/resumes/${resumeId}/share/revoke/`),

  // PDF
  generatePDF: (resumeId) => api.get(`/resumes/${resumeId}/pdf/`),
};

// Cover Letter API
export const coverLetterAPI = {
  getAll: (resumeId) => api.get(`/resumes/${resumeId}/cover-letters/`),
  create: (resumeId, data) => api.post(`/resumes/${resumeId}/cover-letters/`, data),
  update: (id, data) => api.patch(`/resumes/cover-letters/${id}/`, data),
  delete: (id) => api.delete(`/resumes/cover-letters/${id}/`),
};

// Job Application API
export const jobApplicationAPI = {
  getAll: (resumeId) => api.get(`/resumes/${resumeId}/jobs/`),
  create: (resumeId, data) => api.post(`/resumes/${resumeId}/jobs/`, data),
  update: (id, data) => api.patch(`/resumes/jobs/${id}/`, data),
  delete: (id) => api.delete(`/resumes/jobs/${id}/`),
};

// Analytics API
export const analyticsAPI = {
  get: (resumeId) => api.get(`/resumes/${resumeId}/analytics/`),
};

// Versioning API
export const versionAPI = {
  getAll: (resumeId) => api.get(`/resumes/${resumeId}/versions/`),
  create: (resumeId) => api.post(`/resumes/${resumeId}/versions/create/`),
  restore: (resumeId, versionNumber) => api.post(`/resumes/${resumeId}/versions/${versionNumber}/restore/`),
};

export default api;