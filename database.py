import ssl_trust  # noqa: F401  must run before the Supabase client is created

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseDB:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # =====================
    # USER OPERATIONS
    # =====================
    
    async def create_user(self, user_id: str, email: str, username: str) -> Dict:
        """Create new user profile"""
        try:
            response = self.client.table("users").insert({
                "id": user_id,
                "email": email,
                "username": username,
                "level": 1,
                "total_xp": 0,
                "emeralds": 0,
                "streak_days": 0,
                "last_login": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    async def get_user(self, user_id: str) -> Dict:
        """Get user profile"""
        try:
            response = self.client.table("users").select("*").eq("id", user_id).single().execute()
            return response.data
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def update_user_stats(self, user_id: str, emeralds: int = 0, xp: int = 0) -> Dict:
        """Update user emeralds and XP"""
        try:
            user = await self.get_user(user_id)
            if not user:
                return None
            
            new_xp = user["total_xp"] + xp
            new_emeralds = user["emeralds"] + emeralds
            new_level = (new_xp // 1000) + 1  # Level up every 1000 XP
            
            response = self.client.table("users").update({
                "total_xp": new_xp,
                "emeralds": new_emeralds,
                "level": new_level,
                "updated_at": datetime.now().isoformat()
            }).eq("id", user_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating user stats: {e}")
            return None
    
    # =====================
    # MESSAGE OPERATIONS
    # =====================
    
    async def create_message(self, room_id: str, user_id: str, username: str, content: str, avatar_url: Optional[str] = None) -> Dict:
        """Create a new message"""
        try:
            response = self.client.table("messages").insert({
                "room_id": room_id,
                "user_id": user_id,
                "username": username,
                "avatar_url": avatar_url,
                "content": content,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "reactions": {},
                "is_edited": False
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    async def get_messages(self, room_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get messages from a room"""
        try:
            response = self.client.table("messages")\
                .select("*")\
                .eq("room_id", room_id)\
                .order("created_at", desc=False)\
                .range(offset, offset + limit - 1)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    async def add_reaction(self, message_id: str, emoji: str) -> Dict:
        """Add reaction to a message"""
        try:
            message = self.client.table("messages").select("reactions").eq("id", message_id).single().execute()
            reactions = message.data["reactions"] if message.data else {}
            
            reactions[emoji] = reactions.get(emoji, 0) + 1
            
            response = self.client.table("messages").update({
                "reactions": reactions,
                "updated_at": datetime.now().isoformat()
            }).eq("id", message_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding reaction: {e}")
            return None
    
    # =====================
    # ROOM OPERATIONS
    # =====================
    
    async def create_room(self, name: str, creator_id: str, description: Optional[str] = None, is_public: bool = True) -> Dict:
        """Create a new room"""
        try:
            response = self.client.table("rooms").insert({
                "name": name,
                "description": description,
                "creator_id": creator_id,
                "members_count": 1,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "is_public": is_public
            }).execute()
            
            if response.data:
                room_id = response.data[0]["id"]
                # Add creator as member
                await self.add_room_member(room_id, creator_id, "admin")
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating room: {e}")
            return None
    
    async def get_room(self, room_id: str) -> Dict:
        """Get room details"""
        try:
            response = self.client.table("rooms").select("*").eq("id", room_id).single().execute()
            return response.data
        except Exception as e:
            print(f"Error getting room: {e}")
            return None
    
    async def add_room_member(self, room_id: str, user_id: str, role: str = "member") -> Dict:
        """Add member to room"""
        try:
            response = self.client.table("room_members").insert({
                "room_id": room_id,
                "user_id": user_id,
                "joined_at": datetime.now().isoformat(),
                "role": role
            }).execute()
            
            # Increment members count
            room = await self.get_room(room_id)
            self.client.table("rooms").update({
                "members_count": room["members_count"] + 1
            }).eq("id", room_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding room member: {e}")
            return None
    
    # =====================
    # CHALLENGE OPERATIONS
    # =====================
    
    async def create_challenge(self, title: str, description: str, challenge_type: str, 
                              difficulty: str, reward_emeralds: int, reward_xp: int, 
                              time_limit: int) -> Dict:
        """Create a new challenge"""
        try:
            response = self.client.table("challenges").insert({
                "title": title,
                "description": description,
                "type": challenge_type,
                "difficulty": difficulty,
                "reward_emeralds": reward_emeralds,
                "reward_xp": reward_xp,
                "time_limit_seconds": time_limit,
                "available_daily": True,
                "created_at": datetime.now().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating challenge: {e}")
            return None
    
    async def get_challenges(self, difficulty: Optional[str] = None) -> List[Dict]:
        """Get all challenges"""
        try:
            query = self.client.table("challenges").select("*")
            if difficulty:
                query = query.eq("difficulty", difficulty)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error getting challenges: {e}")
            return []
    
    async def submit_challenge(self, challenge_id: str, user_id: str, score: int) -> Dict:
        """Submit challenge completion"""
        try:
            # Get challenge details
            challenge = self.client.table("challenges").select("*").eq("id", challenge_id).single().execute()
            challenge_data = challenge.data
            
            # Award rewards
            await self.update_user_stats(
                user_id,
                emeralds=challenge_data["reward_emeralds"],
                xp=challenge_data["reward_xp"]
            )
            
            # Log submission
            response = self.client.table("challenge_submissions").insert({
                "challenge_id": challenge_id,
                "user_id": user_id,
                "score": score,
                "submitted_at": datetime.now().isoformat()
            }).execute()
            
            return {
                "success": True,
                "emeralds_earned": challenge_data["reward_emeralds"],
                "xp_earned": challenge_data["reward_xp"],
                "submission_id": response.data[0]["id"] if response.data else None
            }
        except Exception as e:
            print(f"Error submitting challenge: {e}")
            return {"success": False, "error": str(e)}
    
    # =====================
    # CLASH BATTLE OPERATIONS
    # =====================
    
    async def create_clash(self, user_1_id: str, user_1_name: str, user_2_id: str, user_2_name: str) -> Dict:
        """Create a new clash battle"""
        try:
            response = self.client.table("clash_battles").insert({
                "user_1_id": user_1_id,
                "user_1_name": user_1_name,
                "user_2_id": user_2_id,
                "user_2_name": user_2_name,
                "user_1_score": 0,
                "user_2_score": 0,
                "status": "active",
                "started_at": datetime.now().isoformat(),
                "ended_at": None,
                "winner_id": None
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating clash: {e}")
            return None
    
    async def update_clash_score(self, clash_id: str, user_id: str, score_increment: int) -> Dict:
        """Update score in an active clash"""
        try:
            clash = self.client.table("clash_battles").select("*").eq("id", clash_id).single().execute()
            clash_data = clash.data
            
            if clash_data["user_1_id"] == user_id:
                new_score_1 = clash_data["user_1_score"] + score_increment
                response = self.client.table("clash_battles").update({
                    "user_1_score": new_score_1
                }).eq("id", clash_id).execute()
            else:
                new_score_2 = clash_data["user_2_score"] + score_increment
                response = self.client.table("clash_battles").update({
                    "user_2_score": new_score_2
                }).eq("id", clash_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating clash score: {e}")
            return None
    
    async def end_clash(self, clash_id: str, winner_id: str) -> Dict:
        """End a clash battle and award rewards"""
        try:
            clash = self.client.table("clash_battles").select("*").eq("id", clash_id).single().execute()
            clash_data = clash.data
            
            # Award winner
            await self.update_user_stats(winner_id, emeralds=200, xp=50)
            
            # Award loser (participation)
            loser_id = clash_data["user_2_id"] if clash_data["user_1_id"] == winner_id else clash_data["user_1_id"]
            await self.update_user_stats(loser_id, emeralds=50, xp=25)
            
            response = self.client.table("clash_battles").update({
                "status": "completed",
                "ended_at": datetime.now().isoformat(),
                "winner_id": winner_id
            }).eq("id", clash_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error ending clash: {e}")
            return None
    
    # =====================
    # STREAK OPERATIONS
    # =====================
    
    async def get_streak(self, user_id: str) -> Dict:
        """Get user's current streak"""
        try:
            response = self.client.table("streaks").select("*").eq("user_id", user_id).single().execute()
            return response.data
        except Exception as e:
            return {"current_streak": 0, "multiplier": 1.0}
    
    async def update_streak(self, user_id: str) -> Dict:
        """Update user's streak (called on daily activity)"""
        try:
            streak_data = await self.get_streak(user_id)
            last_date = streak_data.get("last_activity_date")
            
            today = datetime.now().date()
            last_date_obj = datetime.fromisoformat(last_date).date() if last_date else None
            
            if last_date_obj == today:
                # Already updated today
                return streak_data
            
            if last_date_obj == today - timedelta(days=1):
                # Consecutive day
                new_streak = streak_data["current_streak"] + 1
            else:
                # Streak broken
                new_streak = 1
            
            # Calculate multiplier (increases with streak)
            multiplier = 1.0 + (new_streak * 0.1)  # 1.1x at day 1, 1.2x at day 2, etc.
            multiplier = min(multiplier, 5.0)  # Cap at 5.0x
            
            response = self.client.table("streaks").upsert({
                "user_id": user_id,
                "current_streak": new_streak,
                "longest_streak": max(streak_data.get("longest_streak", 0), new_streak),
                "last_activity_date": datetime.now().isoformat(),
                "multiplier": multiplier
            }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating streak: {e}")
            return None
    
    # =====================
    # SPIN WHEEL OPERATIONS
    # =====================
    
    async def get_last_spin(self, user_id: str) -> Optional[datetime]:
        """Get user's last spin time"""
        try:
            response = self.client.table("spin_history")\
                .select("created_at")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                return datetime.fromisoformat(response.data[0]["created_at"])
            return None
        except Exception as e:
            return None
    
    async def record_spin(self, user_id: str, reward: int, is_rare: bool = False) -> Dict:
        """Record a spin and award reward"""
        try:
            # Award emeralds
            await self.update_user_stats(user_id, emeralds=reward, xp=10)
            
            # Log spin
            response = self.client.table("spin_history").insert({
                "user_id": user_id,
                "reward": reward,
                "is_rare": is_rare,
                "created_at": datetime.now().isoformat()
            }).execute()
            
            return {
                "success": True,
                "reward": reward,
                "is_rare": is_rare,
                "next_spin": (datetime.now() + timedelta(days=1)).isoformat()
            }
        except Exception as e:
            print(f"Error recording spin: {e}")
            return {"success": False, "error": str(e)}
    
    # =====================
    # MYSTERY BOX OPERATIONS
    # =====================
    
    async def unlock_mystery_box(self, user_id: str, rarity: str = "common") -> Dict:
        """Unlock a mystery box for user"""
        try:
            response = self.client.table("mystery_boxes").insert({
                "user_id": user_id,
                "rarity": rarity,
                "opened": False,
                "created_at": datetime.now().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error unlocking mystery box: {e}")
            return None
    
    async def open_mystery_box(self, box_id: str) -> Dict:
        """Open a mystery box and get reward"""
        try:
            box = self.client.table("mystery_boxes").select("*").eq("id", box_id).single().execute()
            box_data = box.data
            
            # Determine reward based on rarity
            rewards = {
                "common": {"emeralds": 50, "xp": 25},
                "rare": {"emeralds": 200, "xp": 75},
                "legendary": {"emeralds": 500, "xp": 150},
                "mythic": {"emeralds": 1000, "xp": 300}
            }
            
            reward = rewards.get(box_data["rarity"], rewards["common"])
            
            # Award rewards
            await self.update_user_stats(
                box_data["user_id"],
                emeralds=reward["emeralds"],
                xp=reward["xp"]
            )
            
            # Mark box as opened
            self.client.table("mystery_boxes").update({
                "opened": True,
                "opened_at": datetime.now().isoformat()
            }).eq("id", box_id).execute()
            
            return {
                "success": True,
                "rarity": box_data["rarity"],
                "emeralds_earned": reward["emeralds"],
                "xp_earned": reward["xp"]
            }
        except Exception as e:
            print(f"Error opening mystery box: {e}")
            return {"success": False, "error": str(e)}
    
    # =====================
    # LEADERBOARD OPERATIONS
    # =====================
    
    async def get_leaderboard(self, leaderboard_type: str = "weekly", limit: int = 10, offset: int = 0) -> List[Dict]:
        """Get leaderboard entries"""
        try:
            response = self.client.table("users")\
                .select("id, username, avatar_url, level, total_xp, streak_days")\
                .order("total_xp", desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            # Add rank
            leaderboard = []
            for idx, user in enumerate(response.data):
                leaderboard.append({
                    "rank": offset + idx + 1,
                    "user_id": user["id"],
                    "username": user["username"],
                    "avatar_url": user["avatar_url"],
                    "xp": user["total_xp"],
                    "level": user["level"],
                    "streak_days": user["streak_days"]
                })
            
            return leaderboard
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
    
    # =====================
    # COSMETICS OPERATIONS
    # =====================
    
    async def get_user_cosmetics(self, user_id: str) -> List[Dict]:
        """Get user's cosmetics"""
        try:
            response = self.client.table("user_cosmetics")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user cosmetics: {e}")
            return []
    
    async def equip_cosmetic(self, user_id: str, cosmetic_id: str) -> Dict:
        """Equip a cosmetic"""
        try:
            # First unequip all cosmetics of same type
            cosmetic = self.client.table("cosmetics").select("type").eq("id", cosmetic_id).single().execute()
            cosmetic_type = cosmetic.data["type"]
            
            self.client.table("user_cosmetics")\
                .update({"equipped": False})\
                .eq("user_id", user_id)\
                .execute()
            
            # Equip selected cosmetic
            response = self.client.table("user_cosmetics")\
                .update({"equipped": True})\
                .eq("user_id", user_id)\
                .eq("cosmetic_id", cosmetic_id)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error equipping cosmetic: {e}")
            return None

# Initialize database
db = SupabaseDB()
