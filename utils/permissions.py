class Permissions:
    ADMIN_PERMISSIONS = ["all"]
    USER_PERMISSIONS = [
        "get_players",
        "get_clubs",
        "get_leagues",
        "get_league_levels",
        "get_national_teams",
        "get_matches"
    ]
    
    @staticmethod
    def has_permission(user, permission):
        if not user:
            return False
        
        if "all" in user.permissions or user.role == "admin":
            return True
        
        return permission in user.permissions
    
    @staticmethod
    def can_perform_action(user, action):
        action_map = {
            "GET_PLAYERS": "get_players",
            "GET_PLAYER": "get_players",
            "ADD_PLAYER": "add_player",
            "UPDATE_PLAYER": "update_player",
            "DELETE_PLAYER": "delete_player",
            "GET_CLUBS": "get_clubs",
            "GET_CLUB": "get_clubs",
            "ADD_CLUB": "add_club",
            "UPDATE_CLUB": "update_club",
            "DELETE_CLUB": "delete_club",
            "GET_LEAGUES": "get_leagues",
            "GET_LEAGUE": "get_leagues",
            "ADD_LEAGUE": "add_league",
            "UPDATE_LEAGUE": "update_league",
            "DELETE_LEAGUE": "delete_league",
            "GET_LEAGUE_LEVELS": "get_league_levels",
            "ADD_LEAGUE_LEVEL": "add_league_level",
            "UPDATE_LEAGUE_LEVEL": "update_league_level",
            "DELETE_LEAGUE_LEVEL": "delete_league_level",
            "SET_CLUBS_TO_LEVEL": "set_clubs_to_level",
            "GET_NATIONAL_TEAMS": "get_national_teams",
            "GET_NATIONAL_TEAM": "get_national_teams",
            "ADD_NATIONAL_TEAM": "add_national_team",
            "UPDATE_NATIONAL_TEAM": "update_national_team",
            "DELETE_NATIONAL_TEAM": "delete_national_team",
            "GET_MATCHES": "get_matches",
            "GET_MATCH": "get_matches",
            "ADD_MATCH": "add_match",
            "UPDATE_MATCH": "update_match",
            "DELETE_MATCH": "delete_match",
            "EXECUTE_PROMOTION_RELEGATION": "execute_promotion_relegation"
        }
        
        permission = action_map.get(action)
        if not permission:
            return False
        
        return Permissions.has_permission(user, permission)