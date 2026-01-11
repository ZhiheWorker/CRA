import uuid
import asyncio
from datetime import datetime, timedelta
from ..data.storage import Storage
from ..models.user import User

class AuthService:
    def __init__(self):
        self.storage = Storage()
        self.active_sessions = {}
        self.session_timeout = timedelta(hours=1)
    
    async def login(self, username, password):
        users = await self.storage.get_all("users")
        for user_data in users:
            if user_data["username"] == username and user_data["password"] == password:
                user = User.from_dict(user_data)
                session_id = str(uuid.uuid4())
                self.active_sessions[session_id] = {
                    "user": user,
                    "last_active": datetime.now()
                }
                return {
                    "session_id": session_id,
                    "user": user.to_dict()
                }
        return None
    
    async def logout(self, session_id):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False
    
    def get_user_from_session(self, session_id):
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        if datetime.now() - session["last_active"] > self.session_timeout:
            del self.active_sessions[session_id]
            return None
        
        session["last_active"] = datetime.now()
        return session["user"]
    
    async def get_user_info(self, session_id):
        user = self.get_user_from_session(session_id)
        if user:
            return user.to_dict()
        return None
    
    async def create_user(self, username, password, role="user", permissions=None):
        existing_users = await self.storage.get_all("users")
        for user_data in existing_users:
            if user_data["username"] == username:
                return None
        
        user = User(username, password, role, permissions)
        await self.storage.create("users", user.to_dict())
        return user.to_dict()
    
    async def update_user(self, user_id, updates):
        user_data = await self.storage.get_by_id("users", user_id)
        if not user_data:
            return None
        
        user = User.from_dict(user_data)
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        await self.storage.update("users", user_id, user.to_dict())
        return user.to_dict()
    
    async def delete_user(self, user_id):
        return await self.storage.delete("users", user_id)
    
    def is_session_valid(self, session_id):
        return self.get_user_from_session(session_id) is not None
    
    async def get_all_users(self):
        return await self.storage.get_all("users")
    
    async def cleanup_expired_sessions(self):
        now = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.active_sessions.items():
            if now - session_data["last_active"] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        return len(expired_sessions)
    
    async def init_admin_user(self):
        admin_users = await self.storage.get_by_field("users", "role", "admin")
        if not admin_users:
            admin_permissions = ["all"]
            admin_user = User("admin", "admin123", "admin", admin_permissions)
            await self.storage.create("users", admin_user.to_dict())
            print("Admin user created: username=admin, password=admin123")