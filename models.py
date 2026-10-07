from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# =====================
# USER & AUTH MODELS
# =====================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: Optional[str] = None
    level: int = 1
    total_xp: int = 0
    emeralds: int = 0
    streak_days: int = 0
    last_login: datetime
    created_at: datetime

class UserStats(BaseModel):
    user_id: str
    level: int
    total_xp: int
    messages_sent: int
    total_emeralds: int
    total_likes_received: int
    achievements_unlocked: int
    cosmetics_owned: int
    accuracy_percentage: float

# =====================
# CHAT & MESSAGE MODELS
# =====================

class Message(BaseModel):
    id: Optional[str] = None
    room_id: str
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    content: str = Field(..., max_length=500)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    reactions: dict = {}  # {emoji: count}
    is_edited: bool = False

class MessageCreate(BaseModel):
    room_id: str
    content: str = Field(..., max_length=500)

class MessageUpdate(BaseModel):
    content: str = Field(..., max_length=500)

class Room(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    creator_id: str
    members_count: int
    created_at: datetime
    updated_at: datetime
    is_public: bool = True

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    is_public: bool = True

class RoomMember(BaseModel):
    room_id: str
    user_id: str
    joined_at: datetime
    role: str = "member"  # member or admin

# =====================
# GAMIFICATION MODELS
# =====================

class ChallengeType(str, Enum):
    SPEED_TAP = "speed_tap"
    PATTERN_MEMORY = "pattern_memory"
    RAPID_CHOICE = "rapid_choice"
    FLICK_MASTER = "flick_master"
    COLOR_MATCH = "color_match"

class ChallengeDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    LEGENDARY = "legendary"

class Challenge(BaseModel):
    id: str
    title: str
    description: str
    type: ChallengeType
    difficulty: ChallengeDifficulty
    reward_emeralds: int
    reward_xp: int
    time_limit_seconds: int
    available_daily: bool
    created_at: datetime

class ChallengeSubmission(BaseModel):
    challenge_id: str
    user_id: str
    score: int
    submitted_at: Optional[datetime] = None

class ChallengeResult(BaseModel):
    success: bool
    score: int
    emeralds_earned: int
    xp_earned: int
    new_level: Optional[int] = None
    achievement_unlocked: Optional[str] = None
    mystery_box_unlocked: bool = False

class ClashBattle(BaseModel):
    id: str
    user_1_id: str
    user_2_id: str
    user_1_name: str
    user_2_name: str
    user_1_score: int = 0
    user_2_score: int = 0
    status: str = "active"  # active, completed, cancelled
    started_at: datetime
    ended_at: Optional[datetime] = None
    winner_id: Optional[str] = None

class ClashBattleCreate(BaseModel):
    challenge_type: ChallengeType

class ClashUpdate(BaseModel):
    clash_id: str
    user_id: str
    score_increment: int

# =====================
# REWARD MODELS
# =====================

class SpinWheelResult(BaseModel):
    reward: int
    is_rare: bool = False
    is_legendary: bool = False
    next_spin: datetime

class MysteryBox(BaseModel):
    id: str
    user_id: str
    rarity: str  # common, rare, legendary, mythic
    opened: bool = False
    created_at: datetime
    opened_at: Optional[datetime] = None

class MysteryBoxReward(BaseModel):
    emeralds: int = 0
    cosmetic_id: Optional[str] = None
    cosmetic_name: Optional[str] = None
    rarity: Optional[str] = None
    xp_boost: Optional[int] = None

class UserCosmetic(BaseModel):
    id: str
    user_id: str
    cosmetic_id: str
    cosmetic_name: str
    cosmetic_type: str  # username_color, glow_effect, border, badge, title
    rarity: str
    equipped: bool = False
    obtained_at: datetime

class CosmeticItem(BaseModel):
    id: str
    name: str
    type: str
    rarity: str
    cost_emeralds: Optional[int] = None
    description: str

# =====================
# LEADERBOARD MODELS
# =====================

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    xp: int
    level: int
    streak_days: int
    change_from_yesterday: int  # positive or negative
    badge: Optional[str] = None

class LeaderboardType(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"
    DAILY_CLASH = "daily_clash"
    ROOM = "room"

# =====================
# ACHIEVEMENT MODELS
# =====================

class Achievement(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    condition: str  # JSON describing the condition
    reward_xp: int
    created_at: datetime

class UserAchievement(BaseModel):
    id: str
    user_id: str
    achievement_id: str
    achievement_name: str
    unlocked_at: datetime

class AchievementList(BaseModel):
    achievements: List[UserAchievement]
    total: int
    percentage_unlocked: float

# =====================
# STREAKS & DAILY MODELS
# =====================

class DailyStreak(BaseModel):
    user_id: str
    current_streak: int
    longest_streak: int
    last_activity_date: datetime
    multiplier: float  # XP multiplier based on streak

class DailyChallenge(BaseModel):
    id: str
    date: datetime
    challenge_id: str
    is_completed: bool
    reward_bonus: int

class DailyStats(BaseModel):
    user_id: str
    date: datetime
    messages_sent: int
    challenges_completed: int
    emeralds_earned: int
    xp_earned: int

# =====================
# RESPONSE MODELS
# =====================

class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    status_code: int

class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[dict]

# =====================
# NOTIFICATION MODELS
# =====================

class NotificationType(str, Enum):
    LEVEL_UP = "level_up"
    ACHIEVEMENT = "achievement"
    STREAK_MILESTONE = "streak_milestone"
    FRIEND_ACTIVITY = "friend_activity"
    MESSAGE_REACTION = "message_reaction"
    REWARD = "reward"
    CHALLENGE_COMPLETE = "challenge_complete"

class Notification(BaseModel):
    id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    data: Optional[dict] = None
    read: bool = False
    created_at: datetime
