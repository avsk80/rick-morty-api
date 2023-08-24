from dataclasses import dataclass

## data classes that hold schema info

@dataclass
class Location:
    id: int
    name: str
    type: str
    # residents: list
    url: str
    created: str
    
@dataclass
class Character:
    id: int
    name: str
    status: str
    species: str
    url: str
    created: str
    
@dataclass
class Episode:
    id: int
    name: str
    air_date: str
    episode: str
    url: str
    created: str
    
@dataclass
class Info:
    count: int
    pages: int
    next: str
    prev: str