import psycopg2 as pg2

"""conn = pg2.connect(
    dbname = "rickmorty",
    user = "postgres",
    password = '1234',
    host='127.0.0.1', 
    port= '5432'
)"""

class DBManager:
    def __init__(self, dbname, user, password, host, port, logger) -> None:
        self.conn = pg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host, 
            port = port
            )
        self.cursor = self.conn.cursor()
        self.logger = logger
        
    def truncate_table(self, table):
        if table == 'location':
            self.cursor.execute("TRUNCATE TABLE TEST.LOCATION")
        if table == 'episode':
            self.cursor.execute("TRUNCATE TABLE TEST.EPISODE")
        if table == 'character':
            self.cursor.execute("TRUNCATE TABLE TEST.CHARACTER")
            
        self.logger.info(f"TRUNCATED {table} !!!!!!!!!!!!!!!!!!!!!")
        # self.conn.commit()
        # self.cursor.close()
        # self.conn.close()
    
    def insert_into(self, isql, data, table):
        self.truncate_table(table=table)
        if table == 'location':
            for d in data:
                self.cursor.execute(isql, (d['id'], d['name'], d['type'], d['url'], d['created']))
        if table == 'episode':
            for d in data:
                self.cursor.execute(isql, (d['id'], d['name'], d['air_date'], d['episode'], d['url'], d['created']))
        if table == 'character':
            for d in data:
                self.cursor.execute(isql, (d['id'], d['name'], d['status'], d['species'], d['url'], d['created']))
           
        self.logger.info("Inserted!!!!!!!!!!")
        
    def get_location_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM TEST.LOCATION;")
        self.logger.info(self.cursor.fetchone()[0])
        
    def cleanup(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.logger.info("Closed all connections safely!!!!!!!!")
# cursor = conn.cursor()
# sql1 = "SELECT COUNT(*) FROM test.location"
# sql2 = "INSERT INTO test.location (id, name, type, url, created) VALUES (%s, %s, %s, %s, %s);"
