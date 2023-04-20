import psycopg2
import psycopg2.extras


class Database:
    def __init__ (self, HOST, DATABASE, USER, PASSWORD):
        print('Connecting to spotifydb...')
        self.HOST=HOST
        self.DATABASE=DATABASE
        self.USER=USER
        self.PASSWORD=PASSWORD
        
    def connect_db(self):
        self.conn = psycopg2.connect(
            host=self.HOST,
            database=self.DATABASE,
            user=self.USER,
            password=self.PASSWORD
        )
        return self.conn
        
    def criate_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()   
    
    def insert_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            self.conn.rollback()
            self.cur.close()
            return 1
        self.cur.close()
    
    def bulk_insert_db(self, sql, data):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        psycopg2.extras.execute_values(self.cur, sql, data)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def select_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.recset = self.cur.fetchall()
        self.records = []
        for rec in self.recset:
            self.records.append(rec)
        self.conn.close()
        return self.records
  

if __name__ == "__main__":
    HOST='localhost'
    DATABASE='spotifydb'
    USER='postgres'
    PASSWORD='postgres'
    db = Database(HOST, DATABASE, USER, PASSWORD)