from sources.basesource import basesource

class Z5(basesource):
    import json
    import requests
    from urllib.parse import urlparse
    from urllib.parse import parse_qs

    from constants import z5api
    from constants import misc

    collectionId: str

    def __init__(self):
        rawJson = self.requests.get(self.z5api.REGIONAL_DETAILS)
        jsonData = rawJson.json()
        self.collectionId = jsonData[0]["collections"]["web_app"]["tvshows"]

    def GetRequestHeaders(self):
        rawJson = self.requests.get(self.z5api.PLATFORM_TOKEN)
        jsonData = rawJson.json()
        xAccessToken = jsonData["token"]

        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "Referer": "https://www.zee5.com",
            "Accept": "application/json, text/plain, */*",
            "X-ACCESS-TOKEN": xAccessToken
            # "Origin": "https://www.zee5.com",
            # "Accept": "*/*",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "en-US,en;q=0.9",
            # "Accept-Language": "en-US,en;q=0.9",
        }

    def GetChannels(self, query: str = ""):
        shows = [
            {
                "Name": "Marathi",
                "ImgSrc": "",
                "Link": "z5/s/l=mr&p=1"
            },
            {
                "Name": "Hindi",
                "ImgSrc": "",
                "Link": "z5/s/l=hi&p=1"
            },
            {
                "Name": "English",
                "ImgSrc": "",
                "Link": "z5/s/l=en&p=1"
            },
            {
                "Name": "Marathi Movies",
                "ImgSrc": "",
                "Link": "z5/s/l=mr&p=1&t=m"
            },
            {
                "Name": "Hindi Movies",
                "ImgSrc": "",
                "Link": "z5/s/l=hi&p=1&t=m"
            },
            {
                "Name": "English Movies",
                "ImgSrc": "",
                "Link": "z5/s/l=en&p=1&t=m"
            }
        ]

        return {
            "Page": 1,
            "ItemsPerPage": 1,
            "TotalItems": 1,
            "Items": shows
        }

    def GetShows(self, query:str = "l=mr&p=1"):
        qdict = dict(item.split("=") for item in query.split("&"))
        lang = qdict["l"]
        page = int(qdict["p"])
        ifMovie = query.find("&t=m") > -1
        type_ = "movie" if ifMovie else "tvshow"
        param = f"languages={lang}&page={page}&page_size={self.misc.PAGE_SIZE}"
        rawJson = self.requests.get(self.z5api.ApiList(param, type_))        
        jsonData = rawJson.json()

        def imgUrl(id:str, listImage:str):
            return "" if (not listImage or listImage.isspace()) else f"https://akamaividz1.zee5.com/resources/{id}/list/1170x658/{listImage}"

        def mapItems(item):
            try:
                return {
                    "Name": item["title"],
                    "Link": f"""z5/e/{item["id"]}&p=1{"&t=m" if ifMovie else ""}""",
                    "ImgSrc": imgUrl(item["id"], item["list_image"])
                }
            except:
                pass


        return {
            "Page": jsonData["page"],
            "ItemsPerPage": jsonData["page_size"],
            "TotalItems": jsonData["total"],
            "Items": list(map(mapItems, jsonData["items"]))
        }

    def GetEpisodes(self, query:str = "p=1"):
        qdict = dict(item.split("=") if item.find("=") > -1 else ["id", item] for item in query.split("&"))
        showId = qdict["id"]
        page = int(qdict["p"])
        ifMovie = query.find("&t=m") > -1
        type_ = "movie" if ifMovie else "tvshow"
        rawJson = self.requests.get(self.z5api.ApiShowDetails(showId,type_))
        jsonData = rawJson.json()
        title = jsonData["title"]

        if ifMovie:
            def imgUrl(id:str, listImage:str):
                return "" if (not listImage or listImage.isspace()) else f"https://akamaividz1.zee5.com/resources/{id}/list/1170x658/{listImage}"

            return {
                "Page": 1,
                "ItemsPerPage": self.misc.PAGE_SIZE,
                "TotalItems": 1,
                "Items": {
                    "Name":title,
                    "Link":f"z5/p/m|{showId}|1",
                    "ImgSrc":imgUrl(showId, jsonData["list_image"]),
                }
            }
        else:
            seasons = jsonData["seasons"]
            latestSeasonId = seasons[len(seasons)-1]["id"]
            
            rawJson = self.requests.get(self.z5api.ApiEpisodesForSeason(latestSeasonId, page),headers=self.GetRequestHeaders())
            jsonData = rawJson.json()

            from datetime import datetime as dt
            def mapItems(item):
                return {
                    "Name": f"""Ep {item["episode_number"]} - {dt.strptime(item["release_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y %b %d")}""",
                    "Link": f"""z5/p/{latestSeasonId}|{item["id"]}|{page}""",
                    "ImgSrc": item["image_url"]
                }
            
            try:
                return {
                    "Page": jsonData["page"],
                    "ItemsPerPage": self.misc.PAGE_SIZE,
                    "TotalItems": jsonData["total_episodes"],
                    "Items": list(map(mapItems, jsonData["episode"]))[:9]
                }      
            except:
                return {
                    "Page": 1,
                    "ItemsPerPage": self.misc.PAGE_SIZE,
                    "TotalItems": 1,
                    "Items": []
                }              

    def GetPlayData(self, query:str = ""):
        rawJson = self.requests.get(self.z5api.VIDEO_TOKEN)
        jsonData = rawJson.json()
        videoToken = jsonData["video_token"]

        arrQuery = query.split('|')
        seasonId = arrQuery[0]
        ifMovie = seasonId == "m"
        episodeId = arrQuery[1]
        page = int(arrQuery[2])

        playData = {}

        if ifMovie:
            rawJson = self.requests.get(self.z5api.ApiShowDetails(episodeId, "movie"))
            jsonData = rawJson.json()
            videoUrl = jsonData["video"]["hls_url"].replace("drm", "hls")
            playData = {
                "Name":jsonData["title"],
                "ImgSrc":jsonData["list_image"],
                "Links":[{
                    "Type": "application/x-mpegURL",
                    "Link": f"{self.z5api.AKAMAI_URL}{videoUrl}{videoToken}"
                }],
            }
        else:
            rawJson = self.requests.get(self.z5api.ApiEpisodesForSeason(seasonId, page))
            jsonData = rawJson.json()

            episode = next((x for x in jsonData["episode"] if x["id"]==episodeId), None) #FirstOrDefault

            episodeUrl = episode["video_details"]["hls_url"].replace("drm", "hls")

            playData = {
                "Name":episode["title"],
                "ImgSrc":episode["image_url"],
                "Links":[{
                    "Type": "application/x-mpegURL",
                    "Link": f"{self.z5api.AKAMAI_URL}{episodeUrl}{videoToken}"
                }],
            }

        return playData

    def GetSource(self, query:str = ""):
        return {
            "Page": 0,
            "ItemsPerPage": 0,
            "TotalItems": 0,
            "Items": [{
                "Name":"Not Applicable"
            }]
        }