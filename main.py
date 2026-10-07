import ssl_trust  # noqa: F401  must run before httpx clients are created

from fastapi import FastAPI, HTTPException, WebSocket, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from typing import Optional, List
import json
from datetime import datetime
import asyncio

from models import *
from database import db
from auth import get_current_user, create_access_token
from websocket_manager import manager

# =====================
# LIFESPAN MANAGEMENT
# =====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

# =====================
# FASTAPI APP SETUP
# =====================

app = FastAPI(
    title="GRIND - Gamified Chat API",
    description="Real-time chat with gamification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# AUTH ENDPOINTS
# =====================

@app.post("/api/auth/register", response_model=dict)
async def register(user_data: UserRegister):
    """Register a new user"""
    try:
        # This would integrate with Supabase Auth
        # For now, we'll assume Supabase auth handles this
        # and we create the profile
        from supabase import create_client
        import uuid
        
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Create user in Supabase Auth
        res = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        user_id = res.user.id
        
        # Create user profile
        await db.create_user(user_id, user_data.email, user_data.username)
        
        # Create access token
        access_token = create_access_token({"sub": user_id})
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id,
            "username": user_data.username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login user"""
    try:
        from supabase import create_client
        
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Login with Supabase Auth
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        user_id = res.user.id
        access_token = create_access_token({"sub": user_id})
        
        user = await db.get_user(user_id)
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id,
            "username": user["username"]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# =====================
# USER ENDPOINTS
# =====================

@app.get("/api/users/me", response_model=UserProfile)
async def get_current_user_profile(user_id: str = Depends(get_current_user)):
    """Get current user profile"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """Get user profile by ID"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/{user_id}/stats", response_model=UserStats)
async def get_user_stats(user_id: str):
    """Get user statistics"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get additional stats from database
    return {
        "user_id": user_id,
        "level": user["level"],
        "total_xp": user["total_xp"],
        "messages_sent": 0,  # Would aggregate from messages table
        "total_emeralds": user["emeralds"],
        "total_likes_received": 0,  # Would aggregate from reactions
        "achievements_unlocked": 0,  # Would count from user_achievements
        "cosmetics_owned": 0,  # Would count from user_cosmetics
        "accuracy_percentage": 0.0  # Would calculate from submissions
    }

# =====================
# CHAT/MESSAGE ENDPOINTS
# =====================

@app.post("/api/rooms", response_model=dict)
async def create_room(room_data: RoomCreate, user_id: str = Depends(get_current_user)):
    """Create a new room"""
    room = await db.create_room(
        name=room_data.name,
        creator_id=user_id,
        description=room_data.description,
        is_public=room_data.is_public
    )
    if not room:
        raise HTTPException(status_code=400, detail="Failed to create room")
    return {"success": True, "room": room}

@app.get("/api/rooms/{room_id}", response_model=dict)
async def get_room(room_id: str):
    """Get room details"""
    room = await db.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.get("/api/rooms/{room_id}/messages", response_model=list)
async def get_room_messages(
    room_id: str,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Get messages from a room"""
    messages = await db.get_messages(room_id, limit, offset)
    return messages

