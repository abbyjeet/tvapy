from sources.basesource import basesource

class VK(basesource):
    import json
    import requests
    from urllib.parse import urlparse
    from urllib.parse import parse_qs

    from constants import vkapi
    from constants import misc

    def GetNext(self, n: int, query: str):
        if n==0: #Channels
            return self.GetLanguages()
        elif n==1: #Shows
            return self.GetShows(query)
        elif n==2: #Episodes
            return self.GetEpisodes(query)
        else: #Playdata
            return self.GetPlayData(query)

    def GetLanguages(self):
        shows = [
            {
                "Name":"Korean",
                "ImgSrc" :"https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/320px-Flag_of_South_Korea.svg.png",
                "Link" :"vk/1?l=kr&p=1"
            },
            {
                "Name":"Japanese",
                "ImgSrc" :"https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/Flag_of_Japan.svg/320px-Flag_of_Japan.svg.png",
                "Link" :"vk/1?l=jp&p=1"
            },
            {
                "Name":"Chinese",
                "ImgSrc" :"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/320px-Flag_of_the_People%27s_Republic_of_China.svg.png",
                "Link" :"vk/1?l=cn&p=1"
            },
            {
                "Name":"Taiwan",
                "ImgSrc" :"https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Flag_of_the_Republic_of_China.svg/320px-Flag_of_the_Republic_of_China.svg.png",
                "Link" :"vk/1?l=tw&p=1"
            },
            {
                "Name":"India",
                "ImgSrc" :"https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/320px-Flag_of_India.svg.png",
                "Link" :"vk/1?l=in&p=1"
            }
        ]

        return {
            "Page": 1,
            "ItemsPerPage": 1,
            "TotalItems": 1,
            "Items": shows
        }

    def GetShows(self, query: str = "l=kr&p=1"):
        qdict = dict(item.split("=") for item in query.split("&"))
        lang = qdict["l"]
        page = int(qdict["p"])
        param = f"origin_country={lang}&page={page}"

        getquery = f"{self.vkapi.ApiListShows(param)}&sort=views_recent&per_page={self.misc.PAGE_SIZE}&with_paging=true"
        rawJson = self.requests.get(getquery)        
        jsonData = rawJson.json()

        totalItems = jsonData["count"]

        def mapItems(item):
            try:
                return {
                    "Name": item["titles"]["en"],
                    "Link": f"""vk/2?{item["id"]}&p=1""",
                    "ImgSrc": item["images"]["poster"]["url"]
                }
            except:
                pass

        return {
            "Page": page,
            "ItemsPerPage": self.misc.PAGE_SIZE,
            "TotalItems": totalItems,
            "Items": list(map(mapItems, jsonData["response"]))
        }

    def GetEpisodes(self, query: str = "p=1"):
        qdict = dict(item.split("=") if item.find("=") > -1 else ["id", item] for item in query.split("&"))
        seriesId = qdict["id"]
        page = int(qdict["p"])

        getquery = self.vkapi.ApiEpisodesForSeason(seriesId, f"sort=number&direction=asc&page={page}&per_page={self.misc.PAGE_SIZE}&with_paging=true")
        rawJson = self.requests.get(getquery)        
        jsonData = rawJson.json()

        totalItems = jsonData["count"]

        def mapItems(item):
            return {
                "Name": f"""Episode {item["number"]}""",
                "Link": f"""vk/3?{item["id"]}|view""",
                "ImgSrc": item["images"]["poster"]["url"]
            }

        return {
            "Page": page,
            "ItemsPerPage": self.misc.PAGE_SIZE,
            "TotalItems": totalItems,
            "Items": list(map(mapItems, jsonData["response"]))
        }        

    def GetPlayData(self, query: str = ""):
        query = query.replace("|view","")     
        getquery = self.vkapi.ApiEpisodeById(query)

        # print(f"query ==> {getquery}")

        rawJson = self.requests.get(getquery)
        jsonData = rawJson.json()

        return {
                    "Name": "",
                    "ImgSrc": self.vkapi.ApiEpisodeSubtitleById(query),
                    "Links": [                      
                        {
                            "Type": "application/x-mpegURL",
                            "Link": jsonData["streams"]["480p"]["https"]["url"]
                        }, 
                        {
                            "Type": "application/x-mpegURL",
                            "Link": jsonData["streams"]["360p"]["https"]["url"]
                        },
                        {
                            "Type": "application/x-mpegURL",
                            "Link": jsonData["streams"]["240p"]["https"]["url"]
                        },
                        {
                            "Type": "application/dash+xml",
                            "Link": jsonData["streams"]["mpd"]["http"]["url"]
                        }
                    ],
                }
