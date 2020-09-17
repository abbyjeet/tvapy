# from constants import *
from constants import misc, url as URL

SECRET = "bcb959661b3be4613c1d380b3c29981e8b1ed868762af37d8201f4f9ff73"
APPID = "100005a"
KEY = "MM_d*yP@`&1@]@!AVrXf_o-HVEnoTnm$O-ti4[G~$JDI/Dc-&piU&z&5.;:}95=Iad"
USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" #Not used

def ApiGetSection(url:str, query:str):
    getQuery = f"{URL.VK}/v4/{url}?app={APPID}&t={misc.CURRENT_TIME_STAMP()}&sig={SECRET}"

    if query:
        getQuery += f"&{query}"

    return getQuery

def ApiListShows(query:str):
    return ApiGetSection("series.json", query)

def ApiEpisodesForSeason(seriesid:str, query:str):
    return ApiGetSection(f"series/{seriesid}/episodes.json", query)

def ApiEpisodeById(episodeId:str):
    timestamp = str(misc.CURRENT_TIME_STAMP())[0:10]
    rawtxt = f"/v5/videos/{episodeId}/streams.json?app={APPID}&t={timestamp}"
    hashed = HashHmacSHA1(rawtxt, KEY)
    return f"{URL.VK}{rawtxt}&sig={hashed}"

def ApiEpisodeSubtitleById(episodeId:str):
    timestamp = str(misc.CURRENT_TIME_STAMP())[0:10]
    rawtxt = f"/v4/videos/{episodeId}/subtitles/en.srt?app={APPID}&t={timestamp}"
    hashed = HashHmacSHA1(rawtxt, KEY)
    return f"{URL.VK}{rawtxt}&sig={hashed}"

def HashHmacSHA1(text:str, key:str):
    import hashlib
    import hmac

    bKey = bytes(key,'UTF-8')
    bText = bytes(text,'UTF-8')
    
    hasher = hmac.new(bKey,bText, hashlib.sha1)
    return hasher.hexdigest()