import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
client.interceptors.response.use(
  (response) => response,
  (error) => {
    const requestUrl = error.config?.url || '';
    const isAuthRequest = requestUrl.includes('/auth/login') || requestUrl.includes('/auth/register');
    if (error.response?.status === 401 && !isAuthRequest) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default client;

// =====================
// AUTH ENDPOINTS
// =====================

export const authAPI = {
  register: (email, username, password) =>
    client.post('/auth/register', { email, username, password }),
  
  login: (email, password) =>
    client.post('/auth/login', { email, password }),
};

// =====================
// USER ENDPOINTS
// =====================

export const userAPI = {
  getProfile: () => client.get('/users/me'),
  
  getProfileById: (userId) =>
    client.get(`/users/${userId}/profile`),
  
  getStats: (userId) =>
    client.get(`/users/${userId}/stats`),
  
  getCosmetics: (userId) =>
    client.get(`/users/${userId}/cosmetics`),
  
  equipCosmetic: (cosmeticId) =>
    client.post(`/cosmetics/${cosmeticId}/equip`),
};

// =====================
// CHAT ENDPOINTS
// =====================

export const chatAPI = {
  createRoom: (name, description, isPublic) =>
    client.post('/rooms', { name, description, is_public: isPublic }),
  
  getRoom: (roomId) =>
    client.get(`/rooms/${roomId}`),
  
  getMessages: (roomId, limit = 50, offset = 0) =>
    client.get(`/rooms/${roomId}/messages`, { params: { limit, offset } }),
  
  sendMessage: (roomId, content) =>
    client.post('/messages', { room_id: roomId, content }),
  
  addReaction: (messageId, emoji) =>
    client.post(`/messages/${messageId}/reactions`, { emoji }),
};

// =====================
// CHALLENGE ENDPOINTS
// =====================

export const challengeAPI = {
  getChallenges: (difficulty = null) =>
    client.get('/challenges', { params: { difficulty } }),
  
  submitChallenge: (challengeId, score) =>
    client.post(`/challenges/${challengeId}/submit`, { score }),
};

// =====================
// CLASH ENDPOINTS
// =====================

export const clashAPI = {
  createClash: () =>
    client.post('/clash/create'),
  
  updateScore: (clashId, scoreIncrement) =>
    client.post(`/clash/${clashId}/update-score`, { score_increment: scoreIncrement }),
  
  endClash: (clashId, winnerId) =>
    client.post(`/clash/${clashId}/end`, { winner_id: winnerId }),
};

// =====================
// REWARDS ENDPOINTS
// =====================

export const rewardsAPI = {
  spinWheel: () =>
    client.post('/spin-wheel'),
  
  openMysteryBox: (boxId) =>
    client.post(`/mystery-boxes/${boxId}/open`),
};

// =====================
// LEADERBOARD ENDPOINTS
// =====================

export const leaderboardAPI = {
  getLeaderboard: (type = 'weekly', limit = 10, offset = 0) =>
    client.get('/leaderboard', { params: { leaderboard_type: type, limit, offset } }),
  
  getUserRank: (userId) =>
    client.get(`/leaderboard/user/${userId}/rank`),
};

// =====================
// STREAK ENDPOINTS
// =====================

export const streakAPI = {
  updateStreak: (userId) =>
    client.post(`/streaks/${userId}/update`),
};