@app.post("/api/messages", response_model=dict)
async def send_message(message_data: MessageCreate, user_id: str = Depends(get_current_user)):
    """Send a message"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    message = await db.create_message(
        room_id=message_data.room_id,
        user_id=user_id,
        username=user["username"],
        content=message_data.content,
        avatar_url=user.get("avatar_url")
    )
    
    if not message:
        raise HTTPException(status_code=400, detail="Failed to send message")
    
    # Award XP and emeralds for messaging
    await db.update_user_stats(user_id, emeralds=10, xp=10)
    
    # Broadcast to WebSocket
    await manager.broadcast_room(
        room_id=message_data.room_id,
        message={
            "type": "message",
            "data": message
        }
    )
    
    return {"success": True, "message": message}

@app.post("/api/messages/{message_id}/reactions", response_model=dict)
async def add_reaction(message_id: str, emoji: str, user_id: str = Depends(get_current_user)):
    """Add reaction to a message"""
    message = await db.add_reaction(message_id, emoji)
    if not message:
        raise HTTPException(status_code=400, detail="Failed to add reaction")
    
    # Broadcast reaction update
    await manager.broadcast(
        message={
            "type": "reaction",
            "data": {"message_id": message_id, "reactions": message["reactions"]}
        }
    )
    
    return {"success": True, "reactions": message["reactions"]}

# =====================
# CHALLENGE ENDPOINTS
# =====================

@app.get("/api/challenges", response_model=list)
async def get_challenges(difficulty: Optional[str] = None):
    """Get available challenges"""
    challenges = await db.get_challenges(difficulty)
    return challenges

@app.post("/api/challenges/{challenge_id}/submit", response_model=dict)
async def submit_challenge(challenge_id: str, score: int, user_id: str = Depends(get_current_user)):
    """Submit challenge completion"""
    result = await db.submit_challenge(challenge_id, user_id, score)
    
    if result["success"]:
        # Broadcast achievement
        await manager.broadcast(
            message={
                "type": "challenge_complete",
                "data": {
                    "user_id": user_id,
                    "challenge_id": challenge_id,
                    "emeralds": result["emeralds_earned"]
                }
            }
        )
    
    return result

# =====================
# CLASH BATTLE ENDPOINTS
# =====================

@app.post("/api/clash/create", response_model=dict)
async def create_clash_battle(user_id: str = Depends(get_current_user)):
    """Create a new clash battle"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find random opponent
    # This would typically select a random user online
    # For now, we'll create with a test opponent
    import random
    import uuid
    
    opponent_id = str(uuid.uuid4())  # Placeholder
    
    clash = await db.create_clash(
        user_1_id=user_id,
        user_1_name=user["username"],
        user_2_id=opponent_id,
        user_2_name="Opponent"
    )
    
    if not clash:
        raise HTTPException(status_code=400, detail="Failed to create clash")
    
    return {"success": True, "clash": clash}

@app.post("/api/clash/{clash_id}/update-score", response_model=dict)
async def update_clash_score(clash_id: str, score_increment: int, user_id: str = Depends(get_current_user)):
    """Update score in a clash battle"""
    clash = await db.update_clash_score(clash_id, user_id, score_increment)
    if not clash:
        raise HTTPException(status_code=400, detail="Failed to update score")
    
    # Broadcast update
    await manager.broadcast(
        message={
            "type": "clash_update",
            "data": clash
        }
    )
    
    return {"success": True, "clash": clash}

@app.post("/api/clash/{clash_id}/end", response_model=dict)
async def end_clash_battle(clash_id: str, winner_id: str, user_id: str = Depends(get_current_user)):
    """End a clash battle"""
    clash = await db.end_clash(clash_id, winner_id)
    if not clash:
        raise HTTPException(status_code=400, detail="Failed to end clash")
    
    # Broadcast end
    await manager.broadcast(
        message={
            "type": "clash_end",
            "data": clash
        }
    )
    
    return {"success": True, "clash": clash}

# =====================
# REWARDS ENDPOINTS
# =====================

@app.post("/api/spin-wheel", response_model=dict)
async def spin_wheel(user_id: str = Depends(get_current_user)):
    """Spin the daily reward wheel"""
    # Check if already spun today
    last_spin = await db.get_last_spin(user_id)
    if last_spin:
        from datetime import date
        if last_spin.date() == date.today():
            raise HTTPException(status_code=429, detail="Already spun today. Try again tomorrow.")
    
    # Generate random reward
    import random
    rewards = [50, 100, 200, 500, 1000]
    weights = [30, 40, 20, 8, 2]  # probability percentages
    
    reward = random.choices(rewards, weights=weights, k=1)[0]
    is_rare = reward >= 500
    
    result = await db.record_spin(user_id, reward, is_rare)
    
    if result["success"]:
        await manager.broadcast(
            message={
                "type": "spin_result",
                "data": {
                    "user_id": user_id,
                    "reward": reward,
                    "is_rare": is_rare
                }
            }
        )
    
    return result

