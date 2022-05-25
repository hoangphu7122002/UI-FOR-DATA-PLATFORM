import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import string

def get_dictionary():
    with open('glove.6B.50d.txt', 'r',encoding="utf8") as f:
        words = set()
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
        return list(words)
        
dictionary = get_dictionary()        
        
def get_extension(text):
    text = text[:-4]
    text = text.split("_")
    return text[-1]

def check_englisth_comment(sentence):
    words = sentence.lower().strip().split()
    count = 0
    for word in words:
        if word in dictionary:
           count += 1
    if count > (0.5 * len(sentence.split())):
       return 1
    return 0
        
def remove_emojis(data):
    emoji = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoji, '', data)

def str_to_int(line):    
    #arxify,15 hours ago,"had this on loop since jan, 13, 2017",71,6
    #6 months ago
    #5 days ago
    #1 month ago
    #1 day ago
    #1 year ago
    #2 weeks ago
    temp = line
    if line[-1] == 'K':
        if line.find('.') == -1:
            temp = line[:-1] + "000"
            temp = int(temp)
        else:
            substr = line[:-1]
            lst_word = substr.strip().split('.')
            print(line)
            # print(lst_word)
            if len(lst_word[1]) == 1:
                temp = lst_word[0] + lst_word[1] + "00"
            elif len(lst_word[1]) == 2:
                temp = lst_word[0] + lst_word[1] + "0"
            elif len(lst_word[1]) == 3:
                temp = lst_word[0] + lst_word[1]
                temp = int(temp)
    elif len(line.split(' ')) == 1:
        temp = int(line)
    else:    
        #1 month ago
        lst_word = line.strip().split(' ')
        if lst_word[1] == "hour" or lst_word[1] == "hours":
            temp = int(lst_word[0])
        if lst_word[1] == "day" or lst_word[1] == "days":
            temp = int(lst_word[0]) * 24
        if lst_word[1] == "month" or lst_word[1] == "months":
            temp = int(lst_word[0]) * 24 * 30
        if lst_word[1] == "year" or lst_word[1] == "years":
            temp = int(lst_word[0]) * 24 * 30 * 12
        if lst_word[1] == "week" or lst_word[1] == "weeks":
            temp = int(lst_word[0]) * 24 * 7
    return temp
    
def clean_comment(tokenizer,stemmer,stopwords_english,line):
    #get content in "" if exist
    if line[0] == "" and line[-1] == "":
        line = line[1:-1]
    
    #convert to lower digit
    line = line.lower()
    
    #remove hyperlink
    line = re.sub(r'https?:\/\/.*[\r\n]*', '', line)
    line = re.sub(r'http?:\/\/.*[\r\n]*', '', line)
    
    #remove hashtag
    line = re.sub(r'#(\w+)','',line)
    
    #remove emoji
    line = remove_emojis(line)
                               
    line_clean = []  
    
    line_tokens = tokenizer.tokenize(line)
    
    for word in line_tokens:
        if word not in stopwords_english and word not in string.punctuation:
            line_clean.append(stemmer.stem(word))
    
    return ' '.join(line_clean)

class CLEAN_CSV(object):
    def __init__(self,filename,df = None):
        #use for clean_data
        self.stemmer = PorterStemmer()
        self.stopwords_english = stopwords.words('english')
        self.tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                   reduce_len=True)
                                   
        self.filename = filename
        if df is None:
            self.df = pd.read_csv(filename)
        else:
            self.df = df
        if "unnamed: 0" in self.get_col_name():
            self.df = self.df.drop('unnamed: 0', 1)
        self.getEnglishData = False
        self.geCleanData = False
        self.extension = get_extension(self.filename)
        self.getConvertType_numLike = (self.extension != "YOUTUBE")
        self.getConvertType_timePost = (self.extension != "YOUTUBE")
        
    def get_col_name(self):
        self.df.columns = self.df.columns.str.lower()
        return self.df.columns.to_list()
    
    def convert_str_to_numeric(self,colname,method = str_to_int):
        if type(self.df[colname].iloc[0]) != str: print("not type string")
        else:
            self.df[colname] = self.df[colname].apply(lambda row :  method(row))
            if colname == "time_post":
                self.getConvertType_timePost = True
            else:
                self.getConvertType_numLike = True
            print("=====success!!=====")
        
    def clean_comment(self,colname):
        # try:
            print("hehe0")
            self.df[colname] = self.df[colname].apply(lambda row : clean_comment(self.tokenizer,self.stemmer,self.stopwords_english,row))
            print("hehe1")
            self.geCleanData = True
            print("=====success!!=====")
        # except:
        #     print("error handling")
            
    def get_comment_english(self,colname):
        # try:
            self.df = self.df.dropna()
            self.df["check_english"] =  self.df[colname].apply(check_englisth_comment)
            print("here1")
            self.df = self.df[self.df["check_english"] == 1]
            print("here2")
            self.df = self.df.drop("check_english", 1)
            print("here3")
            self.getEnglishData = True
            print("=====success!!=====")
        # except:
        #     print("error in processing")
    
    def end_to_end_process_yt(self):
        if self.getEnglishData == False:
            self.get_comment_english('comment_post')
        if self.geCleanData == False:
            self.clean_comment('comment_post')
        if self.getConvertType_timePost == False and self.extension == "YOUTUBE":
            self.convert_str_to_numeric('time_post')
        if self.getConvertType_numLike == False and self.extension == "YOUTUBE":
            self.convert_str_to_numeric('num_like')
        
    def get_clean_data(self):
        # self.end_to_end_process_yt()
        col_usage = ["user_name","time_post","comment_post"]
        return self.df[col_usage]
    
    def save_data(self):
        self.df.to_csv(self.filename,index = None,encoding = 'utf-8')
            
        
    
if __name__ == '__main__':
    filename = "myfile_20220409-134028_.csv"
    cleanCsvModule = CLEAN_CSV(filename)
    print(cleanCsvModule.get_col_name())
    cleanCsvModule.end_to_end_process_yt()
    cleanCsvModule.save_data()
    
    