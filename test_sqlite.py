import sqlite3
import pandas as pd
import re

class SQLIITE_service():
    def __init__(self,filename,df = None):
        self.filename = re.sub('-','_',filename)
        self.df = df
        self.directory = 'db_sqlite'
        self.mode = self.filename.split('_')[-1].split('.')[0]
        self.connect_link = "{}/{}.db".format(self.directory, self.mode)
        self.conn = sqlite3.connect(self.connect_link)
        self.link = self.filename.split('.')[0]
        
    def save_to_db(self):
        if self.df is None:
            return
        if "unnamed: 0" in self.df.columns.to_list():
            self.df = self.df.drop('unnamed: 0', 1)
        self.df.to_sql(self.filename.split('.')[0],con=self.conn, if_exists='replace')
        
    def query_some_record(self,num_records):
        cursor = self.conn.cursor()
        try:
            sqlite_select_query = """SELECT * FROM {}""".format(self.link)
            cursor.execute(sqlite_select_query)
            print("Reading ", num_records, " rows")
            records = cursor.fetchmany(num_records)
            
            cursor.close()
            return records
        except:
            print("NO TABLE EXIST")
    
    def drop_table(self):
        cursor = self.conn.cursor()
        sqlite_select_query = """DROP TABLE {}""".format(self.link)
        cursor.execute(sqlite_select_query) 
        print("DROP DONE!!")
        cursor.close()
    
    def convert_to_csv(self):
        df = pd.read_sql_query("SELECT * FROM {}".format(self.link), self.conn)
        if "Unnamed: 0" in df.columns.to_list():
            df = df.drop('Unnamed: 0', 1)
        if "index" in df.columns.to_list():
            df = df.drop('index', 1)
        print(df.head())
        return df
    
    # def list_of_table(self):
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     print(cursor.fetchall())
    #     cursor.close()
    
if __name__ == '__main__':
    filename = "myfile_20220522-004330_YOUTUBE.csv"
    test = SQLIITE_service(filename,pd.read_csv(filename))
    test.save_to_db()
    test.query_some_record(5)
    # test.convert_to_csv()
    test.list_of_table()
    # test.drop_table()