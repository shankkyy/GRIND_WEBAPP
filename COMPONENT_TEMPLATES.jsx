// =====================
// TEMPLATE: MessageBubble.jsx
// =====================
import './MessageBubble.css';

const MessageBubble = ({ message, isOwn }) => {
  return (
    <div className={`message-bubble ${isOwn ? 'own' : 'other'}`}>
      <div className="message-header">
        <span className="username">{message.username}</span>
        <span className="timestamp">{new Date(message.created_at).toLocaleTimeString()}</span>
      </div>
      <div className="message-content">
        {message.content}
      </div>
      <div className="message-footer">
        {Object.entries(message.reactions || {}).map(([emoji, count]) => (
          <button key={emoji} className="reaction">
            {emoji} {count}
          </button>
        ))}
      </div>
    </div>
  );
};

export default MessageBubble;

// =====================
// TEMPLATE: ClashBattle.jsx
// =====================
import { useState, useEffect } from 'react';
import { useStore } from '../stores/useStore';
import { clashAPI } from '../api/client';
import './ClashBattle.css';

const ClashBattle = () => {
  const { user } = useStore();
  const [timeLeft, setTimeLeft] = useState(60);
  const [yourScore, setYourScore] = useState(0);
  const [oppScore, setOppScore] = useState(0);
  const [gameActive, setGameActive] = useState(true);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          setGameActive(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleTap = async () => {
    if (!gameActive) return;
    
    setYourScore(prev => prev + 1);
    // Send update via API
  };

  const getTimeColor = () => {
    if (timeLeft > 20) return 'green';
    if (timeLeft > 10) return 'gold';
    return 'red';
  };

  return (
    <div className="clash-container">
      <h2>SPEED TAPPING</h2>
      <div className={`timer color-${getTimeColor()}`}>{timeLeft}s</div>
      
      <div className="score-display">
        <div className="score-section">
          <p>YOU</p>
          <div className="score-bar">
            <div className="fill" style={{ width: `${(yourScore / 100) * 100}%` }}></div>
          </div>
          <span className="score">{yourScore}</span>
        </div>
        
        <div className="score-section">
          <p>OPPONENT</p>
          <div className="score-bar">
            <div className="fill" style={{ width: `${(oppScore / 100) * 100}%` }}></div>
          </div>
          <span className="score">{oppScore}</span>
        </div>
      </div>

      <div className="tap-area" onClick={handleTap}>
        TAP HERE
      </div>

      {!gameActive && (
        <div className="result">
          {yourScore > oppScore ? '🎉 YOU WIN!' : '😢 YOU LOST'}
        </div>
      )}
    </div>
  );
};

export default ClashBattle;

// =====================
// TEMPLATE: SpinWheel.jsx
// =====================
import { useState } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '../stores/useStore';
import { rewardsAPI } from '../api/client';
import './SpinWheel.css';

const SpinWheel = () => {
  const { addNotification } = useStore();
  const [isSpinning, setIsSpinning] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [result, setResult] = useState(null);

  const segments = [100, 200, 500, 50, 300, 150, 250, 1000];
  const segmentAngle = 360 / segments.length;

  const handleSpin = async () => {
    if (isSpinning) return;

    setIsSpinning(true);
    
    try {
      const response = await rewardsAPI.spinWheel();
      const reward = response.data.reward;

      // Calculate rotation
      const rewardIndex = segments.indexOf(reward);
      const newRotation = rotation + (360 * 3) + (rewardIndex * segmentAngle);
      
      setRotation(newRotation);
      setResult(reward);

      addNotification({
        type: 'success',
        message: `🎉 You won ${reward} Emeralds!`,
      });
    } catch (error) {
      addNotification({
        type: 'error',
        message: 'Already spun today!',
      });
    } finally {
      setIsSpinning(false);
    }
  };

  return (
    <div className="spin-wheel-container">
      <h2>DAILY SPIN WHEEL ✨</h2>
      
      <motion.div
        className="wheel"
        animate={{ rotate: rotation }}
        transition={{ duration: 4, ease: 'easeOut' }}
      >
        {/* SVG wheel would go here */}
      </motion.div>

      <div className="pointer"></div>

      <button
        className="spin-button"
        onClick={handleSpin}
        disabled={isSpinning}
      >
        {isSpinning ? 'SPINNING...' : 'SPIN NOW!'}
      </button>

      {result && (
        <div className="result">
          +{result} EMERALDS!
        </div>
      )}
    </div>
  );
};

export default SpinWheel;

// =====================
// TEMPLATE: Leaderboard.jsx
// =====================
import { useQuery } from '@tanstack/react-query';
import { leaderboardAPI } from '../api/client';
import './Leaderboard.css';

const Leaderboard = () => {
  const [filterType, setFilterType] = useState('weekly');

  const { data: leaderboard = [], isLoading } = useQuery({
    queryKey: ['leaderboard', filterType],
    queryFn: () => leaderboardAPI.getLeaderboard(filterType, 20),
    select: (response) => response.data,
  });

  if (isLoading) return <div className="loading">Loading...</div>;

  return (
    <div className="leaderboard-container">
      <h2>LEADERBOARD</h2>

      <div className="filters">
        {['weekly', 'monthly', 'all_time'].map(type => (
          <button
            key={type}
            className={`filter-btn ${filterType === type ? 'active' : ''}`}
            onClick={() => setFilterType(type)}
          >
            {type.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="leaderboard-list">
        {leaderboard.map((entry) => (
          <div key={entry.user_id} className="leaderboard-entry">
            <span className="rank">{['🥇', '🥈', '🥉'][entry.rank - 1] || '◆'} #{entry.rank}</span>
            <span className="username">{entry.username}</span>
            <span className="xp">{entry.xp} XP</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Leaderboard;

// =====================
// TEMPLATE: Challenges.jsx
// =====================
import { useQuery } from '@tanstack/react-query';
import { challengeAPI } from '../api/client';
import './Challenges.css';

const Challenges = () => {
  const { data: challenges = [], isLoading } = useQuery({
    queryKey: ['challenges'],
    queryFn: () => challengeAPI.getChallenges(),
    select: (response) => response.data,
  });

  if (isLoading) return <div>Loading challenges...</div>;

  return (
    <div className="challenges-container">
      <h2>AVAILABLE CHALLENGES</h2>

      <div className="challenges-grid">
        {challenges.map(challenge => (
          <div key={challenge.id} className="challenge-card">
            <h3>{challenge.title}</h3>
            <p className="difficulty">{challenge.difficulty.toUpperCase()}</p>
            <p className="description">{challenge.description}</p>
            <div className="rewards">
              <span className="emeralds">💰 {challenge.reward_emeralds}</span>
              <span className="xp">⭐ {challenge.reward_xp} XP</span>
            </div>
            <button className="play-btn">PLAY NOW</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Challenges;

// =====================
// TEMPLATE: Profile.jsx
// =====================
import { useQuery } from '@tanstack/react-query';
import { useStore } from '../stores/useStore';
import { userAPI } from '../api/client';
import './Profile.css';

const Profile = () => {
  const { user } = useStore();
  
  const { data: stats } = useQuery({
    queryKey: ['user-stats', user.id],
    queryFn: () => userAPI.getStats(user.id),
    select: (response) => response.data,
  });

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="avatar">👤</div>
        <div>
          <h2>{user.username}</h2>
          <p className="level">Level {user.level}</p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat">
          <span className="value">{user.totalXp}</span>
          <span className="label">Total XP</span>
        </div>
        <div className="stat">
          <span className="value">{user.emeralds}</span>
          <span className="label">Emeralds</span>
        </div>
        <div className="stat">
          <span className="value">{user.streakDays}</span>
          <span className="label">Day Streak</span>
        </div>
      </div>

      <div className="cosmetics-section">
        <h3>COSMETICS</h3>
        {/* Display equipped cosmetics */}
      </div>

      <div className="achievements-section">
        <h3>ACHIEVEMENTS</h3>
        {/* Display achievements */}
      </div>
    </div>
  );
};

export default Profile;

// =====================
// TEMPLATE: Toast.jsx (Notifications)
// =====================
import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore } from '../stores/useStore';
import './Toast.css';

const Toast = () => {
  const { notifications, removeNotification } = useStore();

  return (
    <div className="toast-container">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -100, opacity: 0 }}
            className={`toast ${notification.type}`}
          >
            {notification.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default Toast;
