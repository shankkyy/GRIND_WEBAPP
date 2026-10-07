import { useState, useEffect } from 'react';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { useStore } from './stores/useStore';
import Navigation from './components/Navigation';
import Chat from './components/Chat';
import Toast from './components/Toast';
import Login from './components/Login';
import './App.css';

const Challenges = () => <div className="screen">Challenges Screen</div>;
const Leaderboard = () => <div className="screen">Leaderboard Screen</div>;
const Rewards = () => <div className="screen">Rewards Screen</div>;
const Profile = () => <div className="screen">Profile Screen</div>;

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (formerly cacheTime)
    },
  },
});

function App() {
  const { isAuthenticated, activeTab } = useStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on load
    const token = localStorage.getItem('access_token');
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>GRIND</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="app-container">
        {/* Main content area */}
        <div className="main-content">
          {activeTab === 'chat' && <Chat />}
          {activeTab === 'challenges' && <Challenges />}
          {activeTab === 'leaderboard' && <Leaderboard />}
          {activeTab === 'rewards' && <Rewards />}
          {activeTab === 'profile' && <Profile />}
        </div>

        {/* Navigation bar (fixed bottom) */}
        <Navigation />

        {/* Toast notifications */}
        <Toast />
      </div>
    </QueryClientProvider>
  );
}

export default App;
