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

class CrawlerTravelokaComment:
    def __init__(self,url,num_page):
        self.options = Options()
        #self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(url)
        self.num_page = num_page
        time.sleep(5)
    
    def getData(self):
        comment_dict = {'user_name': [],
                        'time_post': [],
                        'comment_post': [],
                        'num_like':[]}
        body = self.driver.find_element_by_css_selector('body')
        for i in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            if i == 5:
                time.sleep(2)
        time.sleep(3)
        doc = BeautifulSoup(self.driver.page_source,'html.parser')
        self.doc = doc
        num_page_now = 1
        while num_page_now < self.num_page:
                # selection_class_main = "style-scope ytd-comment-renderer"
                selection_class_main = "css-1dbjc4n r-qklmqi r-11u4nky"
                # main_tags = self.doc.find_all('div',{'class' : selection_class_main,'id' : selection_id_main})
                main_tags = self.doc.find_all('div',{'class' : selection_class_main})
                # replies_tags = self.doc.find_all('div',{'class' : "style-scope ytd-comment-thread-renderer",'id' : "replies"})
                
                user_name = self.getUserNameLst(main_tags)
                time_post = self.getTimePostLst(main_tags)
                comment_post = self.getCommentPostLst(main_tags)
                num_like = self.getNumLikeLst(main_tags)
                
                print(user_name, time_post, comment_post,num_like)
                # num_like = self.getNumLikeLst(main_tags)
                # subCommentTag = self.getNumSubComment(main_tags)
                min_len = int(min(len(user_name),len(time_post),len(comment_post),len(num_like)))
                comment_dict['user_name'] += user_name[:min_len]
                comment_dict['time_post'] += time_post[:min_len]
                comment_dict['comment_post'] += comment_post[:min_len]
                comment_dict['num_like'] += num_like[:min_len]
                time.sleep(2)
                
                direction = self.driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/div/div/div[1]/div/div/div[9]/div/div[6]') 
                if direction is None:
                    print("here")
                    break
                else:
                    num_page_now += 1
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
        selection_class_name = 'css-901oao r-1sixt3s r-1inkyih r-b88u0q r-135wba7 r-fdjqy7'
        # selection_id_name = 'author-text'
        
        for entry in main_tags:
            user_name_tag = entry.find('div',{'class' : selection_class_name})
            if user_name_tag is not None:
               user_name.append(user_name_tag.text.strip())
        return user_name
    
    def getTimePostLst(self,main_tags):
        time_post = []
        selection_class_time_post = 'css-901oao r-1ud240a r-1sixt3s r-1b43r93 r-b88u0q r-135wba7 r-fdjqy7 r-tsynxw' 
        
        for entry in main_tags:
            time_post_tag = entry.find('div',{'class' : selection_class_time_post})
            if time_post_tag is not None:
                text = time_post_tag.text.strip()
                time_post.append(text)
        
        return time_post
    
    def getCommentPostLst(self,main_tags):
        comment_post = []
        selection_class_comment = 'css-901oao r-1sixt3s r-ubezar r-majxgm r-135wba7 r-fdjqy7'
        # selection_id_comment = 'content-text'
        
        for entry in main_tags:
            comment_tag = entry.find('div',{'class' : selection_class_comment})
            if comment_tag is not None:
               comment_post.append(comment_tag.text.strip())
    
        return comment_post
    
    def getNumLikeLst(self,main_tags):
        num_like = []
        selection_class_like = "css-4rbku5 css-901oao r-1sixt3s r-1b43r93 r-b88u0q r-1cwl3u0 r-1jkjb r-fdjqy7"
        
        for entry in main_tags:
            like_tag = entry.find('h4',{'class' : selection_class_like})
            if like_tag is not None:
                text = like_tag.text
                text = re.findall('[0-9]+', text)
                if text != []:
                    num_like.append(text[0].strip())
                else:
                    num_like.append(0)
        
        return num_like
    
if __name__ == "__main__":
    url = "https://www.traveloka.com/en-vn/hotel/vietnam/harmony-saigon-hotel--spa-1000000312095?spec=27-05-2022.28-05-2022..1.HOTEL.1000000312095..1&currency=VND&contexts=%7B%22sourceHotelDetail%22%3A%22VNMCHHYGIENE2%20Desktop%22%2C%22accessCode%22%3A%223758VNMERCH1205%22%7D"
    crawlCmtShopee = CrawlerTravelokaComment(url,5)
    crawlCmtShopee.getData()
    # crawlCmtYoutube.saveData()
    crawlCmtShopee.driver.close()