from ..data.storage import Storage
from ..models.player import Player

class PlayerService:
    def __init__(self):
        self.storage = Storage()
    
    async def get_all_players(self):
        players_data = await self.storage.get_all("players")
        return players_data
    
    async def get_player_by_id(self, player_id):
        return await self.storage.get_by_id("players", player_id)
    
    async def create_player(self, name, position, qq, game_id, club=None, national_team=None):
        player = Player(name, position, qq, game_id, club, national_team)
        return await self.storage.create("players", player.to_dict())
    
    async def update_player(self, player_id, updates):
        player_data = await self.storage.get_by_id("players", player_id)
        if not player_data:
            return None
        
        player = Player.from_dict(player_data)
        for key, value in updates.items():
            if hasattr(player, key):
                setattr(player, key, value)
        
        return await self.storage.update("players", player_id, player.to_dict())
    
    async def delete_player(self, player_id):
        return await self.storage.delete("players", player_id)
    
    async def get_players_by_club(self, club_id):
        players_data = await self.storage.get_all("players")
        return [player for player in players_data if player.get("club") == club_id]
    
    async def get_players_by_national_team(self, national_team_id):
        players_data = await self.storage.get_all("players")
        return [player for player in players_data if player.get("national_team") == national_team_id]
    
    async def update_player_stats(self, player_id, stats_updates):
        player_data = await self.storage.get_by_id("players", player_id)
        if not player_data:
            return None
        
        player = Player.from_dict(player_data)
        for key, value in stats_updates.items():
            if key in player.stats:
                player.stats[key] += value
        
        return await self.storage.update("players", player_id, player.to_dict())