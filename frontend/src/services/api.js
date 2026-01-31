import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';


// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests
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

// Handle response errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.reload();
        }
        return Promise.reject(error);
    }
);

// Auth APIs
export const authAPI = {
    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    getCurrentUser: async () => {
        const response = await api.get('/auth/me');
        return response.data;
    },
};

// Tasks APIs
export const tasksAPI = {
    getAll: async () => {
        const response = await api.get('/tasks');
        return response.data;
    },

    get: async (id) => {
        const response = await api.get(`/tasks/${id}`);
        return response.data;
    },

    create: async (taskData) => {
        const response = await api.post('/tasks', taskData);
        return response.data;
    },

    update: async (id, taskData) => {
        const response = await api.put(`/tasks/${id}`, taskData);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/tasks/${id}`);
        return response.data;
    },

    search: async (filters) => {
        const response = await api.get('/tasks/search', { params: filters });
        return response.data;
    },
};

// Projects APIs
export const projectsAPI = {
    getAll: async () => {
        const response = await api.get('/projects');
        return response.data;
    },

    create: async (projectData) => {
        const response = await api.post('/projects', projectData);
        return response.data;
    },

    update: async (id, projectData) => {
        const response = await api.put(`/projects/${id}`, projectData);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/projects/${id}`);
        return response.data;
    },
};

// Comments APIs
export const commentsAPI = {
    getByTask: async (taskId) => {
        const response = await api.get(`/comments/task/${taskId}`);
        return response.data;
    },

    create: async (commentData) => {
        const response = await api.post('/comments', commentData);
        return response.data;
    },
};

// Notifications APIs
export const notificationsAPI = {
    getAll: async (unreadOnly = false) => {
        const response = await api.get('/notifications', { params: { unread_only: unreadOnly } });
        return response.data;
    },

    markAsRead: async (id) => {
        const response = await api.post(`/notifications/${id}/read`);
        return response.data;
    },

    markAllAsRead: async () => {
        const response = await api.post('/notifications/read-all');
        return response.data;
    },
};

// History APIs
export const historyAPI = {
    getByTask: async (taskId) => {
        const response = await api.get(`/history/task/${taskId}`);
        return response.data;
    },

    getAll: async (limit = 100) => {
        const response = await api.get('/history', { params: { limit } });
        return response.data;
    },
};

// Reports APIs
export const reportsAPI = {
    getStats: async () => {
        const response = await api.get('/reports/stats');
        return response.data;
    },

    generate: async (type) => {
        const response = await api.get('/reports/generate', { params: { report_type: type } });
        return response.data;
    },

    getUsers: async () => {
        const response = await api.get('/reports/users');
        return response.data;
    },
};

export default api;
