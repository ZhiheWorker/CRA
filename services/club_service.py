from ..data.storage import Storage
from ..models.club import Club

class ClubService:
    def __init__(self):
        self.storage = Storage()
    
    async def get_all_clubs(self):
        clubs_data = await self.storage.get_all("clubs")
        return clubs_data
    
    async def get_club_by_id(self, club_id):
        return await self.storage.get_by_id("clubs", club_id)
    
    async def create_club(self, name, league, league_level, home_stadium, coach):
        club = Club(name, league, league_level, home_stadium, coach)
        return await self.storage.create("clubs", club.to_dict())
    
    async def update_club(self, club_id, updates):
        club_data = await self.storage.get_by_id("clubs", club_id)
        if not club_data:
            return None
        
        club = Club.from_dict(club_data)
        for key, value in updates.items():
            if hasattr(club, key):
                setattr(club, key, value)
        
        return await self.storage.update("clubs", club_id, club.to_dict())
    
    async def delete_club(self, club_id):
        return await self.storage.delete("clubs", club_id)
    
    async def get_clubs_by_league(self, league_id):
        clubs_data = await self.storage.get_all("clubs")
        return [club for club in clubs_data if club.get("league") == league_id]
    
    async def get_clubs_by_league_level(self, league_level_id):
        clubs_data = await self.storage.get_all("clubs")
        return [club for club in clubs_data if club.get("league_level") == league_level_id]
    
    async def update_club_stats(self, club_id, stats_updates):
        club_data = await self.storage.get_by_id("clubs", club_id)
        if not club_data:
            return None
        
        club = Club.from_dict(club_data)
        for key, value in stats_updates.items():
            if key in club.stats:
                club.stats[key] = value
        
        return await self.storage.update("clubs", club_id, club.to_dict())
    
    async def add_player_to_club(self, club_id, player_id):
        club_data = await self.storage.get_by_id("clubs", club_id)
        if not club_data:
            return None
        
        club = Club.from_dict(club_data)
        if player_id not in club.players:
            club.players.append(player_id)
            return await self.storage.update("clubs", club_id, club.to_dict())
        return club_data
    
    async def remove_player_from_club(self, club_id, player_id):
        club_data = await self.storage.get_by_id("clubs", club_id)
        if not club_data:
            return None
        
        club = Club.from_dict(club_data)
        if player_id in club.players:
            club.players.remove(player_id)
            return await self.storage.update("clubs", club_id, club.to_dict())
        return club_data