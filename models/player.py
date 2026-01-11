import uuid

class Player:
    def __init__(self, name, position, qq, game_id, club=None, national_team=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.position = position
        self.qq = qq
        self.game_id = game_id
        self.club = club
        self.national_team = national_team
        self.stats = {
            "goals": 0,
            "assists": 0,
            "apps": 0,
            "yellow_cards": 0,
            "red_cards": 0
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "qq": self.qq,
            "game_id": self.game_id,
            "club": self.club,
            "national_team": self.national_team,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(
            data.get("name"),
            data.get("position"),
            data.get("qq"),
            data.get("game_id"),
            data.get("club"),
            data.get("national_team")
        )
        player.id = data.get("id", str(uuid.uuid4()))
        player.stats = data.get("stats", {
            "goals": 0,
            "assists": 0,
            "apps": 0,
            "yellow_cards": 0,
            "red_cards": 0
        })
        return player