from PredictData import predict_naive_bayes
from PredictData import predict_bert
from VisualizeData import visualize
from CleanData import clean_csv
import streamlit as st
import pandas as pd
import numpy as np
import sys
import base64
from CleanData.streamlit_clean_data import *
import test_sqlite

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
		name_part[0] = "PREDICT"
		extension = name_part[-1].split('.')[0]
		new_filename = "_".join(name_part)
		self.col.markdown("#### DOWNLOAD FILE ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">CLICK HERE!!</a>'
		self.col.markdown(href,unsafe_allow_html=True)
		return new_filename,extension

def end_to_end_process(mode="CSV"):
    st.title("END TO END PROCESSING")
    # st.markdown("#### UploadDTS ###")  
    col1,col2 = st.columns(2)
    if mode == "CSV":
        col1.markdown("#### UPLOAD FILE ###")
        df = col1.file_uploader("",type = ["csv"])    
    elif mode == "MONGODB":
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
    else:
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
        
    download = ""
    if mode == "CSV":
        choice = col1.selectbox('--------MODEL--------',('NAIVE_BAYES','BERT'))
        choice1 = col1.selectbox('--------SAVE MONGODB-------',('Y','N'))
        choice2 = col1.selectbox('--------SAVE SQLITE-------',('Y','N'))
    else:
        choice = st.selectbox('--------MODEL--------',('NAIVE_BAYES','BERT'))
        choice1 = st.selectbox('--------SAVE MONGODB-------',('Y','N'))
        choice2 = st.selectbox('--------SAVE SQLITE-------',('Y','N'))
    
    if col1.button("START"):
        #clean data
        filename = ""
        if mode == "CSV":
            filename = df.name
            df1 = pd.read_csv(df)
            file_details = {"FILENAME":df.name, "FILETYPE":df.type,
                                "FILESIZE":sys.getsizeof(df1), "NUM_COL" : len(df1.columns.to_list()), "NUM_ROW" : len(df1)}
            col1.write(file_details)
            
            col1.write("DATA OVERVIEW")
            col1.dataframe(df1.head(6))
        elif mode == "MONGODB":
            col1,col2 = st.columns(2)
            if name[0] == "\"":
                name = name[1:-1]
            db_name_file = ""
            for key,value in dict_collect.items():
                if name in value:
                    db_name_file = key 
            collection = cluster[db_name_file][name]
            df1 = pd.DataFrame()
            for ele in collection.find():
                if '_id' in ele:
                    del ele['_id']
                print(ele)
                df1 = df1.append(ele,ignore_index=True)
            #before processing data
            file_details = {"FILENAME":name, "FILETYPE":"text/string",
                                "FILESIZE":sys.getsizeof(df1), "NUM_COL" : len(df1.columns.to_list()), "NUM_ROW" : len(df1)}
            col1.write(file_details)
            try:
                col1.write("DATA OVERVIEW")
                col1.dataframe(df1.head(6))
            except:
                pass
            filename = name
        else:
            col1,col2 = st.columns(2)
            cursor = dict_cursor[name_db]
            if name[0] == "\"":
                name = name[1:-1]
            name = name + ".csv"
            test = SQLIITE_service(name)
            col1.write("ONE QUERY EXAMPLE")
            col1.write(test.query_some_record(1))
            
            df1 = test.convert_to_csv()
            col1.write("DATA CRAWL OVERVIEW")
            col1.write(df1.head(6))
            filename = name
        #clean data
        check_extension = filename.split('_')[0]
        if check_extension != "CLEAN":
            cleanCsvModule = clean_csv.CLEAN_CSV(filename,df1)
            cleanCsvModule.end_to_end_process_yt()
    
            test = cleanCsvModule.get_clean_data()
            download,extension = FileDownloader(test.to_csv(),col2,filename,file_ext='csv').download()
            file_details = {"FILENAME":download,"FILETYPE":"text/string","FILESIZE":sys.getsizeof(test), "NUM_COL": len(test.columns.to_list()),"NUM_ROW":len(test)}
            col2.write(file_details)
            col2.write("DATA OVERVIEW")
            col2.dataframe(test.head(6))     
        else:
            test = df1
        #predict data        
        if choice == "NAIVE_BAYES":
            data = predict_naive_bayes.load_csv_and_predict(test,1)
        else:
            data = predict_bert.load_csv_and_predict_bert(test,1)
        statistic = {}
        pos = statistic["POSITIVE"] = np.sum(data.target == 1).squeeze()
        neg = statistic["NEGATIVE"] = np.sum(data.target == 0).squeeze()
        print("=================================")
        print(pos,neg)
        print("=================================")
        if pos > neg:
            statistic["CONTENT"] = "POSITIVE CONTENT"
        elif pos == neg:
            statistic["CONTENT"] = "NEUTRAL CONTENT"
        else:
            statistic["CONTENT"] = "NEGATIVE CONTENT"
        col1.write(statistic)
        # name_part = download.split('_')
        # name_part[0] = "PREDICT"
        # extension = name_part[-1].split('.')[0]
        # new_filename = "_".join(name_part)
        
        #visualize data
        plot_model = visualize.PLOT_MODULE(data,download,col1,col2)
        #left hide information
        plot_model.show_word_distrib()
        plot_model.plot_average_word_length()
        plot_model.unique_words()
        if 'target' in data.columns.to_list():
            plot_model.plot_hist_classes(plot_model.to_plot_chars_target)
            plot_model.plot_hist_classes(plot_model.to_plot_word_target)
        else:
            plot_model.plot_hist_classes(plot_model.to_plot_chars)
            plot_model.plot_hist_classes(plot_model.to_plot_word)
        
        #right hide information
        plot_model.plot_n_gram(2)
        plot_model.plot_n_gram(3)
        plot_model.plot_n_gram(4)
        plot_model.plot_n_gram(5)
        plot_model.statistics_information()    
        if choice1 == 'Y':
            connect_address = 'mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
            createDB = MongoDB(connect_address,extension)
            createDB.createDb(data,download)
            col2.success("===Upload Success!!!===")
            col2.write("EXAMPLE")
            col2.write(createDB.query_one_collection(download))
        if choice2 == 'Y':
            time.sleep(2)
            test1 = SQLIITE_service(download,data)
            test1.save_to_db()
            col2.write("SQLITE QUERY")
            col2.write(test1.query_some_record(2))
        
# end_to_end_process()