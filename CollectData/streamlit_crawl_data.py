import streamlit as st
from CollectData.youtube_crawler import *
from CollectData.shopee_crawler import *
from CollectData.traveloka_crawler import *
from CollectData.MongoDB import *
from test_sqlite import *
# Utils
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import pandas as pd 

connect_address = 'mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

class FileDownloader(object):
	
	def __init__(self, data,col,filename='CRAWL',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext
		self.col = col

	def download(self,type = "YOUTUBE"):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}_{}.{}".format(self.filename,timestr,type,self.file_ext)
		self.col.markdown("#### Download File ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here!!</a>'
		self.col.markdown(href,unsafe_allow_html=True)
		return new_filename

def ShopeeCrawling():
    st.title("SHOPEE COMMENT")
    col1,col2 = st.columns(2)
    col1.markdown("#### CRAWLING TOOL ###")
    col2.markdown("#### RESULT ####")
    url = col1.text_input("----INPUT SHOPEE DOCUMENT URL----")
    save_mongoDB = col1.selectbox("----SAVE MONGO_DB (Y/N)----",('Y','N'))
    save_sqlite = col1.selectbox("----SAVE SQLITE (Y/N)----",('Y','N'))
    createDB = MongoDB(connect_address,"SHOPEE")
    if st.button("CRAWLING"):
        try:
            crawlCmtShopee = CrawlerShopeeComment(url)
            df = crawlCmtShopee.getData()
            crawlCmtShopee.driver.close()
            download = FileDownloader(df.to_csv(),col2,file_ext='csv').download("SHOPEE")
            col1.write("INFORMATION ABOUT DATA")
            col1.dataframe(df.head(6))
            col2.success("SUCCESSFUL!!")
            if save_mongoDB == 'Y':
                time.sleep(3)
                print("ohno2")
                createDB.createDb(df,download)
                print("ohno3")
                col2.success("===Upload Success!!!===")
                col2.write("MONGODB QUERY")
                col2.write(createDB.query_one_collection(download))
                print("ohno4")
            if save_sqlite == 'Y':
                time.sleep(2)
                test = SQLIITE_service(download,df)
                test.save_to_db()
                col2.write("SQLITE QUERY")
                col2.write(test.query_some_record(2))
        except:
            col2.error("ERROR CRAWLING")
            

def YoutubeCrawling_V1():
    st.title("YOUTUBE COMMENT")
    col1,col2 = st.columns(2)
    col1.markdown("#### CRAWLING TOOL ###")
    col2.markdown("#### RESULT ####")
    url = col1.text_input("----INPUT YOUTUBE URL----")
    num_scroll = col1.text_input("----INPUT YOUR NUM SCROLL----")
    save_mongoDB = col1.selectbox("----SAVE MONGO_DB (Y/N)----",('Y','N'))
    save_sqlite = col1.selectbox("----SAVE SQLITE (Y/N)----",('Y','N'))
    # df = None
    # download = None
    createDB = MongoDB(connect_address,"YOUTUBE")
    with col1:
        if col1.button("CRAWLING"):
            try:
                crawlCmtYoutube = CrawlerYoutubeComment(url,int(num_scroll))
                crawlCmtYoutube.scrollDown()
                df = crawlCmtYoutube.getData()
                crawlCmtYoutube.driver.close()
                download = FileDownloader(df.to_csv(),col2,file_ext='csv').download("YOUTUBE")
                col1.write("INFORMATION ABOUT DATA")
                col1.dataframe(df.head(6))
                col2.success("SUCCESSFUL!!")
                if save_mongoDB == 'Y':
                    time.sleep(3)
                    print("ohno2")
                    createDB.createDb(df,download)
                    print("ohno3")
                    col2.success("===Upload Success!!!===")
                    col2.write("MONGODB QUERY")
                    col2.write(createDB.query_one_collection(download))
                    print("ohno4")
                if save_sqlite == 'Y':
                    time.sleep(2)
                    test = SQLIITE_service(download,df)
                    test.save_to_db()
                    col2.write("SQLITE QUERY")
                    col2.write(test.query_some_record(2))
            except:
                col2.error("ERROR CRAWLING")
                
                
    
def TravelokaCrawling():
    st.title("TRAVELOKA COMMENT")
    col1,col2 = st.columns(2)
    col1.markdown("#### CRAWLING TOOL ###")
    col2.markdown("#### RESULT ####")
    url = col1.text_input("----INPUT TRAVELOKA URL----")
    num_page = col1.text_input("----INPUT YOUR NUM PAGE----")
    save_mongoDB = col1.selectbox("----SAVE MONGO_DB (Y/N)----",('Y','N'))
    save_sqlite = col1.selectbox("----SAVE SQLITE (Y/N)----",('Y','N'))
    createDB = MongoDB(connect_address,"TRAVELOKA")
    if st.button("CRAWLING"):
        try:
            crawlCmtTraveloka = CrawlerTravelokaComment(url,int(num_page))
            df = crawlCmtTraveloka.getData()
            crawlCmtTraveloka.driver.close()
            download = FileDownloader(df.to_csv(),col2,file_ext='csv').download("TRAVELOKA")
            col1.write("INFORMATION ABOUT DATA")
            col1.dataframe(df.head(6))
            col2.success("SUCCESSFUL!!")
            if save_mongoDB == 'Y':
                time.sleep(3)
                print("ohno2")
                createDB.createDb(df,download)
                print("ohno3")
                col2.success("===Upload Success!!!===")
                col2.write("MONGODB QUERY")
                col2.write(createDB.query_one_collection(download))
                print("ohno4")
            if save_sqlite == 'Y':
                time.sleep(2)
                test = SQLIITE_service(download,df)
                test.save_to_db()
                col2.write("SQLITE QUERY")
                col2.write(test.query_some_record(2))
        except:
            col2.error("ERROR CRAWLING")



            
    