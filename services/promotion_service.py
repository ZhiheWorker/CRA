from ..data.storage import Storage
from ..models.club import Club

class PromotionService:
    def __init__(self):
        self.storage = Storage()
    
    async def execute_promotion_relegation(self, league_id):
        league_data = await self.storage.get_by_id("leagues", league_id)
        if not league_data:
            return None
        
        promotion_relegation_rules = league_data.get("promotion_relegation_rules", {"promote": 2, "relegate": 2})
        promote_count = promotion_relegation_rules["promote"]
        relegate_count = promotion_relegation_rules["relegate"]
        
        league_levels_data = await self.storage.get_all("league_levels")
        league_levels = [level for level in league_levels_data if level.get("league_id") == league_id]
        
        # Sort levels by name (assuming lower numbers are higher levels, e.g., "Level 1" > "Level 2")
        league_levels.sort(key=lambda x: x.get("name"))
        
        if len(league_levels) < 2:
            return {"message": "Not enough league levels to perform promotion/relegation"}
        
        results = {
            "promoted": [],
            "relegated": []
        }
        
        # Process each level except the highest one for relegation
        for i, level in enumerate(league_levels):
            clubs_data = await self.storage.get_all("clubs")
            clubs_in_level = [club for club in clubs_data if club.get("league_level") == level["id"]]
            
            # Sort clubs by points (descending), then goal difference (descending), then goals for (descending)
            clubs_in_level.sort(
                key=lambda x: (
                    x.get("stats", {}).get("points", 0),
                    x.get("stats", {}).get("goal_difference", 0),
                    x.get("stats", {}).get("goals_for", 0)
                ),
                reverse=True
            )
            
            # Promotion: clubs from lower levels move up to higher levels
            if i < len(league_levels) - 1:
                next_level = league_levels[i + 1]
                promote_clubs = clubs_in_level[:promote_count]
                
                for club_data in promote_clubs:
                    club = Club.from_dict(club_data)
                    club.league_level = next_level["id"]
                    await self.storage.update("clubs", club.id, club.to_dict())
                    results["promoted"].append({
                        "club": club.name,
                        "from_level": level["name"],
                        "to_level": next_level["name"]
                    })
            
            # Relegation: clubs from higher levels move down to lower levels
            if i > 0:
                prev_level = league_levels[i - 1]
                relegate_clubs = clubs_in_level[-relegate_count:]
                
                for club_data in relegate_clubs:
                    club = Club.from_dict(club_data)
                    club.league_level = prev_level["id"]
                    await self.storage.update("clubs", club.id, club.to_dict())
                    results["relegated"].append({
                        "club": club.name,
                        "from_level": level["name"],
                        "to_level": prev_level["name"]
                    })
        
        return results
    
    async def calculate_club_rankings(self, league_level_id):
        clubs_data = await self.storage.get_all("clubs")
        clubs_in_level = [club for club in clubs_data if club.get("league_level") == league_level_id]
        
        # Sort clubs by points (descending), then goal difference (descending), then goals for (descending)
        clubs_in_level.sort(
            key=lambda x: (
                x.get("stats", {}).get("points", 0),
                x.get("stats", {}).get("goal_difference", 0),
                x.get("stats", {}).get("goals_for", 0)
            ),
            reverse=True
        )
        
        rankings = []
        for rank, club in enumerate(clubs_in_level, start=1):
            rankings.append({
                "rank": rank,
                "club_id": club["id"],
                "club_name": club["name"],
                "points": club.get("stats", {}).get("points", 0),
                "goal_difference": club.get("stats", {}).get("goal_difference", 0),
                "goals_for": club.get("stats", {}).get("goals_for", 0)
            })
        
        # Update league level rankings
        level_data = await self.storage.get_by_id("league_levels", league_level_id)
        if level_data:
            level_data["rankings"] = rankings
            await self.storage.update("league_levels", league_level_id, level_data)
        
        return rankings
    
    async def get_league_table(self, league_level_id):
        level_data = await self.storage.get_by_id("league_levels", league_level_id)
        if not level_data:
            return None
        
        if "rankings" not in level_data or not level_data["rankings"]:
            await self.calculate_club_rankings(league_level_id)
            level_data = await self.storage.get_by_id("league_levels", league_level_id)
        
        return level_data["rankings"]