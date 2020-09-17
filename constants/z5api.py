
REGIONAL_DETAILS = "https://b2bapi.zee5.com/front/countrylist.php?lang=en&ccode=AU"
AKAMAI_URL = "https://zee5vodnd.akamaized.net"
VIDEO_TOKEN = "https://useraction.zee5.com/tokennd/"
PLATFORM_TOKEN = "https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app"

def ApiList(query:str, type:str = "tvshow"):
    return f"https://catalogapi.zee5.com/v1/{type}?asset_subtype={type}&sort_by_field=release_date&sort_order=DESC&genres=Action,Animation,Comedy,Cookery,Crime,Devotional,Docudrama,Drama,Entertainment,Fantasy,Horror,Infotainment,Kids,Lifestyle,Mystery,News,Reality,Romance,Sci-Fi%20%26%20Fantasy,Thriller,Wellness&country=AU&translation=en&{query}"

def ApiShowDetails(showId:str, type:str = "tvshow"):
    return f"https://catalogapi.zee5.com/v1/{type}/{showId}"

def ApiEpisodesForSeason(seasonId:str, page:int = 1, limit:int = 9):
    return f"https://gwapi.zee5.com/content/tvshow/?season_id={seasonId}&type=episode&page={page}&limit={limit}"

def ApiEpisodesForShow(showId:str, page:int=1, limit:int=9):
    return f"https://gwapi.zee5.com/content/tvshow/{showId}?translation=en&country=AU&page={page}&limit={limit}"