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
            "Name": "DesiTvFlix",
            "Link":"df/&p=1", 
            "ImgSrc":"http://desitvflix.com/images/namelogo.png"
        },
        {
            "Name": "Zee5",
            "Link":"z5", 
            "ImgSrc": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Zee5-official-logo.jpeg/600px-Zee5-official-logo.jpeg"
        },
        {
            "Name": "Viki",
            "Link": "vk", 
            "ImgSrc": "https://images-eu.ssl-images-amazon.com/images/I/41fLQDXrS3L.png"
        }
    ]
}