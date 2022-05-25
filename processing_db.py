from test_sqlite import *
import streamlit as st
from test_pymongo import *
from CleanData.clean_csv import * 
from CleanData.MongoDB import *
import sys

def processing_sqlite_db():
    st.title("SQLITE PROCESSING")
    col1,col2,col3 = st.columns(3)
    
    db1 = "db_sqlite/TRAVELOKA.db"
    db2 = "db_sqlite/YOUTUBE.db"
    db3 = "db_sqlite/SHOPEE.db"
    
    #initialize connection
    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)
    conn3 = sqlite3.connect(db3)
    
    #initialize cursor
    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    cursor3 = conn3.cursor()
    
    cursor1.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor3.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    col1.write("TRAVELOKA")
    col1.write(cursor1.fetchall())
        
    col2.markdown("YOUTUBE")
    col2.write(cursor2.fetchall())
    
    col3.markdown("SHOPEE")
    col3.write(cursor3.fetchall())
    
    #cursor dictionary
    dict_cursor = {"TRAVELOKA" : cursor1,
                   "YOUTUBE" : cursor2,
                   "SHOPEE" : cursor3}
    
    name_db = st.selectbox("-------------------INPUT DBNAME-------------------",('TRAVELOKA','SHOPEE','YOUTUBE'))
    name = st.text_input("-------------------INPUT FILENAME-------------------")
    choice = st.selectbox('--------SAVE MONGODB(Y/N)--------',('Y','N'))
    choice1 = st.selectbox('--------SAVE SQLITE(Y/N)--------',('Y','N'))
    
    if st.button("PROCESSING"):
        col1,col2 = st.columns(2)
        cursor = dict_cursor[name_db]
        if name[0] == "\"":
            name = name[1:-1]
        name = name + ".csv"
        test = SQLIITE_service(name)
        col1.write("ONE QUERY EXAMPLE")
        col1.write(test.query_some_record(1))
        
        df = test.convert_to_csv()
        col1.write("DATA CRAWL OVERVIEW")
        col1.write(df.head(6))
        
        cleanCsvModule = CLEAN_CSV(name,df)
        cleanCsvModule.end_to_end_process_yt()
        test = cleanCsvModule.get_clean_data()
        download,extension = FileDownloader(test.to_csv(),col1,name,file_ext='csv').download()
        file_details = {"FILENAME":download,"FILETYPE":"text/string","FILESIZE":sys.getsizeof(test), "NUM_COL": len(test.columns.to_list()),"NUM_ROW":len(test)}
        col1.write(file_details)
        col1.write("DATA OVERVIEW")
        col1.dataframe(test.head(6))
        
        if choice == 'Y':
            time.sleep(3)
            connect_address = 'mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
            createDB = MongoDB(connect_address,extension)
            createDB.createDb(test,download)
            col2.success("===Upload Success!!!===")
            col2.write("EXAMPLE")
            col2.write(createDB.query_one_collection(download))
        if choice1 == 'Y':
            time.sleep(2)
            test1 = SQLIITE_service(download,test)
            test1.save_to_db()
            col2.write("SQLITE QUERY")
            col2.write(test1.query_some_record(2))
    
def collect_sqlite():
    st.title("SQLITE PROCESSING")
    col1,col2,col3 = st.columns(3)
    
    db1 = "db_sqlite/TRAVELOKA.db"
    db2 = "db_sqlite/YOUTUBE.db"
    db3 = "db_sqlite/SHOPEE.db"
    
    #initialize connection
    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)
    conn3 = sqlite3.connect(db3)
    
    #initialize cursor
    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    cursor3 = conn3.cursor()
    
    cursor1.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor3.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    col1.write("TRAVELOKA")
    col1.write(cursor1.fetchall())
        
    col2.markdown("YOUTUBE")
    col2.write(cursor2.fetchall())
    
    col3.markdown("SHOPEE")
    col3.write(cursor3.fetchall())
    
    #cursor dictionary
    dict_cursor = {"TRAVELOKA" : cursor1,
                   "YOUTUBE" : cursor2,
                   "SHOPEE" : cursor3}
    
    name_db = st.selectbox("-------------------INPUT DBNAME-------------------",('TRAVELOKA','SHOPEE','YOUTUBE'))
    name = st.text_input("-------------------INPUT FILENAME-------------------")
    choice = st.selectbox('--------SAVE MONGODB(Y/N)--------',('Y','N'))

    if st.button("PROCESSING"):
        col1,col2 = st.columns(2)
        cursor = dict_cursor[name_db]
        if name[0] == "\"":
            name = name[1:-1]
        name = name + ".csv"
        test = SQLIITE_service(name)
        col1.write("ONE QUERY EXAMPLE")
        col1.write(test.query_some_record(1))
        
        df = test.convert_to_csv()
        col1.write("DATA CRAWL OVERVIEW")
        col1.write(df.head(6))
        
        download,extension = FileDownloader(df.to_csv(),col1,name,file_ext='csv').download()
        file_details = {"FILENAME":download,"FILETYPE":"text/string","FILESIZE":sys.getsizeof(df), "NUM_COL": len(df.columns.to_list()),"NUM_ROW":len(df)}
        col1.write(file_details)
        col1.write("DATA OVERVIEW")
        col1.dataframe(df.head(6))
        
        if choice == 'Y':
            time.sleep(3)
            connect_address = 'mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
            createDB = MongoDB(connect_address,extension)
            createDB.createDb(df,download)
            col2.success("===Upload Success!!!===")
            col2.write("EXAMPLE")
            col2.write(createDB.query_one_collection(download))