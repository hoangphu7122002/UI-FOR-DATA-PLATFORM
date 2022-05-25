import pandas as pd
import json

with open("data_file.json", "r") as read_file:
   data = json.load(read_file)
   
log_likelihood = data['log_likelihood']
log_prior = data['log_prior']
   
def predict(sentence):
   print(sentence)
   tweet = sentence.strip().split()

   res = 0

   for word in tweet:
        if word in log_likelihood:
           res += log_likelihood[word]    

   res += log_prior
   if res >= 0:
       return 1
   return 0
    
def load_csv_and_predict(filename,mode = 0):
   if mode == 0:
      df = pd.read_csv(filename)
   else:
      df = filename
   if 'Unamed : 0' in df.columns.to_list():
      df = df.drop('Unamed : 0',1)
   if 'emotion' in df.columns.to_list():
      df = df.drop('emotion',1)
   df = df.dropna()
   df["target"] = df["comment_post"].apply(predict)
   # df.to_csv(filename)
   return df

if __name__ == "__main__":
   filename = "myfile_20220409-134028_.csv"
   load_csv_and_predict(filename)