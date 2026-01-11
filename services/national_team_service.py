from ..data.storage import Storage
from ..models.national_team import NationalTeam

class NationalTeamService:
    def __init__(self):
        self.storage = Storage()
    
    async def get_all_national_teams(self):
        national_teams_data = await self.storage.get_all("national_teams")
        return national_teams_data
    
    async def get_national_team_by_id(self, team_id):
        return await self.storage.get_by_id("national_teams", team_id)
    
    async def create_national_team(self, country_name, coach):
        national_team = NationalTeam(country_name, coach)
        return await self.storage.create("national_teams", national_team.to_dict())
    
    async def update_national_team(self, team_id, updates):
        team_data = await self.storage.get_by_id("national_teams", team_id)
        if not team_data:
            return None
        
        team = NationalTeam.from_dict(team_data)
        for key, value in updates.items():
            if hasattr(team, key):
                setattr(team, key, value)
        
        return await self.storage.update("national_teams", team_id, team.to_dict())
    
    async def delete_national_team(self, team_id):
        return await self.storage.delete("national_teams", team_id)
    
    async def add_player_to_national_team(self, team_id, player_id):
        team_data = await self.storage.get_by_id("national_teams", team_id)
        if not team_data:
            return None
        
        team = NationalTeam.from_dict(team_data)
        if player_id not in team.players:
            team.players.append(player_id)
            return await self.storage.update("national_teams", team_id, team.to_dict())
        return team_data
    
    async def remove_player_from_national_team(self, team_id, player_id):
        team_data = await self.storage.get_by_id("national_teams", team_id)
        if not team_data:
            return None
        
        team = NationalTeam.from_dict(team_data)
        if player_id in team.players:
            team.players.remove(player_id)
            return await self.storage.update("national_teams", team_id, team.to_dict())
        return team_data