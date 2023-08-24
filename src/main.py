import sys
print(sys.path.append("d:\\MS\\projects\\utube\\Rick_Morty"))
import os
from api.fetchdata import APISession, APIFetcher
from db.storedata import DBManager
from configparser import ConfigParser
from utils.logger import Logger

if __name__ == "__main__":
    try:
        dir = os.path.join("D:\\", "MS", "projects", "utube", "Rick_Morty", "config", "config.ini")
        print(os.path.exists(dir))
        print(dir + " Config Path exists.....")
        
        config = ConfigParser()
        config.read(dir)
        ##read configs
        log_path = config.get("Logs", "log_file_path")
        base_url = config.get("API", "base_url")
        dbname = config.get("DB", "dbname")
        user = config.get("DB", "user")
        password = config.get("DB", "password")
        host = config.get("DB", "host")
        port = config.get("DB", "port")
        
        logger = Logger(log_file=log_path)
        logger.info("Starting the API fetch process ..........")
        # base_url = ""
        s = APISession(base_url=base_url, logger=logger)
        response = s.get(endpoint='/location')
    
        fetch = APIFetcher(session=s, logger=logger)
        locations = fetch.fetch_locations()

        db = DBManager(
            dbname = dbname,
            user = user,
            password = password,
            host= host, 
            port= port,
            logger=logger
        ) 

        location_spec = {
            'table' : 'location',
            'sql' :  "INSERT INTO test.location (id, name, type, url, created) VALUES (%s, %s, %s, %s, %s);",
            'data' : locations
        }
        db.insert_into(isql= location_spec['sql'], data=location_spec['data'], table=location_spec['table'])
        logger.info("Stored location API data to DB!!!!!!!!")
        
        episodes = fetch.fetch_episodes()   
        episode_spec = {
            'table' : 'episode',
            'sql' :  "INSERT INTO test.episode (id, name, air_date, episode, url, created) VALUES (%s, %s, %s, %s, %s, %s);",
            'data' : episodes
        }
        db.insert_into(isql= episode_spec['sql'], data=episode_spec['data'], table=episode_spec['table'])
        logger.info("Stored episode API data to DB!!!!!!!!")
    
        characters = fetch.fetch_characters()    
        character_spec = {
            'table' : 'character',
            'sql' :  "INSERT INTO test.character (id, name, status, species, url, created) VALUES (%s, %s, %s, %s, %s, %s);",
            'data' : characters
        }
        db.insert_into(isql= character_spec['sql'], data=character_spec['data'], table=character_spec['table'])
        logger.info("Stored character API data to DB!!!!!!!!")
        db.get_location_count()
        
    except Exception as e:
        logger.info("EXCEPTION OCCURED!!!!!!")
        logger.info(e)
    finally:
        db.cleanup()

    '''
    
    # print(len(response['results']))
    # print(s.get_base_url())
  
    # print(len(locations))
    # print(locations[0])
    # print(locations[-1])
    
    sql1 = "INSERT INTO test.location (id, name, type, url, created) VALUES (%s, %s, %s, %s, %s);"
    sql2 = "INSERT INTO test.location (id, name, air_date, episode, url, created) VALUES (%s, %s, %s, %s, %s, %s);"
    sql3 = "INSERT INTO test.location (id, name, status, species, url, created) VALUES (%s, %s, %s, %s, %s, %s);"
    
    # print(len(episodes))
    # print(episodes[0])
    # print(episodes[-1])
    
    # print(len(characters))
    # print(characters[0])
    # print(characters[-1])
    '''