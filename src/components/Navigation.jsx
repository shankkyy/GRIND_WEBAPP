import { useStore } from '../stores/useStore';
import './Navigation.css';

const Navigation = () => {
  const { activeTab, setActiveTab } = useStore();

  const tabs = [
    { id: 'chat', icon: '🏠', label: 'Home' },
    { id: 'challenges', icon: '⚡', label: 'Challenges' },
    { id: 'leaderboard', icon: '🏆', label: 'Leaderboard' },
    { id: 'rewards', icon: '🎁', label: 'Rewards' },
    { id: 'profile', icon: '👤', label: 'Profile' },
  ];

  return (
    <nav className="navigation">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`nav-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
          title={tab.label}
        >
          <span className="nav-icon">{tab.icon}</span>
          <span className="nav-label">{tab.label}</span>
        </button>
      ))}
    </nav>
  );
};

export default Navigation;
