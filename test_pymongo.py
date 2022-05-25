import pymongo
import json
from pymongo import MongoClient
import pandas as pd
import streamlit as st
from bson import Code
import base64
from test_sqlite import *
import time

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

def collect_mongoDB():
    st.title("MONGODB ASSEMBLE")
    
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
    choice = st.selectbox('--------OPERATION--------',('ASSEMBLE','DELETE'))
    choice1 = st.selectbox('--------SAVE SQLITE(Y/N) IF ASSEMBLE--------',('Y','N'))
    if st.button("START"):
        if name[0] == "\"":
            name = name[1:-1]
        db_name_file = ""
        for key,value in dict_collect.items():
            if name in value:
                db_name_file = key 
        collection = cluster[db_name_file][name]
        if choice == "ASSEMBLE":
            col1,col2 = st.columns(2)
            ele = collection.find_one()
            #schema object
            key_ele = [key for key in ele.keys()]
            statistic = {
                        "key: " : key_ele,
                        "type: " : "string",
                        "one_record_example: " : ele}
            col1.markdown("======STATISTIC INFORMATION======")
            col1.write(statistic) 
            df = pd.DataFrame()
            for ele in collection.find():
                if '_id' in ele:
                    del ele['_id']
                print(ele)
                df = df.append(ele,ignore_index=True)
            
            col1.write(df.head(6))
            download,extension = FileDownloader(df.to_csv(),col2,name,file_ext='csv').download()
            
            if choice1 == 'Y':
                time.sleep(2)
                test = SQLIITE_service(download,df)
                test.save_to_db()
                col2.write("SQLITE QUERY")
                col2.write(test.query_some_record(2))
        else:
            collection.drop()
        