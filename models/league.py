import uuid

class League:
    def __init__(self, name, season, promotion_relegation_rules=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.season = season
        self.league_levels = []
        self.promotion_relegation_rules = promotion_relegation_rules or {
            "promote": 2,
            "relegate": 2
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "season": self.season,
            "league_levels": self.league_levels,
            "promotion_relegation_rules": self.promotion_relegation_rules
        }
    
    @classmethod
    def from_dict(cls, data):
        league = cls(
            data.get("name"),
            data.get("season"),
            data.get("promotion_relegation_rules")
        )
        league.id = data.get("id", str(uuid.uuid4()))
        league.league_levels = data.get("league_levels", [])
        return league