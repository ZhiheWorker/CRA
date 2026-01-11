import uuid

class LeagueLevel:
    def __init__(self, name, league_id, clubs=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.league_id = league_id
        self.clubs = clubs or []
        self.rankings = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "league_id": self.league_id,
            "clubs": self.clubs,
            "rankings": self.rankings
        }
    
    @classmethod
    def from_dict(cls, data):
        league_level = cls(
            data.get("name"),
            data.get("league_id"),
            data.get("clubs")
        )
        league_level.id = data.get("id", str(uuid.uuid4()))
        league_level.rankings = data.get("rankings", [])
        return league_level