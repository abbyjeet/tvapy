from typing import List
from models.tvdataitem import TvDataItem

class TvData:
    Page:int
    ItemsPerPage:int
    TotalItems:int
    Items:List[TvDataItem]

    def __init__(self, Page:int, ItemsPerPage:int, TotalItems:int, Items:List[TvDataItem]):
        self.Page = Page
        self.ItemsPerPage = ItemsPerPage
        self.TotalItems = TotalItems
        self.Items = Items