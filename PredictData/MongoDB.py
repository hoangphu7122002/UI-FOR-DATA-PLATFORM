import pymongo
from pymongo import MongoClient
import pandas as pd

# cluster = MongoClient('mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# db = cluster["youtube_crawling"]

# collection = db["test"]

# post = {"_id" : 1,"name" : "TIM","Score" : 5}

# collection.insert_one(post)
# print(post)

class MongoDB(object): 
    def __init__(self,ip_address,ext = "YOUTUBE"):
        self.ip_address = ip_address
        self.cluster = MongoClient(ip_address)
        if ext == "YOUTUBE":
            self.db = self.cluster["youtube_crawling"]
        elif ext == "TRAVELOKA":
            self.db = self.cluster["traveloka_crawling"]
        else:
            self.db = self.cluster["shopee_crawling"]
    
    def createDb(self,df,filename):
        
        if filename.split('.')[0] in self.db.list_collection_names():
            print("collection exist")
        else:
            collection = self.db[filename.split('.')[0]]
            if 'Unnamed: 0' in df.columns.to_list():
                df = df.drop('Unnamed: 0', 1)
            mylist = []
            for i,row in df.iterrows():
                mylist.append(row.to_dict())
            
            collection.insert_many(mylist)

    def searchDB(self,name_db):
        if name_db in self.listDB():
            return self.cluster[name_db]
        print("not exist")
        return None
    
    def listDB(self):
        return self.db.list_database_names()
        
    def query_collection(self,name_db,key):
        pass

    def convert_collectionDB(self,name_collection):
        pass
    
    def query_one_collection(self,filename):
        collection = self.db[filename.split('.')[0]]
        ele = collection.find_one()
        return ele
        
    def drop_collection(self,filename): 
        collection = self.db[filename.split('.')[0]]
        collection.drop()
        
    #for clean_data
    #add function to choose connect conlum_index
    def sort_follow_columns(self,filename):
        key_lst = self.get_key_of_collection(filename)
        collection = self.db[filename.split('.')[0]]
        
        key_idx = 1
        sorted_collection = collection.find().sort(key_lst[key_idx])
        for i,record in enumerate(sorted_collection):
            if i == 5:
                break
            print(record)
        
    def get_key_of_collection(self,filename):
        ele = self.query_one_collection(filename)
        return list(ele.keys())
        
if __name__ == "__main__":
    createDB = MongoDB('mongodb+srv://hoangphu7122002:071202@cluster0.obabt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    df = pd.read_csv("myfile_20220407-120252_.csv")
    createDB.createDbYtc(df,"myfile_20220407-120252_.csv")
    
    print(createDB.get_key_of_collection("myfile_20220407-120252_.csv"))
    createDB.sort_follow_columns("myfile_20220407-120252_.csv")
    # print(df.head(5))
        