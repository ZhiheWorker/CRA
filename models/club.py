import uuid

class Club:
    def __init__(self, name, league, league_level, home_stadium, coach):
        self.id = str(uuid.uuid4())
        self.name = name
        self.league = league
        self.league_level = league_level
        self.home_stadium = home_stadium
        self.coach = coach
        self.players = []
        self.stats = {
            "points": 0,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "league": self.league,
            "league_level": self.league_level,
            "home_stadium": self.home_stadium,
            "coach": self.coach,
            "players": self.players,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data):
        club = cls(
            data.get("name"),
            data.get("league"),
            data.get("league_level"),
            data.get("home_stadium"),
            data.get("coach")
        )
        club.id = data.get("id", str(uuid.uuid4()))
        club.players = data.get("players", [])
        club.stats = data.get("stats", {
            "points": 0,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0
        })
        return club