from urllib.parse import parse_qs, parse_qsl

from requests.models import parse_url
from sources.basesource import basesource


class DR(basesource):
    import json
    import requests

    from bs4 import BeautifulSoup as html
    from urllib.parse import parse_qs, urlparse

    from constants import misc, url as URL

    def GetNext(self, n: int, query: str):
        if n == 0:  # Channels
            return self.GetChannels()
        elif n == 1:  # Shows
            return self.GetShows(query)
        elif n == 2:  # Episodes
            return self.GetEpisodes(query)
        elif n == 3:  # Sources
            return self.GetSources(query)
        else:  # Playdata
            return self.GetPlayData(query)

    def GetChannels(self):

        def mapItems(node):
            try:
                return {
                    "Name": node.string,
                    "Link": f"""dr/1?q={self.__linkToQs(str(node["href"])[:-1])}""",
                    "ImgSrc": ""  # node.a.img["src"].replace("about:///", "")
                }
            except:
                pass

        def unwanted(item):
            return not set(["webseries", "urdu", "pakistani", "mtv", "other", "[v]", "mtv", "jalsha", "bangla", "telugu", "tamil", "vijay"]).intersection(item["Name"].lower().split())

        # First list
        rawHtml = self.requests.get(self.URL.DR + self.URL.DR1).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select(".titleline a")

        channels = list(filter(unwanted, map(mapItems, nodes)))

        # Second list
        rawHtml = self.requests.get(self.URL.DR + self.URL.DR2).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select(".titleline a")

        channels = channels + list(filter(unwanted, map(mapItems, nodes)))

        return {
            "Page": 1,
            "ItemsPerPage": len(channels),
            "TotalItems": len(channels),
            "Items": channels
        }

    def GetShows(self, query: str = ""):
        # print(query)
        rawHtml = self.requests.get(self.__qsToPath(query)).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select(".titleline a")

        def mapItems(node):
            try:
                return {
                    "Name": node.string,
                    "Link": f"""dr/2?q={self.__linkToQs(node["href"])}""",
                    "ImgSrc": ""  # node.a.img["src"].replace("about:///", "")
                }
            except:
                pass

        shows = list(map(mapItems, nodes))

        return {
            "Page": 1,
            "ItemsPerPage": len(shows),
            "TotalItems": len(shows),
            "Items": shows
        }

    def GetEpisodes(self, query: str = ""):
        rawHtml = self.requests.get(self.__qsToPath(query)).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select(".title")

        def mapItems(node):
            try:
                return {
                    "Name": node.text,
                    "Link": f"""dr/3?q={self.__linkToQs(node["href"])}""",
                    "ImgSrc": ""  # node.a.img["src"].replace("about:///", "")
                }
            except:
                pass

        episodes = list(map(mapItems, nodes))

        return {
            "Page": 1,
            "ItemsPerPage": len(episodes),
            "TotalItems": len(episodes),
            "Items": episodes
        }

    def GetSources(self, query: str = ""):
        rawHtml = self.requests.get(self.__qsToPath(query)).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select(".postcontent a")

        def mapItems(node):
            try:
                # if not any(src in node["href"] for src in ["hqq", "vkprime", "vidoza"]):
                if "hqq" not in node["href"]:
                    return {
                        "Name": node.text,
                        "Link": f"""dr/4?q={self.__linkToQs(node["href"])}|view""",
                        "ImgSrc": ""  # node.a.img["src"].replace("about:///", "")
                    }
            except:
                pass

        links = list(filter(lambda x: x != None, map(mapItems, nodes)))

        return {
            "Page": 1,
            "ItemsPerPage": len(links),
            "TotalItems": len(links),
            "Items": links
        }

    def GetPlayData(self, query: str = ""):
        query = query.replace("|view","")
        
        import re
        rawHtml = self.requests.get(query).text

        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select("iframe")

        if len(nodes) > 0 and "embed" in nodes[0]["src"]:
            return {
                "Name": "",
                "ImgSrc": "",
                "Links": [{
                    "Type": "browser",
                    "Link": nodes[0]["src"]
                }],
            }
        else:
            url = re.search(
                "(?P<url>(http|https)?://[^\s]+)\">", rawHtml).group("url")
       
            rawHtml = self.requests.get(url).text

            ohtml = self.html(rawHtml, 'lxml')
            nodes = ohtml.select("iframe")
            # print(nodes)
            if len(nodes) > 0:
                return {
                    "Name": "",
                    "ImgSrc": "",
                    "Links": [{
                        "Type": "browser",
                        "Link": nodes[0]["src"]
                    }],
                }

        return {
            "Name": "",
            "ImgSrc": "",
            "Links": [],
        }

    # def GetPlayData(self, query: str = ""):
        # import re
        # rawHtml = self.requests.get(query).text
        # url = re.search(
        #     "(?P<url>(http|https)?://[^\s]+)\">", rawHtml).group("url")

        # rawHtml = self.requests.get(url).text

        # ohtml = self.html(rawHtml, 'lxml')
        # nodes = ohtml.select("iframe")
        # if len(nodes) > 0:
        #     url = nodes[0]["src"]
        #     print(url)
        #     rawHtml = self.requests.get(url).text

        #     #vkprime, videowatch
        #     if any(src in url for src in ["vkprime", "watchvideo"]):
        #         test = re.search("\|{4}(?P<test>.+)\|defaults", rawHtml).group("test")
        #         meta = test.split("|")

        #         if "mp4" in test:
        #             return {
        #                 "Name": "",
        #                 "ImgSrc": "",
        #                 "Links": [
        #                     {
        #                         "Type": "video/mp4",
        #                         "Link": f"{meta[0]}://{meta[24]}.{meta[23]}.{meta[3]}/{meta[150]}/v.mp4"
        #                     },
        #                 ],
        #             }
        #         elif "m3u8" in test:
        #             return {
        #                 "Name": "",
        #                 "ImgSrc": "",
        #                 "Links": [
        #                     {
        #                         "Type": "application/x-mpegURL",
        #                         "Link": f"{meta[0]}://{meta[59]}.{meta[58]}.{meta[7]}/{meta[157]}/,{meta[156]},.{meta[155]}/{meta[154]}.{meta[153]}"
        #                     },
        #                 ],
        #             }
        #     # vidoza
        #     else:
        #         ohtml = self.html(rawHtml, 'lxml')
        #         nodes = ohtml.select("video source")
        #         return {
        #             "Name": "",
        #             "ImgSrc": "",
        #             "Links": [
        #                 {
        #                     "Type": nodes[0]["type"],
        #                     "Link": nodes[0]["src"]
        #                 },
        #             ],
        #         }

        # return {
        #     "Name": "",
        #     "ImgSrc": "",
        #     "Links": [],
        # }

    def __linkToQs(self, link):
        if '?s=' in link:
            parts = link.split("?")
            path = parts[0].replace(self.URL.DR, "")
            return f"{path}"
        else:
            return link

    def __qsToPath(self, link):
        return f"{self.URL.DR}{link}"
