# GRIND Webapp - Complete Setup & Implementation Guide

## 📋 Project Overview

This document provides a complete guide to set up and run the GRIND gamified chat application with FastAPI backend and React frontend.

---

## 📂 Project Structure

```
grind-project/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── database.py             # Supabase integration
│   ├── auth.py                 # JWT authentication
│   ├── websocket_manager.py    # WebSocket connections
│   ├── requirements.txt         # Python dependencies
│   └── .env                    # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.jsx  # Navigation bar
│   │   │   ├── Chat.jsx        # Chat screen
│   │   │   ├── Challenges.jsx  # Challenges screen
│   │   │   ├── Leaderboard.jsx # Leaderboard screen
│   │   │   ├── Rewards.jsx     # Rewards screen
│   │   │   ├── Profile.jsx     # Profile screen
│   │   │   ├── SpinWheel.jsx   # Spin wheel modal
│   │   │   ├── ClashBattle.jsx # Clash battle screen
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── Toast.jsx       # Notifications
│   │   │   └── Modal.jsx       # Generic modal
│   │   ├── hooks/
│   │   │   ├── useWebSocket.js # WebSocket hook
│   │   │   └── useQuery.js     # React Query setup
│   │   ├── stores/
│   │   │   └── useStore.js     # Zustand store
│   │   ├── api/
│   │   │   └── client.js       # API client
│   │   ├── styles/
│   │   │   └── global.css      # Global styles
│   │   ├── App.jsx             # Root component
│   │   └── main.jsx            # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.local
```

---

## 🚀 Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install fastapi uvicorn python-dotenv pydantic supabase python-jose pyjwt
```

### 2. Create `.env` file

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this

# Environment
ENVIRONMENT=development
```

### 3. Supabase Database Schema

Run these SQL commands in your Supabase SQL editor:

```sql
-- Create users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  level INT DEFAULT 1,
  total_xp INT DEFAULT 0,
  emeralds INT DEFAULT 0,
  streak_days INT DEFAULT 0,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create rooms table
CREATE TABLE rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  creator_id UUID REFERENCES users(id),
  members_count INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_public BOOLEAN DEFAULT true
);

-- Create room_members table
CREATE TABLE room_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  joined_at TIMESTAMP DEFAULT NOW(),
  role TEXT DEFAULT 'member',
  UNIQUE(room_id, user_id)
);

-- Create messages table
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  username TEXT NOT NULL,
  avatar_url TEXT,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  reactions JSONB DEFAULT '{}',
  is_edited BOOLEAN DEFAULT false
);

-- Create challenges table
CREATE TABLE challenges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  type TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  reward_emeralds INT NOT NULL,
  reward_xp INT NOT NULL,
  time_limit_seconds INT NOT NULL,
  available_daily BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create challenge_submissions table
CREATE TABLE challenge_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  challenge_id UUID REFERENCES challenges(id),
  user_id UUID REFERENCES users(id),
  score INT NOT NULL,
  submitted_at TIMESTAMP DEFAULT NOW()
);

-- Create clash_battles table
CREATE TABLE clash_battles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_1_id UUID REFERENCES users(id),
  user_1_name TEXT NOT NULL,
  user_2_id UUID REFERENCES users(id),
  user_2_name TEXT NOT NULL,
  user_1_score INT DEFAULT 0,
  user_2_score INT DEFAULT 0,
  status TEXT DEFAULT 'active',
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  winner_id UUID REFERENCES users(id)
);

-- Create streaks table
CREATE TABLE streaks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE REFERENCES users(id),
  current_streak INT DEFAULT 0,
  longest_streak INT DEFAULT 0,
  last_activity_date TIMESTAMP,
  multiplier FLOAT DEFAULT 1.0,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create spin_history table
CREATE TABLE spin_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  reward INT NOT NULL,
  is_rare BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create mystery_boxes table
CREATE TABLE mystery_boxes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  rarity TEXT NOT NULL,
  opened BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  opened_at TIMESTAMP
);

-- Create user_achievements table
CREATE TABLE user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  achievement_id TEXT NOT NULL,
  achievement_name TEXT NOT NULL,
  unlocked_at TIMESTAMP DEFAULT NOW()
);

-- Create user_cosmetics table
CREATE TABLE user_cosmetics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  cosmetic_id TEXT NOT NULL,
  cosmetic_name TEXT NOT NULL,
  cosmetic_type TEXT NOT NULL,
  rarity TEXT NOT NULL,
  equipped BOOLEAN DEFAULT false,
  obtained_at TIMESTAMP DEFAULT NOW()
);

-- Create cosmetics table
CREATE TABLE cosmetics (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  rarity TEXT NOT NULL,
  cost_emeralds INT,
  description TEXT
);

-- Create indexes for better performance
CREATE INDEX idx_messages_room_id ON messages(room_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_room_members_room_id ON room_members(room_id);
CREATE INDEX idx_room_members_user_id ON room_members(user_id);
CREATE INDEX idx_challenge_submissions_user_id ON challenge_submissions(user_id);
CREATE INDEX idx_clash_battles_user_1_id ON clash_battles(user_1_id);
CREATE INDEX idx_clash_battles_user_2_id ON clash_battles(user_2_id);
CREATE INDEX idx_spin_history_user_id ON spin_history(user_id);
CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX idx_user_cosmetics_user_id ON user_cosmetics(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

### 4. Run FastAPI Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

---

## 🎨 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Create `.env.local` file

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## 🛠️ Key Components Implementation

### Chat Component (`src/components/Chat.jsx`)

Handles real-time messaging with:
- Message input and sending
- Auto-scroll to latest message
- Real-time WebSocket updates
- Quick action buttons for rewards

### ClashBattle Component (`src/components/ClashBattle.jsx`)

Real-time competitive tapping game:
```javascript
// Example
const ClashBattle = () => {
  const [yourScore, setYourScore] = useState(0);
  const [oppScore, setOppScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);

  const handleTap = () => {
    setYourScore(prev => prev + 1);
    // Send update via WebSocket
  };

  // Countdown timer, score updates, winner determination
};
```

### SpinWheel Component (`src/components/SpinWheel.jsx`)

SVG-based spinning wheel:
```javascript
// Uses Framer Motion for smooth rotation animation
// Weighted random selection for rewards
// Celebration effects on rare wins
```

### Leaderboard Component (`src/components/Leaderboard.jsx`)

Real-time rankings with:
- Live rank changes
- XP progression tracking
- Streak indicators
- Achievement badges

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### User
- `GET /api/users/me` - Get current user
- `GET /api/users/{id}/profile` - Get user profile
- `GET /api/users/{id}/stats` - Get user statistics
- `GET /api/users/{id}/cosmetics` - Get user cosmetics
- `POST /api/cosmetics/{id}/equip` - Equip cosmetic

### Chat
- `POST /api/rooms` - Create room
- `GET /api/rooms/{id}` - Get room details
- `GET /api/rooms/{id}/messages` - Get messages
- `POST /api/messages` - Send message
- `POST /api/messages/{id}/reactions` - Add reaction

### Challenges
- `GET /api/challenges` - Get challenges
- `POST /api/challenges/{id}/submit` - Submit challenge

### Clash
- `POST /api/clash/create` - Create clash
- `POST /api/clash/{id}/update-score` - Update score
- `POST /api/clash/{id}/end` - End clash

### Rewards
- `POST /api/spin-wheel` - Spin wheel
- `POST /api/mystery-boxes/{id}/open` - Open mystery box

### Leaderboard
- `GET /api/leaderboard` - Get leaderboard
- `GET /api/leaderboard/user/{id}/rank` - Get user rank

### Streaks
- `POST /api/streaks/{id}/update` - Update streak

---

## 🔌 WebSocket Events

### Client → Server

```javascript
// Join room
{ type: 'join', room_id: 'room-123', user_id: 'user-456' }

// Send message
{ type: 'message', content: 'Hello!' }

// Clash tap
{ type: 'clash_tap', clash_id: 'clash-123', score: 1 }
```

### Server → Client

```javascript
// Message received
{ type: 'message', data: messageObject }

