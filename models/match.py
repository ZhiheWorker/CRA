import uuid

class Match:
    def __init__(self, home_team, away_team, match_time, location):
        self.id = str(uuid.uuid4())
        self.home_team = home_team
        self.away_team = away_team
        self.match_time = match_time
        self.location = location
        self.score = {
            "home": 0,
            "away": 0
        }
        self.goal_scorers = []
        self.status = "scheduled"  # scheduled, in_progress, completed
        self.match_type = "league"  # league, cup, friendly
    
    def to_dict(self):
        return {
            "id": self.id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "match_time": self.match_time,
            "location": self.location,
            "score": self.score,
            "goal_scorers": self.goal_scorers,
            "status": self.status,
            "match_type": self.match_type
        }
    
    @classmethod
    def from_dict(cls, data):
        match = cls(
            data.get("home_team"),
            data.get("away_team"),
            data.get("match_time"),
            data.get("location")
        )
        match.id = data.get("id", str(uuid.uuid4()))
        match.score = data.get("score", {
            "home": 0,
            "away": 0
        })
        match.goal_scorers = data.get("goal_scorers", [])
        match.status = data.get("status", "scheduled")
        match.match_type = data.get("match_type", "league")
        return match