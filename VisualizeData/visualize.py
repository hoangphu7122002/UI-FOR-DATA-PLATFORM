import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyplot
import nltk
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

stop=set(stopwords.words('english'))
def get_top_ngram(corpus, n  = None):
    vec = CountVectorizer(ngram_range=(n, n),stop_words=stop).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:20]
        

class PLOT_MODULE(object):
    def __init__(self,df,filename,module_L = None,module_R = None):
        # self.filename = filename
        self.df = df
        if "unnamed: 0" in self.get_col_name():
            self.df = self.df.drop('unnamed: 0', 1)
        self.df = self.df.dropna()
        self.type = filename.split('_')[0]
        self.mode = filename.split('_')[-1].split('.')[0]
        self.module_L = module_L
        self.module_R = module_R
        self.train_test = False
        self.validation()
            
    def get_col_name(self):
        return self.df.columns.to_list()
            
    def validation(self):
        if self.mode == "YOUTUBE" and self.type == "CLEAN":
            if "time_post" in self.df.columns.to_list():
                self.df['time_post'] = self.df['time_post'].astype(int)
            if "num_like" in self.df.columns.to_list():
                self.df['num_like'] = self.df['num_like'].astype(int)
            if "num_subcomments" in self.df.columns.to_list():
                self.df['num_subcomments'] = self.df['num_subcomments'].astype(int)
            
        if 'target' in self.df.columns.to_list():
            self.train_test = True
    
    def show_word_distrib(self,field = "comment_post",top_N = 10):
        fig = plt.figure()    
        txt = self.df[field]
        temp = ""
        for line in txt:
            temp = temp + line + " "
        words = nltk.tokenize.word_tokenize(temp)
        words_except_stop_dist = nltk.FreqDist(words) 
        
        word_frequency = pd.DataFrame(words_except_stop_dist.most_common(top_N),columns = ['Word','Frequency Text']).set_index('Word')
        
        ax1 = fig.add_subplot()
        word_frequency.plot.bar(rot = 0,ax = ax1)
        if self.module_L is None:
            plt.show()
        else:
            self.module_L.write("ABOUT WORD ATTRIBUTES")
            self.module_L.pyplot(fig)
        plt.close()
    
    def get_number_sample(self):
        return len(self.df)
        
    def to_plot_chars(self,col = "comment_post"):
        return self.df[col].str.len()
        
    def to_plot_word(self,col = "comment_post"):
        return self.df[col].str.split(' ').map(lambda x : len(x))
    
    def to_plot_chars_target(self,target,col = "comment_post"): 
        return self.df[self.df['target']== target][col].str.len()
    
    def to_plot_word_target(self,target,col = "comment_post"):
        return self.df[self.df['target']== target][col].str.split().map(lambda x: len(x))    
    
    def plot_hist_classes(self,to_plot,col = "comment_post"):
        if self.train_test == True:
            fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))
    
            df_len = to_plot(0, col)
            ax1.hist(df_len,color='red')
            ax1.set_title('Negative Tweets')
            
            df_len = to_plot(1, col)
            ax2.hist(df_len,color='green')
            ax2.set_title('Positive Tweets')    
            
            fig.suptitle("information")
            if self.module_L is None:
                plt.show()
            else:
                if to_plot == self.to_plot_word_target:
                    self.module_L.write("PLOT HIST WORDS")
                else:
                    self.module_L.write("PLOT HIST CHARS")
                self.module_L.pyplot(fig)
            plt.close()
        else:
            fig,ax = plt.subplots(1)
            df = to_plot(col)
            ax.hist(df,color = 'blue')
            fig.suptitle("information")
            if self.module_L is None:
                plt.show()
            else:
                if to_plot == self.to_plot_word:
                    self.module_L.write("PLOT HIST WORDS")
                else:
                    self.module_L.write("PLOT HIST CHARS")
                self.module_L.pyplot(fig)
            plt.close()
            
    def plot_average_word_length(self,col = "comment_post"):
        print("Average word length in comment post\n")
        if self.train_test == True:
            fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))
    
            word = self.df[self.df['target']== 0][col].str.split().apply(lambda x : [len(i) for i in x])
            sns.distplot(word.map(lambda x: np.mean(x)),ax=ax1,color='red')
            ax1.set_title('Negative')
            
            word = self.df[self.df['target']== 1][col].str.split().apply(lambda x : [len(i) for i in x])
            sns.distplot(word.map(lambda x: np.mean(x)),ax=ax2,color='green')
            ax2.set_title('Positive')
            
            fig.suptitle('Average word length in each tweet')
            if self.module_L is None:
                plt.show()
            else:
                self.module_L.write("AVERAGE WORD LENGTH")
                self.module_L.pyplot(fig)
            plt.close()

        else:
            fig,ax = plt.subplots(1)
            word = self.df[col].str.split(' ').apply(lambda x : [len(i) for i in x])
            sns.distplot(word.map(lambda x: np.mean(x)),ax=ax,color='blue')
            
            fig.suptitle('Average word length in each tweet')
            if self.module_L is None:
                plt.show()
            else:
                self.module_L.write("AVERAGE WORD LENGTH")
                self.module_L.pyplot(fig)
            plt.close()
            
    def unique_words(self,col = "comment_post",title = "distribution of number of unique words"):
        print("Number of unique word in comment_text\n")
        if self.train_test == True:
            fig,ax=plt.subplots(1,2,figsize=(12,7))
            colors = {
                "1": "green",
                "0": "red"
            }
            for _, i in enumerate([0, 1]):
                new=self.df[self.df['target']==i][col].map(lambda x: len(set(x.split())))
                sns.distplot(new.values,ax=ax[_],color=colors[str(i)])
                ax[_].set_title(str(i))
            fig.suptitle(title)
            if self.module_L is None:
                plt.show()
            else:
                self.module_L.write("ABOUT UNIQUE WORD")
                self.module_L.pyplot(fig)
            plt.close()
        else:
            fig,ax = plt.subplots(1)
            word = self.df[col].map(lambda x : len(set(x.split(' '))))
            sns.distplot(word.values,ax=ax,color="blue")
            fig.suptitle(title)
            if self.module_L is None:
                plt.show()
            else:
                self.module_L.write("ABOUT UNIQUE WORD")
                self.module_L.pyplot(fig)
            plt.close()
    
    def plot_n_gram(self,size = 2,col = "comment_post"):
        fig,ax = plt.subplots(1)
        new = self.df[col]
        top_n_bigrams= get_top_ngram(new,size)[:12]
        x,y=map(list,zip(*top_n_bigrams))
        sns.barplot(x=y,y=x,ax=ax,color='blue')
        fig.suptitle("Common {}-grams in selected text".format(size))
        if self.module_R is None:
            plt.show()
        else:
            self.module_R.write("ABOUT {}-GRAMS".format(size))
            self.module_R.pyplot(fig)
        plt.close()
    
    def statistics_information(self):
        # time_post,comment_post,num_like,num_subcomments,target
        print(self.mode,self.type)
        if self.mode == "YOUTUBE" and (self.type == "myfile" or self.type == "CRAWL"):
            columns = ["time_post","num_like","num_subcomments"]
        else:
            columns = ["time_post"]
        fig,ax =  plt.subplots(len(columns), sharex='col', sharey='row')
        colors = {
            "0" : "red",
            "1" : "green",
            "2" : "blue"
        }
        if len(columns) != 1:
            for i in range(len(columns)):
                columns_lst = self.df[columns[i]].to_list()
                print(columns_lst)
                ax[i].hist(columns_lst,color = colors[str(i)])
                ax[i].tick_params(bottom=False, labelbottom=False)
                ax[i].set_title("{} | min:{} max:{}".format(columns[i],min(columns_lst),max(columns_lst)))
        else:
            columns_lst = self.df[columns[0]].to_list()
            print(columns_lst)
            ax.hist(columns_lst,color = colors["0"])
            ax.tick_params(bottom=False, labelbottom=False)
            ax.set_title("{} | min:{} max:{}".format(columns[0],min(columns_lst),max(columns_lst)))
        if self.module_R is None:
            plt.show()
        else:
            self.module_R.write("STATISTIC ANOTHER INFORMATION")
            self.module_R.pyplot(fig)
        plt.close()
    
if __name__ == "__main__":
    filename = "myfile_20220409-134028_.csv"
    plot_model = PLOT_MODULE(filename)
    plot_model.statistics_information()
    
        
        
    
        
                
    