@app.post("/api/mystery-boxes/{box_id}/open", response_model=dict)
async def open_mystery_box(box_id: str, user_id: str = Depends(get_current_user)):
    """Open a mystery box"""
    result = await db.open_mystery_box(box_id)
    
    if result["success"]:
        await manager.broadcast(
            message={
                "type": "box_opened",
                "data": {
                    "user_id": user_id,
                    "rarity": result["rarity"],
                    "emeralds": result["emeralds_earned"]
                }
            }
        )
    
    return result

# =====================
# LEADERBOARD ENDPOINTS
# =====================

@app.get("/api/leaderboard", response_model=list)
async def get_leaderboard(
    leaderboard_type: str = Query("weekly"),
    limit: int = Query(10, le=100),
    offset: int = Query(0, ge=0)
):
    """Get leaderboard"""
    leaderboard = await db.get_leaderboard(leaderboard_type, limit, offset)
    return leaderboard

@app.get("/api/leaderboard/user/{user_id}/rank", response_model=dict)
async def get_user_rank(user_id: str):
    """Get user's rank on leaderboard"""
    leaderboard = await db.get_leaderboard(limit=10000)  # Get all to find rank
    
    for entry in leaderboard:
        if entry["user_id"] == user_id:
            return {"success": True, "rank": entry["rank"], "xp": entry["xp"]}
    
    return {"success": False, "rank": None}

# =====================
# STREAKS & DAILY ENDPOINTS
# =====================

@app.post("/api/streaks/{user_id}/update", response_model=dict)
async def update_user_streak(user_id: str, current_user_id: str = Depends(get_current_user)):
    """Update user's daily streak"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    streak = await db.update_streak(user_id)
    if not streak:
        raise HTTPException(status_code=400, detail="Failed to update streak")
    
    # Broadcast milestone if reached
    if streak["current_streak"] % 7 == 0:
        await manager.broadcast(
            message={
                "type": "streak_milestone",
                "data": {
                    "user_id": user_id,
                    "streak": streak["current_streak"]
                }
            }
        )
    
    return {"success": True, "streak": streak}

# =====================
# COSMETICS ENDPOINTS
# =====================

@app.get("/api/users/{user_id}/cosmetics", response_model=list)
async def get_user_cosmetics(user_id: str):
    """Get user's cosmetics"""
    cosmetics = await db.get_user_cosmetics(user_id)
    return cosmetics

@app.post("/api/cosmetics/{cosmetic_id}/equip", response_model=dict)
async def equip_cosmetic(cosmetic_id: str, user_id: str = Depends(get_current_user)):
    """Equip a cosmetic"""
    cosmetic = await db.equip_cosmetic(user_id, cosmetic_id)
    if not cosmetic:
        raise HTTPException(status_code=400, detail="Failed to equip cosmetic")
    
    return {"success": True, "cosmetic": cosmetic}

# =====================
# WEBSOCKET ENDPOINTS
# =====================

@app.websocket("/ws/chat/{room_id}/{user_id}")
async def websocket_chat(websocket: WebSocket, room_id: str, user_id: str):
    """WebSocket connection for real-time chat"""
    await manager.connect(websocket, room_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast to room
            await manager.broadcast_room(
                room_id=room_id,
                message={
                    "type": "message",
                    "user_id": user_id,
                    "data": message_data
                }
            )
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(room_id, user_id)

@app.websocket("/ws/leaderboard")
async def websocket_leaderboard(websocket: WebSocket):
    """WebSocket connection for real-time leaderboard updates"""
    await manager.connect_global(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Just keep connection alive
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await manager.disconnect_global(websocket)

# =====================
# HEALTH CHECK
# =====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# =====================
# ROOT
# =====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "GRIND - Gamified Chat",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
