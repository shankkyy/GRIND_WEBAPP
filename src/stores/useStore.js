import { create } from 'zustand';

export const useStore = create((set, get) => ({
  // =====================
  // AUTH STATE
  // =====================
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: {
    id: localStorage.getItem('user_id') || null,
    username: localStorage.getItem('username') || null,
    email: null,
    level: 1,
    totalXp: 0,
    emeralds: 0,
    streakDays: 0,
  },
  
  setUser: (user) => set({ user, isAuthenticated: true }),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    set({
      isAuthenticated: false,
      user: {
        id: null,
        username: null,
        email: null,
        level: 1,
        totalXp: 0,
        emeralds: 0,
        streakDays: 0,
      },
    });
  },
  
  // =====================
  // STATS STATE
  // =====================
  stats: {
    messagesCount: 0,
    challengesCompleted: 0,
    emeraldsEarned: 0,
  },
  
  updateStats: (newStats) =>
    set((state) => ({
      stats: { ...state.stats, ...newStats },
    })),
  
  // =====================
  // NOTIFICATIONS
  // =====================
  notifications: [],
  
  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { id: Date.now(), ...notification },
      ],
    })),
  
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
  
  // =====================
  // CHAT STATE
  // =====================
  currentRoom: null,
  messages: [],
  
  setCurrentRoom: (room) => set({ currentRoom: room }),
  
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  
  setMessages: (messages) => set({ messages }),
  
  clearMessages: () => set({ messages: [] }),
  
  // =====================
  // CLASH STATE
  // =====================
  currentClash: null,
  clashActive: false,
  
  setClash: (clash) => set({ currentClash: clash, clashActive: true }),
  endClash: () => set({ currentClash: null, clashActive: false }),
  
  // =====================
  // LEADERBOARD STATE
  // =====================
  leaderboard: [],
  userRank: null,
  
  setLeaderboard: (leaderboard) => set({ leaderboard }),
  setUserRank: (rank) => set({ userRank: rank }),
  
  // =====================
  // COSMETICS STATE
  // =====================
  cosmetics: [],
  equippedCosmetics: {},
  
  setCosmetics: (cosmetics) => set({ cosmetics }),
  setEquippedCosmetics: (cosmetics) => set({ equippedCosmetics: cosmetics }),
  
  // =====================
  // UI STATE
  // =====================
  activeTab: 'chat',
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  showModal: false,
  modalContent: null,
  openModal: (content) => set({ showModal: true, modalContent: content }),
  closeModal: () => set({ showModal: false, modalContent: null }),
  
  // =====================
  // REAL-TIME STATE
  // =====================
  onlineUsers: [],
  setOnlineUsers: (users) => set({ onlineUsers: users }),
  
  // =====================
  // STREAMING STATE
  // =====================
  streak: {
    days: 0,
    multiplier: 1.0,
  },
  setStreak: (streak) => set({ streak }),
  
  // =====================
  // MYSTERY BOXES
  // =====================
  mysteryBoxes: [],
  setMysteryBoxes: (boxes) => set({ mysteryBoxes: boxes }),
  
  addMysteryBox: (box) =>
    set((state) => ({
      mysteryBoxes: [...state.mysteryBoxes, box],
    })),
}));
