from PredictData.predict_naive_bayes import *
from PredictData.predict_bert import *
from PredictData.MongoDB import *
import pandas as pd
import streamlit as st
import numpy as np
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import sys
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
		name_part[0] = "PREDICT"
		extension = name_part[-1].split('.')[0]
		new_filename = "_".join(name_part)
		self.col.markdown("#### DOWNLOAD FILE ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">CLICK HERE!!</a>'
		self.col.markdown(href,unsafe_allow_html=True)
		return new_filename,extension

def predict():
    col1,col2 = st.columns(2)
    col1.title("DATA PREDICTION")
    col2.title("")
    col1.markdown("#### UPLOAD FILE ###")
    df = col1.file_uploader("",type = ["csv"])
    
    choice = col1.selectbox('--------MODEL--------',('NAIVE_BAYES','BERT'))
    choice1 = col1.selectbox('--------SAVE MONGODB-------',('Y','N'))
    choice2 = col1.selectbox('--------SAVE SQLITE--------',('Y','N'))
    if col1.button("PREDICT"):
        download,extension,data = predict_page(col2,df,choice)
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
    
def predict_page(module,filename,choice):
    if choice == "NAIVE_BAYES":
        data = load_csv_and_predict(filename)
    else:
        data = load_csv_and_predict_bert(filename)
    statistic = {}
    download,extension = FileDownloader(data.to_csv(),module,filename.name,file_ext='csv').download()
    statistic["FILENAME"] = download
    statistic["FILETYPE"] = filename.type
    statistic["FILESIZE"] = sys.getsizeof(data)
    statistic["NUM_COL"] = len(data.columns.to_list())
    statistic["NUM_ROW"] = len(data)
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
    module.write(statistic)
    return download,extension,data