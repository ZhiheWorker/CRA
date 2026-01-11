from .services import (
    AuthService,
    PlayerService,
    ClubService,
    LeagueService,
    NationalTeamService,
    MatchService,
    PromotionService
)
from .utils.permissions import Permissions

class CommandHandler:
    def __init__(self):
        self.auth_service = AuthService()
        self.player_service = PlayerService()
        self.club_service = ClubService()
        self.league_service = LeagueService()
        self.national_team_service = NationalTeamService()
        self.match_service = MatchService()
        self.promotion_service = PromotionService()
    
    async def handle_command(self, command, data, session_id):
        # 权限验证
        user = self.auth_service.get_user_from_session(session_id)
        
        # 无需权限的命令
        if command == "LOGIN":
            return await self.handle_login(data)
        
        if command == "PING":
            return self.handle_ping()
        
        # 需要权限验证的命令
        if not user:
            return {
                "status": "error",
                "message": "Unauthorized: Please login first",
                "command": command
            }
        
        if not Permissions.can_perform_action(user, command):
            return {
                "status": "error",
                "message": "Forbidden: You don't have permission to perform this action",
                "command": command
            }
        
        # 处理具体命令
        handlers = {
            "LOGOUT": self.handle_logout,
            "GET_USER_INFO": self.handle_get_user_info,
            "GET_PLAYERS": self.handle_get_players,
            "GET_PLAYER": self.handle_get_player,
            "ADD_PLAYER": self.handle_add_player,
            "UPDATE_PLAYER": self.handle_update_player,
            "DELETE_PLAYER": self.handle_delete_player,
            "GET_CLUBS": self.handle_get_clubs,
            "GET_CLUB": self.handle_get_club,
            "ADD_CLUB": self.handle_add_club,
            "UPDATE_CLUB": self.handle_update_club,
            "DELETE_CLUB": self.handle_delete_club,
            "GET_LEAGUES": self.handle_get_leagues,
            "GET_LEAGUE": self.handle_get_league,
            "ADD_LEAGUE": self.handle_add_league,
            "UPDATE_LEAGUE": self.handle_update_league,
            "DELETE_LEAGUE": self.handle_delete_league,
            "GET_LEAGUE_LEVELS": self.handle_get_league_levels,
            "ADD_LEAGUE_LEVEL": self.handle_add_league_level,
            "UPDATE_LEAGUE_LEVEL": self.handle_update_league_level,
            "DELETE_LEAGUE_LEVEL": self.handle_delete_league_level,
            "SET_CLUBS_TO_LEVEL": self.handle_set_clubs_to_level,
            "GET_NATIONAL_TEAMS": self.handle_get_national_teams,
            "GET_NATIONAL_TEAM": self.handle_get_national_team,
            "ADD_NATIONAL_TEAM": self.handle_add_national_team,
            "UPDATE_NATIONAL_TEAM": self.handle_update_national_team,
            "DELETE_NATIONAL_TEAM": self.handle_delete_national_team,
            "GET_MATCHES": self.handle_get_matches,
            "GET_MATCH": self.handle_get_match,
            "ADD_MATCH": self.handle_add_match,
            "UPDATE_MATCH": self.handle_update_match,
            "DELETE_MATCH": self.handle_delete_match,
            "EXECUTE_PROMOTION_RELEGATION": self.handle_execute_promotion_relegation
        }
        
        if command in handlers:
            return await handlers[command](data, session_id)
        
        return {
            "status": "error",
            "message": "Invalid command",
            "command": command
        }
    
    # 命令处理函数
    async def handle_login(self, data):
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return {
                "status": "error",
                "message": "Missing username or password",
                "command": "LOGIN"
            }
        
        login_result = await self.auth_service.login(username, password)
        if login_result:
            return {
                "status": "success",
                "data": login_result,
                "message": "Login successful",
                "command": "LOGIN",
                "session_id": login_result["session_id"]
            }
        
        return {
            "status": "error",
            "message": "Invalid username or password",
            "command": "LOGIN"
        }
    
    async def handle_logout(self, data, session_id):
        logout_result = await self.auth_service.logout(session_id)
        if logout_result:
            return {
                "status": "success",
                "message": "Logout successful",
                "command": "LOGOUT"
            }
        return {
            "status": "error",
            "message": "Logout failed",
            "command": "LOGOUT"
        }
    
    async def handle_get_user_info(self, data, session_id):
        user_info = await self.auth_service.get_user_info(session_id)
        if user_info:
            return {
                "status": "success",
                "data": user_info,
                "message": "User info retrieved",
                "command": "GET_USER_INFO"
            }
        return {
            "status": "error",
            "message": "User not found",
            "command": "GET_USER_INFO"
        }
    
    def handle_ping(self):
        return {
            "status": "success",
            "message": "Pong",
            "command": "PING"
        }
    
    # 球员管理命令
    async def handle_get_players(self, data, session_id):
        players = await self.player_service.get_all_players()
        return {
            "status": "success",
            "data": players,
            "message": "Players retrieved",
            "command": "GET_PLAYERS"
        }
    
    async def handle_get_player(self, data, session_id):
        player_id = data.get("id")
        if not player_id:
            return {
                "status": "error",
                "message": "Missing player ID",
                "command": "GET_PLAYER"
            }
        
        player = await self.player_service.get_player_by_id(player_id)
        if player:
            return {
                "status": "success",
                "data": player,
                "message": "Player retrieved",
                "command": "GET_PLAYER"
            }
        return {
            "status": "error",
            "message": "Player not found",
            "command": "GET_PLAYER"
        }
    
    async def handle_add_player(self, data, session_id):
        name = data.get("name")
        position = data.get("position")
        qq = data.get("qq")
        game_id = data.get("game_id")
        club = data.get("club")
        national_team = data.get("national_team")
        
        if not name or not position or not qq or not game_id:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_PLAYER"
            }
        
        player = await self.player_service.create_player(name, position, qq, game_id, club, national_team)
        return {
            "status": "success",
            "data": player,
            "message": "Player created",
            "command": "ADD_PLAYER"
        }
    
    async def handle_update_player(self, data, session_id):
        player_id = data.get("id")
        updates = data.get("updates")
        
        if not player_id or not updates:
            return {
                "status": "error",
                "message": "Missing player ID or updates",
                "command": "UPDATE_PLAYER"
            }
        
        player = await self.player_service.update_player(player_id, updates)
        if player:
            return {
                "status": "success",
                "data": player,
                "message": "Player updated",
                "command": "UPDATE_PLAYER"
            }
        return {
            "status": "error",
            "message": "Player not found",
            "command": "UPDATE_PLAYER"
        }
    
    async def handle_delete_player(self, data, session_id):
        player_id = data.get("id")
        if not player_id:
            return {
                "status": "error",
                "message": "Missing player ID",
                "command": "DELETE_PLAYER"
            }
        
        deleted = await self.player_service.delete_player(player_id)
        if deleted:
            return {
                "status": "success",
                "message": "Player deleted",
                "command": "DELETE_PLAYER"
            }
        return {
            "status": "error",
            "message": "Player not found",
            "command": "DELETE_PLAYER"
        }
    
    # 俱乐部管理命令
    async def handle_get_clubs(self, data, session_id):
        clubs = await self.club_service.get_all_clubs()
        return {
            "status": "success",
            "data": clubs,
            "message": "Clubs retrieved",
            "command": "GET_CLUBS"
        }
    
    async def handle_get_club(self, data, session_id):
        club_id = data.get("id")
        if not club_id:
            return {
                "status": "error",
                "message": "Missing club ID",
                "command": "GET_CLUB"
            }
        
        club = await self.club_service.get_club_by_id(club_id)
        if club:
            return {
                "status": "success",
                "data": club,
                "message": "Club retrieved",
                "command": "GET_CLUB"
            }
        return {
            "status": "error",
            "message": "Club not found",
            "command": "GET_CLUB"
        }
    
    async def handle_add_club(self, data, session_id):
        name = data.get("name")
        league = data.get("league")
        league_level = data.get("league_level")
        home_stadium = data.get("home_stadium")
        coach = data.get("coach")
        
        if not name or not league or not league_level or not home_stadium or not coach:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_CLUB"
            }
        
        club = await self.club_service.create_club(name, league, league_level, home_stadium, coach)
        return {
            "status": "success",
            "data": club,
            "message": "Club created",
            "command": "ADD_CLUB"
        }
    
    async def handle_update_club(self, data, session_id):
        club_id = data.get("id")
        updates = data.get("updates")
        
        if not club_id or not updates:
            return {
                "status": "error",
                "message": "Missing club ID or updates",
                "command": "UPDATE_CLUB"
            }
        
        club = await self.club_service.update_club(club_id, updates)
        if club:
            return {
                "status": "success",
                "data": club,
                "message": "Club updated",
                "command": "UPDATE_CLUB"
            }
        return {
            "status": "error",
            "message": "Club not found",
            "command": "UPDATE_CLUB"
        }
    
    async def handle_delete_club(self, data, session_id):
        club_id = data.get("id")
        if not club_id:
            return {
                "status": "error",
                "message": "Missing club ID",
                "command": "DELETE_CLUB"
            }
        
        deleted = await self.club_service.delete_club(club_id)
        if deleted:
            return {
                "status": "success",
                "message": "Club deleted",
                "command": "DELETE_CLUB"
            }
        return {
            "status": "error",
            "message": "Club not found",
            "command": "DELETE_CLUB"
        }
    
    # 联赛管理命令
    async def handle_get_leagues(self, data, session_id):
        leagues = await self.league_service.get_all_leagues()
        return {
            "status": "success",
            "data": leagues,
            "message": "Leagues retrieved",
            "command": "GET_LEAGUES"
        }
    
    async def handle_get_league(self, data, session_id):
        league_id = data.get("id")
        if not league_id:
            return {
                "status": "error",
                "message": "Missing league ID",
                "command": "GET_LEAGUE"
            }
        
        league = await self.league_service.get_league_by_id(league_id)
        if league:
            return {
                "status": "success",
                "data": league,
                "message": "League retrieved",
                "command": "GET_LEAGUE"
            }
        return {
            "status": "error",
            "message": "League not found",
            "command": "GET_LEAGUE"
        }
    
    async def handle_add_league(self, data, session_id):
        name = data.get("name")
        season = data.get("season")
        promotion_relegation_rules = data.get("promotion_relegation_rules")
        
        if not name or not season:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_LEAGUE"
            }
        
        league = await self.league_service.create_league(name, season, promotion_relegation_rules)
        return {
            "status": "success",
            "data": league,
            "message": "League created",
            "command": "ADD_LEAGUE"
        }
    
    async def handle_update_league(self, data, session_id):
        league_id = data.get("id")
        updates = data.get("updates")
        
        if not league_id or not updates:
            return {
                "status": "error",
                "message": "Missing league ID or updates",
                "command": "UPDATE_LEAGUE"
            }
        
        league = await self.league_service.update_league(league_id, updates)
        if league:
            return {
                "status": "success",
                "data": league,
                "message": "League updated",
                "command": "UPDATE_LEAGUE"
            }
        return {
            "status": "error",
            "message": "League not found",
            "command": "UPDATE_LEAGUE"
        }
    
    async def handle_delete_league(self, data, session_id):
        league_id = data.get("id")
        if not league_id:
            return {
                "status": "error",
                "message": "Missing league ID",
                "command": "DELETE_LEAGUE"
            }
        
        deleted = await self.league_service.delete_league(league_id)
        if deleted:
            return {
                "status": "success",
                "message": "League deleted",
                "command": "DELETE_LEAGUE"
            }
        return {
            "status": "error",
            "message": "League not found",
            "command": "DELETE_LEAGUE"
        }
    
    # 联赛级别管理命令
    async def handle_get_league_levels(self, data, session_id):
        league_id = data.get("league_id")
        if league_id:
            league_levels = await self.league_service.get_league_levels(league_id)
        else:
            league_levels = await self.league_service.get_all_leagues()
        return {
            "status": "success",
            "data": league_levels,
            "message": "League levels retrieved",
            "command": "GET_LEAGUE_LEVELS"
        }
    
    async def handle_add_league_level(self, data, session_id):
        league_id = data.get("league_id")
        name = data.get("name")
        
        if not league_id or not name:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_LEAGUE_LEVEL"
            }
        
        league_level = await self.league_service.add_league_level(league_id, name)
        return {
            "status": "success",
            "data": league_level,
            "message": "League level added",
            "command": "ADD_LEAGUE_LEVEL"
        }
    
    async def handle_update_league_level(self, data, session_id):
        level_id = data.get("id")
        updates = data.get("updates")
        
        if not level_id or not updates:
            return {
                "status": "error",
                "message": "Missing level ID or updates",
                "command": "UPDATE_LEAGUE_LEVEL"
            }
        
        league_level = await self.league_service.update_league_level(level_id, updates)
        if league_level:
            return {
                "status": "success",
                "data": league_level,
                "message": "League level updated",
                "command": "UPDATE_LEAGUE_LEVEL"
            }
        return {
            "status": "error",
            "message": "League level not found",
            "command": "UPDATE_LEAGUE_LEVEL"
        }
    
    async def handle_delete_league_level(self, data, session_id):
        level_id = data.get("id")
        if not level_id:
            return {
                "status": "error",
                "message": "Missing level ID",
                "command": "DELETE_LEAGUE_LEVEL"
            }
        
        deleted = await self.league_service.delete_league_level(level_id)
        if deleted:
            return {
                "status": "success",
                "message": "League level deleted",
                "command": "DELETE_LEAGUE_LEVEL"
            }
        return {
            "status": "error",
            "message": "League level not found",
            "command": "DELETE_LEAGUE_LEVEL"
        }
    
    async def handle_set_clubs_to_level(self, data, session_id):
        level_id = data.get("level_id")
        club_ids = data.get("club_ids")
        
        if not level_id or not club_ids:
            return {
                "status": "error",
                "message": "Missing level ID or club IDs",
                "command": "SET_CLUBS_TO_LEVEL"
            }
        
        updated_level = await self.league_service.set_clubs_to_level(level_id, club_ids)
        if updated_level:
            return {
                "status": "success",
                "data": updated_level,
                "message": "Clubs set to league level",
                "command": "SET_CLUBS_TO_LEVEL"
            }
        return {
            "status": "error",
            "message": "League level not found",
            "command": "SET_CLUBS_TO_LEVEL"
        }
    
    # 国家队管理命令
    async def handle_get_national_teams(self, data, session_id):
        national_teams = await self.national_team_service.get_all_national_teams()
        return {
            "status": "success",
            "data": national_teams,
            "message": "National teams retrieved",
            "command": "GET_NATIONAL_TEAMS"
        }
    
    async def handle_get_national_team(self, data, session_id):
        team_id = data.get("id")
        if not team_id:
            return {
                "status": "error",
                "message": "Missing team ID",
                "command": "GET_NATIONAL_TEAM"
            }
        
        national_team = await self.national_team_service.get_national_team_by_id(team_id)
        if national_team:
            return {
                "status": "success",
                "data": national_team,
                "message": "National team retrieved",
                "command": "GET_NATIONAL_TEAM"
            }
        return {
            "status": "error",
            "message": "National team not found",
            "command": "GET_NATIONAL_TEAM"
        }
    
    async def handle_add_national_team(self, data, session_id):
        country_name = data.get("country_name")
        coach = data.get("coach")
        
        if not country_name or not coach:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_NATIONAL_TEAM"
            }
        
        national_team = await self.national_team_service.create_national_team(country_name, coach)
        return {
            "status": "success",
            "data": national_team,
            "message": "National team created",
            "command": "ADD_NATIONAL_TEAM"
        }
    
    async def handle_update_national_team(self, data, session_id):
        team_id = data.get("id")
        updates = data.get("updates")
        
        if not team_id or not updates:
            return {
                "status": "error",
                "message": "Missing team ID or updates",
                "command": "UPDATE_NATIONAL_TEAM"
            }
        
        national_team = await self.national_team_service.update_national_team(team_id, updates)
        if national_team:
            return {
                "status": "success",
                "data": national_team,
                "message": "National team updated",
                "command": "UPDATE_NATIONAL_TEAM"
            }
        return {
            "status": "error",
            "message": "National team not found",
            "command": "UPDATE_NATIONAL_TEAM"
        }
    
    async def handle_delete_national_team(self, data, session_id):
        team_id = data.get("id")
        if not team_id:
            return {
                "status": "error",
                "message": "Missing team ID",
                "command": "DELETE_NATIONAL_TEAM"
            }
        
        deleted = await self.national_team_service.delete_national_team(team_id)
        if deleted:
            return {
                "status": "success",
                "message": "National team deleted",
                "command": "DELETE_NATIONAL_TEAM"
            }
        return {
            "status": "error",
            "message": "National team not found",
            "command": "DELETE_NATIONAL_TEAM"
        }
    
    # 比赛管理命令
    async def handle_get_matches(self, data, session_id):
        matches = await self.match_service.get_all_matches()
        return {
            "status": "success",
            "data": matches,
            "message": "Matches retrieved",
            "command": "GET_MATCHES"
        }
    
    async def handle_get_match(self, data, session_id):
        match_id = data.get("id")
        if not match_id:
            return {
                "status": "error",
                "message": "Missing match ID",
                "command": "GET_MATCH"
            }
        
        match = await self.match_service.get_match_by_id(match_id)
        if match:
            return {
                "status": "success",
                "data": match,
                "message": "Match retrieved",
                "command": "GET_MATCH"
            }
        return {
            "status": "error",
            "message": "Match not found",
            "command": "GET_MATCH"
        }
    
    async def handle_add_match(self, data, session_id):
        home_team = data.get("home_team")
        away_team = data.get("away_team")
        match_time = data.get("match_time")
        location = data.get("location")
        match_type = data.get("match_type", "league")
        
        if not home_team or not away_team or not match_time or not location:
            return {
                "status": "error",
                "message": "Missing required fields",
                "command": "ADD_MATCH"
            }
        
        match = await self.match_service.create_match(home_team, away_team, match_time, location, match_type)
        return {
            "status": "success",
            "data": match,
            "message": "Match created",
            "command": "ADD_MATCH"
        }
    
    async def handle_update_match(self, data, session_id):
        match_id = data.get("id")
        updates = data.get("updates")
        
        if not match_id or not updates:
            return {
                "status": "error",
                "message": "Missing match ID or updates",
                "command": "UPDATE_MATCH"
            }
        
        match = await self.match_service.update_match(match_id, updates)
        if match:
            return {
                "status": "success",
                "data": match,
                "message": "Match updated",
                "command": "UPDATE_MATCH"
            }
        return {
            "status": "error",
            "message": "Match not found",
            "command": "UPDATE_MATCH"
        }
    
    async def handle_delete_match(self, data, session_id):
        match_id = data.get("id")
        if not match_id:
            return {
                "status": "error",
                "message": "Missing match ID",
                "command": "DELETE_MATCH"
            }
        
        deleted = await self.match_service.delete_match(match_id)
        if deleted:
            return {
                "status": "success",
                "message": "Match deleted",
                "command": "DELETE_MATCH"
            }
        return {
            "status": "error",
            "message": "Match not found",
            "command": "DELETE_MATCH"
        }
    
    # 升降级命令
    async def handle_execute_promotion_relegation(self, data, session_id):
        league_id = data.get("league_id")
        if not league_id:
            return {
                "status": "error",
                "message": "Missing league ID",
                "command": "EXECUTE_PROMOTION_RELEGATION"
            }
        
        result = await self.promotion_service.execute_promotion_relegation(league_id)
        if result:
            return {
                "status": "success",
                "data": result,
                "message": "Promotion/relegation executed",
                "command": "EXECUTE_PROMOTION_RELEGATION"
            }
        return {
            "status": "error",
            "message": "Failed to execute promotion/relegation",
            "command": "EXECUTE_PROMOTION_RELEGATION"
        }