// User joined
{ type: 'user_joined', user_id: 'user-123' }

// Clash update
{ type: 'clash_update', data: clashObject }

// Reaction
{ type: 'reaction', data: { message_id, reactions } }

// Achievement
{ type: 'achievement', data: { name, description } }
```

---

## 🎨 Styling System

### CSS Variables

All colors, spacing, and typography are defined in `src/styles/global.css`:

```css
:root {
  /* Colors */
  --color-accent-green: #00ff41;
  --color-accent-blue: #00d4ff;
  --color-accent-gold: #ffcc00;
  
  /* Spacing */
  --space-sm: 8px;
  --space-md: 16px;
  
  /* Animations */
  --duration-fast: 150ms;
  --easing-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### Utility Classes

Use predefined classes for consistency:
```html
<div class="flex gap-md p-lg bg-grid border-accent">
  Content here
</div>
```

---

## 🔐 Authentication Flow

```
1. User registers/logs in
2. FastAPI creates JWT token
3. Token stored in localStorage
4. Token sent with every API request
5. WebSocket authenticated on connect
6. Token auto-refreshed on expiry
```

---

## 📦 State Management

Using Zustand for global state:

```javascript
import { useStore } from './stores/useStore';

const MyComponent = () => {
  const { user, addNotification } = useStore();
  
  const handleAction = () => {
    addNotification({
      type: 'success',
      message: 'Action completed!'
    });
  };
};
```

---

## 🚀 Deployment

### Backend (Render, Railway, etc.)

```bash
# Push to Git
git push origin main

# Render will auto-deploy with Procfile:
# web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel, Netlify, etc.)

```bash
npm run build
# Deploy dist/ folder
```

---

## 📊 Performance Optimization

### Frontend
- Code splitting by route
- Image lazy loading
- Memoization of expensive components
- Debounced WebSocket updates

### Backend
- Connection pooling for Supabase
- Redis caching for leaderboard
- Query optimization with indexes
- WebSocket message batching

---

## 🧪 Testing

### Backend
```bash
pip install pytest pytest-asyncio
pytest backend/tests/
```

### Frontend
```bash
npm install vitest @testing-library/react
npm run test
```

---

## 🐛 Debugging

### Backend
```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend
```javascript
// React DevTools extension
// Redux DevTools for state debugging
// Network tab for API calls
```

---

## 📱 Mobile Optimization

- Touch targets minimum 48×48px
- Responsive breakpoints at 768px and 480px
- Mobile-first CSS
- Swipe gesture support for navigation

---

## 🔄 Real-Time Features

### Message Streaming
- Messages appear instantly
- Typing indicators
- Read receipts

### Leaderboard Live Updates
- Real-time rank changes
- Animated transitions
- Notification alerts

### Clash Battles
- Live score updates
- Timer synchronization
- Instant result display

---

## 🎯 Next Steps

1. **Clone/create project structure** from this guide
2. **Set up Supabase** with the provided SQL schema
3. **Install dependencies** for both backend and frontend
4. **Configure environment variables**
5. **Run both servers**
6. **Test authentication flow**
7. **Build features** in priority order:
   - Chat messaging
   - Challenges & submission
   - Clash battles
   - Leaderboard
   - Rewards & cosmetics

---

## 📚 Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Supabase Documentation](https://supabase.com/docs)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [React Query Documentation](https://tanstack.com/query/latest)

---

## ✅ Checklist

- [ ] Backend set up and running
- [ ] Supabase database created with schema
- [ ] Frontend set up and running
- [ ] Authentication working (register/login)
- [ ] Chat messaging working
- [ ] WebSocket connected
- [ ] Challenges functional
- [ ] Clash battles working
- [ ] Leaderboard updating
- [ ] Spin wheel functional
- [ ] Cosmetics displaying
- [ ] Notifications working
- [ ] Responsive design tested
- [ ] Performance optimized
- [ ] Deployed to production

---

## 🎉 You're Ready!

Your GRIND webapp is now set up and ready for development. Happy coding! 🚀
