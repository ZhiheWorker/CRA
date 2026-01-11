import uuid

class NationalTeam:
    def __init__(self, country_name, coach):
        self.id = str(uuid.uuid4())
        self.country_name = country_name
        self.coach = coach
        self.players = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "country_name": self.country_name,
            "coach": self.coach,
            "players": self.players
        }
    
    @classmethod
    def from_dict(cls, data):
        national_team = cls(
            data.get("country_name"),
            data.get("coach")
        )
        national_team.id = data.get("id", str(uuid.uuid4()))
        national_team.players = data.get("players", [])
        return national_team