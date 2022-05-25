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
from selenium.webdriver.common.action_chains import ActionChains

timestr = time.strftime("%Y%m%d-%H%M%S")
import re

class CrawlerShopeeComment:
    def __init__(self,url):
        self.options = Options()
        #self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(5)
    
    def getData(self):
        comment_dict = {'user_name': [],
                        'time_post': [],
                        'comment_post': []}
        body = self.driver.find_element_by_css_selector('body')
        for i in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            if i == 5:
                time.sleep(2)
        time.sleep(3)
        doc = BeautifulSoup(self.driver.page_source,'html.parser')
        self.doc = doc
        with open('xpath.txt', 'r') as reader:
            for line in reader:
                # selection_class_main = "style-scope ytd-comment-renderer"
                selection_class_main = "shopee-product-rating__main"
                # main_tags = self.doc.find_all('div',{'class' : selection_class_main,'id' : selection_id_main})
                main_tags = self.doc.find_all('div',{'class' : selection_class_main})
                # replies_tags = self.doc.find_all('div',{'class' : "style-scope ytd-comment-thread-renderer",'id' : "replies"})
                
                user_name = self.getUserNameLst(main_tags)
                time_post = self.getTimePostLst(main_tags)
                comment_post = self.getCommentPostLst(main_tags)
                print(user_name, time_post, comment_post)
                # num_like = self.getNumLikeLst(main_tags)
                # subCommentTag = self.getNumSubComment(main_tags)
                min_len = int(min(len(user_name),len(time_post),len(comment_post)))
                comment_dict['user_name'] += user_name[:min_len]
                comment_dict['time_post'] += time_post[:min_len]
                comment_dict['comment_post'] += comment_post[:min_len]
                time.sleep(2)
                
                direction = self.driver.find_element_by_xpath(line.strip()) 
                if direction is None:
                    print("here")
                    break
                else:
                    try:
                        direction.send_keys(Keys.ENTER)
                    except:
                        break
                    time.sleep(3)
                    self.doc = BeautifulSoup(self.driver.page_source,'html.parser')
                
        self.data = pd.DataFrame(comment_dict)
        return self.data
        
    def saveData(self):
        self.data.to_csv("data_raw{}.csv".format(timestr),index = None,encoding = 'utf-8')
        
    def getUserNameLst(self,main_tags):
        user_name = []
        selection_class_name = 'shopee-product-rating__author-name'
        # selection_id_name = 'author-text'
        
        for entry in main_tags:
            user_name_tag = entry.find('div',{'class' : selection_class_name})
            if user_name_tag is not None:
               user_name.append(user_name_tag.text.strip())
        return user_name
    
    def getTimePostLst(self,main_tags):
        time_post = []
        selection_class_time_post = 'shopee-product-rating__time' 
        
        for entry in main_tags:
            time_post_tag = entry.find('div',{'class' : selection_class_time_post})
            if time_post_tag is not None:
                text = time_post_tag.text
                text = text[0:text.find('|')].strip()
                time_post.append(text)
        
        return time_post
    
    def getCommentPostLst(self,main_tags):
        comment_post = []
        selection_class_comment = 'Em3Qhp'
        # selection_id_comment = 'content-text'
        
        for entry in main_tags:
            comment_tag = entry.find('div',{'class' : selection_class_comment})
            if comment_tag is not None:
               comment_post.append(comment_tag.text.strip())
    
        return comment_post
        
if __name__ == "__main__":
    url = "https://shopee.sg/(Full-Coverage)-IPhone-13-12-Pro-Max-11-Pro-Max-X-XS-Max-Tempered-Glass-Screen-Protector-i.15961547.277862695"
    crawlCmtShopee = CrawlerShopeeComment(url)
    crawlCmtShopee.getData()
    # crawlCmtYoutube.saveData()
    crawlCmtShopee.driver.close()