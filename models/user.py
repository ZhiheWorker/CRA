import uuid

class User:
    def __init__(self, username, password, role="user", permissions=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.role = role
        self.permissions = permissions or []
        self.created_at = None
        self.updated_at = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "permissions": self.permissions
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(
            data.get("username"),
            data.get("password"),
            data.get("role", "user"),
            data.get("permissions", [])
        )
        user.id = data.get("id", str(uuid.uuid4()))
        return user