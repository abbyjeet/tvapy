from sources.basesource import basesource


class DF(basesource):
    import json
    import requests

    from bs4 import BeautifulSoup as html
    from urllib.parse import urlparse
    from urllib.parse import parse_qs

    from constants import misc, url as URL

    def GetChannels(self, query: str = ""):
        rawHtml = self.requests.get(self.URL.DF).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select("#blogtile-left #blogs .tile")

        qdict = dict(item.split("=") if item.find("=") > -
                     1 else ["id", item] for item in query.split("&"))
        lang = qdict.get("l", "en")
        page = int(qdict.get("p", "1"))

        def mapItems(node):
            try:
                return {
                    "Name": node.text,
                    "Link": f"""df/s/{self.__linkToQs(node.a["href"])}""",
                    "ImgSrc": node.a.img["src"].replace("about:///", "")
                }
            except:
                pass

        channels = list(map(mapItems, reversed(nodes)))

        return {
            "Page": 1,
            "ItemsPerPage": len(channels),
            "TotalItems": len(channels),
            "Items": channels
        }

    def GetSource(self, query: str = ""):
        rawHtml = self.requests.get(self.__qsToPath(query)).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select("#blogtile-left #blogs .tile")

        def mapItems(node):
            try:
                return {
                    "Name": node.a.title,
                    "Link": f"""{self.__linkToQs(node.a["href"])}""",
                    "ImgSrc": ""
                }
            except:
                pass

        sources = list(map(mapItems, nodes))

        return {
            "Page": 1,
            "ItemsPerPage": len(sources),
            "TotalItems": len(sources),
            "Items": sources
        }

    def GetShows(self, query: str = ""):
        sources = self.GetSource(query)["Items"]

        source = next((x for x in sources if "Dates.php" in x["Link"]), None)

        if not source:
            source = next(
                (x for x in sources if x["Name"] == "Source 2" or "2" in x["Name"]), None)

            if not source:
                source = next(
                    (x for x in sources if x["Name"] == "Source 1" or "1" in x["Name"]), None)

                if not source:
                    source = next(
                        (x for x in sources if "Source (" in x["Name"]), None)

                    if not source:
                        source = next(
                            (x for x in sources if "tShows.php" in x["Link"]), None)

                        if not source:
                            source = sources[0]

                            if not source:
                                return {
                                    "Page": 1,
                                    "ItemsPerPage": self.misc.PAGE_SIZE,
                                    "TotalItems": 0,
                                    "Items": []
                                }

        rawHtml = self.requests.get(self.__qsToPath(source["Link"])).text
        ohtml = self.html(rawHtml, 'lxml')
        nodes = ohtml.select("#blogtile-left #blogs .tile")
         
        def mapItems(node):
            try:
                return {
                    "Name": node.a.title,
                    "Link": f"""df/e/{self.__linkToQs(node.a["href"])}""",
                    "ImgSrc": ""
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
        nodes = ohtml.select("#blogtile-left #blogs .tile")
         
        def mapItems(node):
            try:
                return {
                    "Name": node.a.title,
                    "Link": f"""df/p/{self.__linkToQs(node.a["href"])}""",
                    "ImgSrc": node.a.img["src"].replace("about:///", "")
                }
            except:
                pass

        episodes = list(map(mapItems, reversed(nodes)))

        return {
            "Page": 1,
            "ItemsPerPage": len(episodes),
            "TotalItems": len(episodes),
            "Items": episodes
        }

    def GetPlayData(self, query: str = ""):
        rawHtml = self.requests.get(self.__qsToPath(query)).text
        ohtml = self.html(rawHtml, 'lxml')
        title = ohtml.select("#content-title")
        node = ohtml.select("video")

        return {
            "Name": title.text.strip(),
            "ImgSrc": "",
            "Links": [                      
                {
                    "Type": node.source["type"],
                    "Link": node.source["source"]
                }
            ]
        }


    def __linkToQs(self, link):
        parts = link.split("?")
        path = parts[0]
        querystring = parts[1].replace("?", "").replace("&", "|")
        return f"{path};{querystring}"

    def __qsToPath(self, link):
        parts = link.split(";")
        path = parts[0]
        query = parts[1]
        return f"""{self.URL.DF}{path}?{query.replace("|","&")}"""
