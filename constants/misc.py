from datetime import datetime

_epoch = datetime.utcfromtimestamp(0)

def CURRENT_TIME_STAMP():
    return int((datetime.now() - _epoch).total_seconds())

PAGE_SIZE = 9

Sources = {
    "Page": 1, 
    "ItemsPerPage": PAGE_SIZE,
    "TotalItems":3,
    "Items":[
        {
            "Name": "DesiRulez",
            "Link":"dr", 
            "ImgSrc":"http://www.desirulez.cc/images/styles/HighlightBlue/style/logo.png"
        },
        {
            "Name": "Zee5",
            "Link":"z5", 
            "ImgSrc": "https://cdn.dnaindia.com/sites/default/files/styles/full/public/2019/07/26/759898-zee5.png"
        },
        {
            "Name": "Viki",
            "Link": "vk", 
            "ImgSrc": "https://images-eu.ssl-images-amazon.com/images/I/41fLQDXrS3L.png"
        }
    ]
}