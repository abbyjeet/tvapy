from sources.basesource import basesource

def source(key:str) -> basesource:
    from sources.z5 import Z5
    from sources.vk import VK
    from sources.df import DF
    switch = {
        "df":DF(), 
        "z5":Z5(), 
        "vk":VK()    
    }
    
    if any(key in k for k in switch.keys()):
        return switch[key]
    else:
        return basesource()
