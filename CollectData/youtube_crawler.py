import selenium
from selenium import webdriver
print(selenium.__version__)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import re

class CrawlerYoutubeComment:
    def __init__(self,url,num_scroll):
        self.options = Options()
        #self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(url)
        self.num_scroll = num_scroll
    
    def scrollDown(self):
        
        # time.sleep(5)
        body = self.driver.find_element_by_css_selector('body')
        i = 0
        while(True):
            #scroll down to the buttom
            print("IN PROCESS TIME {}\n".format(i + 1))
            for j in range(2):
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            print("SUCCESS PROCESS {} !!!\n".format(i + 1))
            if i == self.num_scroll:
                break
            i += 1
        print("SUCCESS")
        doc = BeautifulSoup(self.driver.page_source,'html.parser')
        self.doc = doc
    
    def getData(self):
            
        # selection_class_main = "style-scope ytd-comment-renderer"
        selection_class_main = "style-scope ytd-item-section-renderer"
        selection_id_main = "main"
        # main_tags = self.doc.find_all('div',{'class' : selection_class_main,'id' : selection_id_main})
        main_tags = self.doc.find_all('ytd-comment-thread-renderer',{'class' : selection_class_main})
        # replies_tags = self.doc.find_all('div',{'class' : "style-scope ytd-comment-thread-renderer",'id' : "replies"})
        
        user_name = self.getUserNameLst(main_tags)
        time_post = self.getTimePostLst(main_tags)
        comment_post = self.getCommentPostLst(main_tags)
        num_like = self.getNumLikeLst(main_tags)
        subCommentTag = self.getNumSubComment(main_tags)
        
        comment_dict = {'user_name': user_name,
                        'time_post': time_post,
                        'comment_post': comment_post,
                        'num_like': num_like,
                        'num_subcomments' : subCommentTag}
        self.data = pd.DataFrame(comment_dict)
        return self.data
        
    def saveData(self):
        self.data.to_csv("data_raw{}.csv".format(timestr),index = None,encoding = 'utf-8')
        
    def getUserNameLst(self,main_tags):
        user_name = []
        selection_class_name = 'yt-simple-endpoint style-scope ytd-comment-renderer'
        selection_id_name = 'author-text'
        
        for entry in main_tags:
            user_name_tag = entry.find('a',{'class' : selection_class_name,'id' : selection_id_name})
            if user_name_tag is not None:
               user_name.append(user_name_tag.text.strip())
        return user_name
    
    def getNumSubComment(self,main_tags):
        SubComment = []
        selection_class_name = "style-scope ytd-button-renderer"
        selection_id = "text"
        for entry in main_tags:
            subCommentTag = entry.findAll('yt-formatted-string',{'class' : selection_class_name,'id' : selection_id})
            if subCommentTag == []:
                SubComment.append("0")
            else:
                temp_digit = re.findall('[0-9]+',subCommentTag[1].text.strip())
                if len(temp_digit) == 0:
                    SubComment.append("0")
                else:
                    SubComment.append(temp_digit[0])
        return SubComment
    
    def getTimePostLst(self,main_tags):
        time_post = []
        selection_class_time_post = 'yt-simple-endpoint style-scope yt-formatted-string' 
        
        for entry in main_tags:
            time_post_tag = entry.find('a',{'class' : selection_class_time_post})
            if time_post_tag is not None:
               time_post.append(time_post_tag.text.strip())
        
        return time_post
    
    def getCommentPostLst(self,main_tags):
        comment_post = []
        selection_class_comment = 'style-scope ytd-comment-renderer'
        selection_id_comment = 'content-text'
        
        for entry in main_tags:
            comment_tag = entry.find('yt-formatted-string',{'class' : selection_class_comment,'id' : selection_id_comment})
            if comment_tag is not None:
               comment_post.append(comment_tag.text.strip())
    
        return comment_post
    
    def getNumLikeLst(self,main_tags):
        num_like = []
        selection_class_like = 'style-scope ytd-comment-action-buttons-renderer'
        selection_id_like = 'vote-count-middle'
        
        for entry in main_tags:
            like_tag = entry.find('span',{'class' : selection_class_like,'id' : selection_id_like})
            if like_tag is not None:
               num_like.append(like_tag.text.strip())
        
        return num_like
        
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=mWRsgZuwf_8&list=RDEMrP1xMaEmkxteWhBxMXKITA&index=5"
    crawlCmtYoutube = CrawlerYoutubeComment(url,3)
    crawlCmtYoutube.scrollDown()
    crawlCmtYoutube.getData()
    crawlCmtYoutube.saveData()
    crawlCmtYoutube.driver.close()