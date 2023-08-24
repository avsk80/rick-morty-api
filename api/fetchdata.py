import sys
print(sys.path)

import requests
from api.schema import Location, Info, Character, Episode

## Class to create API session
class APISession:
    def __init__(self, base_url, logger) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logger
        
    def get_base_url(self):
        return self.base_url
        
    def get(self, endpoint=None, url=None, params=None):
        '''
        returns response JSON for an endpoint
        '''
        if url == None:
            response = self.session.get(url = (self.base_url + endpoint), params=params)
        else:
            response = self.session.get(url = url, params=params)
        response.raise_for_status()
        return response.json()


## Class to fetch data and handle pagination
class APIFetcher:
    def __init__(self, session, logger) -> None:
        self.session = session
        self.logger = logger
        
    def fetch_locations(self):
        '''
        returns a list of final locations data after collecting location info from each page
        '''
        locations = []
        endpoint = "/location"
        url = self.session.get_base_url()
        url = url + endpoint
        self.logger.info(url) 
        
        while url:
            self.logger.info(url)
            data = self.session.get(url = url)
            info = Info(**data['info'])
 
            for j in data['results']:
                loc_obj = Location(
                    id=j['id'],
                    name= j['name'],
                    type= j['type'],
                    # residents= j['residents'],
                    url= j['url'],
                    created= j['created']
                )
                locations.append(loc_obj.__dict__)
            url = info.next
        return locations
    
    def fetch_characters(self):
        '''
        returns a list of final characters data after collecting characters info from each page
        '''
        characters = []
        endpoint = "/character"
        url = self.session.get_base_url()
        url = url + endpoint
        self.logger.info(url)
        while url:
            data = self.session.get(url=url)
            info = Info(**data['info'])
            
            for j in data['results']:
                self.logger.info(url)
                char_obj = Character(
                    id = j['id'],
                    name = j['name'],
                    status = j['status'],
                    species = j['species'],
                    url = j['url'],
                    created = j['created'] 
                )
                characters.append(char_obj.__dict__)
            url = info.next
        return characters
    
    def fetch_episodes(self):
        '''
        returns a list of final episodes data after collecting episodes info from each page
        '''
        episodes = []
        endpoint = "/episode"
        url = self.session.get_base_url()
        url = url + endpoint
        
        while url:
            self.logger.info(url)
            data = self.session.get(url= url)
            info_obj = Info(**data['info'])

            for j in data['results']:
                epi = Episode(
                    id = j['id'],
                    name = j['name'],
                    air_date = j['air_date'],
                    episode= j['episode'],
                    url= j['url'],
                    created= j['created']
                )
                episodes.append(epi.__dict__)
            url = info_obj.next
        
        return episodes
        
        