from ..data.storage import Storage
from ..models.league import League
from ..models.league_level import LeagueLevel

class LeagueService:
    def __init__(self):
        self.storage = Storage()
    
    async def get_all_leagues(self):
        leagues_data = await self.storage.get_all("leagues")
        return leagues_data
    
    async def get_league_by_id(self, league_id):
        return await self.storage.get_by_id("leagues", league_id)
    
    async def create_league(self, name, season, promotion_relegation_rules=None):
        league = League(name, season, promotion_relegation_rules)
        return await self.storage.create("leagues", league.to_dict())
    
    async def update_league(self, league_id, updates):
        league_data = await self.storage.get_by_id("leagues", league_id)
        if not league_data:
            return None
        
        league = League.from_dict(league_data)
        for key, value in updates.items():
            if hasattr(league, key):
                setattr(league, key, value)
        
        return await self.storage.update("leagues", league_id, league.to_dict())
    
    async def delete_league(self, league_id):
        return await self.storage.delete("leagues", league_id)
    
    async def get_league_levels(self, league_id):
        league_levels_data = await self.storage.get_all("league_levels")
        return [level for level in league_levels_data if level.get("league_id") == league_id]
    
    async def add_league_level(self, league_id, name):
        league_level = LeagueLevel(name, league_id)
        level_data = await self.storage.create("league_levels", league_level.to_dict())
        
        league_data = await self.storage.get_by_id("leagues", league_id)
        if league_data:
            league = League.from_dict(league_data)
            league.league_levels.append(level_data["id"])
            await self.storage.update("leagues", league_id, league.to_dict())
        
        return level_data
    
    async def update_league_level(self, level_id, updates):
        level_data = await self.storage.get_by_id("league_levels", level_id)
        if not level_data:
            return None
        
        level = LeagueLevel.from_dict(level_data)
        for key, value in updates.items():
            if hasattr(level, key):
                setattr(level, key, value)
        
        return await self.storage.update("league_levels", level_id, level.to_dict())
    
    async def delete_league_level(self, level_id):
        level_data = await self.storage.get_by_id("league_levels", level_id)
        if not level_data:
            return False
        
        league_id = level_data["league_id"]
        league_data = await self.storage.get_by_id("leagues", league_id)
        if league_data:
            league = League.from_dict(league_data)
            if level_id in league.league_levels:
                league.league_levels.remove(level_id)
                await self.storage.update("leagues", league_id, league.to_dict())
        
        return await self.storage.delete("league_levels", level_id)
    
    async def set_clubs_to_level(self, level_id, club_ids):
        level_data = await self.storage.get_by_id("league_levels", level_id)
        if not level_data:
            return None
        
        level = LeagueLevel.from_dict(level_data)
        level.clubs = club_ids
        
        return await self.storage.update("league_levels", level_id, level.to_dict())