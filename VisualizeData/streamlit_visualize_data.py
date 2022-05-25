from VisualizeData.visualize import *
import pandas as pd
import streamlit as st
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import sys

def visualizeDT():
    st.title("DATA VISUALIZATION")
    # st.markdown("#### UploadDTS ###")  
    # col1,col2 = st.columns(2)
    st.markdown("#### UPLOAD FILE ###")
    df = st.file_uploader("",type = ["csv"])
    
    col1,col2 = st.columns(2)
    
    if df is not None:
        filename = df.name
        df1 = pd.read_csv(df)
        # file_details = {"FILENAME":df.name, "FILETYPE":df.type,
        #                     "FILESIZE":sys.getsizeof(df1), "NUM_COL" : len(df1.columns.to_list()), "NUM_ROW" : len(df1)}
        # st.write(file_details)
        
        # st.write("DATA OVERVIEW")
        # st.dataframe(df1.head(6))
        
        plot_model = PLOT_MODULE(df1,filename,col1,col2)
        #left hide information
        plot_model.show_word_distrib()
        plot_model.plot_average_word_length()
        plot_model.unique_words()
        if 'target' in df1.columns.to_list():
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
        # plot_model.plot_hist_classes()