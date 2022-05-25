import pandas as pd
import streamlit as st
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import sys
# import pandas as pd 
from CleanData.clean_csv import *
from CleanData.MongoDB import *
from test_sqlite import *

connect_address = 'mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

class FileDownloader(object):
	def __init__(self, data,col,filename,file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext
		self.col = col

	def download(self,type = None):
		b64 = base64.b64encode(self.data.encode()).decode()
		name_part = self.filename.split('_')
		name_part[0] = "CLEAN"
		extension = name_part[-1].split('.')[0]
		new_filename = "_".join(name_part)
		self.col.markdown("#### DOWNLOAD FILE ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">CLICK HERE!!</a>'
		self.col.markdown(href,unsafe_allow_html=True)
		return new_filename,extension

def processingCSV():
    st.title("PROCESSING DATA")
    # st.markdown("#### UploadDTS ###")  
    col1,col2 = st.columns(2)
    col1.markdown("#### UPLOAD FILE ###")
    df = col1.file_uploader("",type = ["csv"])
    
    if df is not None:
        filename = df.name
        df1 = pd.read_csv(df)
        file_details = {"FILENAME":df.name, "FILETYPE":df.type,
                            "FILESIZE":sys.getsizeof(df1), "NUM_COL" : len(df1.columns.to_list()), "NUM_ROW" : len(df1)}
        col1.write(file_details)
        
        col1.write("DATA OVERVIEW")
        col1.dataframe(df1.head(6))
        
        choice = col1.selectbox('----SAVE MONGO_DB (Y/N)----',('Y','N'))
        choice1 = col1.selectbox('----SAVE SQLITE (Y/N)----',('Y','N'))
        if col1.button("PROCESSING"):
            cleanCsvModule = CLEAN_CSV(filename,df1)
            cleanCsvModule.end_to_end_process_yt()

            test = cleanCsvModule.get_clean_data()
            download,extension = FileDownloader(test.to_csv(),col2,filename,file_ext='csv').download()
            file_details = {"FILENAME":download,"FILETYPE":df.type,"FILESIZE":sys.getsizeof(test), "NUM_COL": len(test.columns.to_list()),"NUM_ROW":len(test)}
            col2.write(file_details)
            col2.write("DATA OVERVIEW")
            col2.dataframe(test.head(6))
            if choice == 'Y':
                time.sleep(3)
                print("ohno2")
                createDB = MongoDB(connect_address,extension)
                createDB.createDb(test,download)
                print("ohno3")
                col2.success("===Upload Success!!!===")
                col2.write("EXAMPLE")
                col2.write(createDB.query_one_collection(download))
            if choice1 == 'Y':
                time.sleep(2)
                test1 = SQLIITE_service(download,test)
                test1.save_to_db()
                col2.write("SQLITE QUERY")
                col2.write(test1.query_some_record(2))
            # cleanCsvModule.save_data()
    
def processingMongoDB():
    st.title("MONGODB PROCESSING DATA")
    
    ip_address = "mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    
    cluster = MongoClient(ip_address)
    db_name = cluster.list_database_names()[:3]
    dict_collect = {db_name[0] : cluster[db_name[0]].list_collection_names(),
                    db_name[1] : cluster[db_name[1]].list_collection_names(),
                    db_name[2] : cluster[db_name[2]].list_collection_names()
                    }
    
    col1,col2,col3 = st.columns(3)
    col1.markdown(db_name[0])
    col1.write(cluster[db_name[0]].list_collection_names())
    
    col2.markdown(db_name[1])
    col2.write(cluster[db_name[1]].list_collection_names())
    
    col3.markdown(db_name[2])
    col3.write(cluster[db_name[2]].list_collection_names())
    
    
    name = st.text_input("-------------------INPUT FILENAME-------------------")
    choice = st.selectbox('----SAVE MONGO_DB (Y/N)----',('Y','N'))
    choice1 = st.selectbox('----SAVE SQLITE (Y/N)----',('Y','N'))
    if st.button("START"):
        if name[0] == "\"":
            name = name[1:-1]
        db_name_file = ""
        for key,value in dict_collect.items():
            if name in value:
                db_name_file = key 
        collection = cluster[db_name_file][name]
        df = pd.DataFrame()
        for ele in collection.find():
            if '_id' in ele:
                del ele['_id']
            print(ele)
            df = df.append(ele,ignore_index=True)
        #before processing data
        file_details = {"FILENAME":name, "FILETYPE":"text/string",
                            "FILESIZE":sys.getsizeof(df), "NUM_COL" : len(df.columns.to_list()), "NUM_ROW" : len(df)}
        st.write(file_details)
        
        st.write("DATA OVERVIEW")
        st.dataframe(df.head(6))
        
        #after that
        cleanCsvModule = CLEAN_CSV(name,df)
        cleanCsvModule.end_to_end_process_yt()

        test = cleanCsvModule.get_clean_data()
        download,extension = FileDownloader(test.to_csv(),st,name,file_ext='csv').download()
        file_details = {"FILENAME":download,"FILETYPE":"text/string","FILESIZE":sys.getsizeof(test), "NUM_COL": len(test.columns.to_list()),"NUM_ROW":len(test)}
        st.write(file_details)
        st.write("DATA OVERVIEW")
        st.dataframe(test.head(6))
        
        if choice == 'Y':
            time.sleep(3)
            createDB = MongoDB(connect_address,extension)
            createDB.createDb(test,download)
            st.success("===Upload Success!!!===")
            st.write("EXAMPLE")
            st.write(createDB.query_one_collection(download))
        if choice1 == 'Y':
            time.sleep(2)
            test1 = SQLIITE_service(download,test)
            test1.save_to_db()
            st.write("SQLITE QUERY")
            st.write(test1.query_some_record(2))
        
def processing_sqlite():
    pass