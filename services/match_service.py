from ..data.storage import Storage
from ..models.match import Match

class MatchService:
    def __init__(self):
        self.storage = Storage()
    
    async def get_all_matches(self):
        matches_data = await self.storage.get_all("matches")
        return matches_data
    
    async def get_match_by_id(self, match_id):
        return await self.storage.get_by_id("matches", match_id)
    
    async def create_match(self, home_team, away_team, match_time, location, match_type="league"):
        match = Match(home_team, away_team, match_time, location)
        match.match_type = match_type
        return await self.storage.create("matches", match.to_dict())
    
    async def update_match(self, match_id, updates):
        match_data = await self.storage.get_by_id("matches", match_id)
        if not match_data:
            return None
        
        match = Match.from_dict(match_data)
        for key, value in updates.items():
            if hasattr(match, key):
                setattr(match, key, value)
        
        return await self.storage.update("matches", match_id, match.to_dict())
    
    async def delete_match(self, match_id):
        return await self.storage.delete("matches", match_id)
    
    async def update_match_score(self, match_id, home_score, away_score):
        match_data = await self.storage.get_by_id("matches", match_id)
        if not match_data:
            return None
        
        match = Match.from_dict(match_data)
        match.score["home"] = home_score
        match.score["away"] = away_score
        match.status = "completed"
        
        return await self.storage.update("matches", match_id, match.to_dict())
    
    async def get_matches_by_team(self, team_id):
        matches_data = await self.storage.get_all("matches")
        return [match for match in matches_data if match.get("home_team") == team_id or match.get("away_team") == team_id]
    
    async def get_matches_by_status(self, status):
        matches_data = await self.storage.get_all("matches")
        return [match for match in matches_data if match.get("status") == status]
    
    async def get_matches_by_type(self, match_type):
        matches_data = await self.storage.get_all("matches")
        return [match for match in matches_data if match.get("match_type") == match_type]
    
    async def add_goal_scorer(self, match_id, player_id, team, minute):
        match_data = await self.storage.get_by_id("matches", match_id)
        if not match_data:
            return None
        
        match = Match.from_dict(match_data)
        match.goal_scorers.append({
            "player_id": player_id,
            "team": team,
            "minute": minute
        })
        
        return await self.storage.update("matches", match_id, match.to_dict())