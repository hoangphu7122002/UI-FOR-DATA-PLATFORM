import streamlit as st
from streamlit.legacy_caching.hashing import _CodeHasher
import pandas as pd 
import numpy as np
from streamlit.scriptrunner import add_script_run_ctx as get_report_ctx
from streamlit.server.server import Server
import hydralit_components as hc

from PredictData import streamlit_predict_emotion
from CollectData import streamlit_crawl_data
from CleanData import streamlit_clean_data
from VisualizeData import streamlit_visualize_data
from end_to_end_streamlit import end_to_end_process
import test_pymongo
import processing_db

menu_data = [
    {'label':"YOUTUBE"},
    {'label':"SHOPEE"},
    {'label':"TRAVELOKA"},
    {'label':"MONGODB"},
    {'label':"SQLITE"}
]

class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

def _get_session():
    session_id = get_report_ctx().streamlit_script_run_ctx.session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state
    
def page_crawling(state):
    menu_id = hc.nav_bar(menu_definition=menu_data)
    if menu_id == "YOUTUBE":
        streamlit_crawl_data.YoutubeCrawling_V1()
    elif menu_id == "SHOPEE":
        streamlit_crawl_data.ShopeeCrawling()
    elif menu_id == "TRAVELOKA":
        streamlit_crawl_data.TravelokaCrawling()
    elif menu_id == "MONGODB":
        test_pymongo.collect_mongoDB()
    else:
        processing_db.collect_sqlite()
        
def page_dashboard(state):
    st.header(":mag_right: DATA COLLECTION")
    st.subheader("**This site is for collect data from Youtube**")
    # st.subheader("**YOUTUBE CRAWL DATA INSTRUCTION** ")
    st.write(":point_right: Copy your youtube video's url then paste to the **INPUT YOUTUBE URL** field.")
    st.write(":point_right: Then type the number of scroll that you want the tool to scroll.")
    st.write(":point_right: If you want to save your data to mongoDB through the tool, choose **Y** option in the **SAVE MONGO_DB (Y/N)** field, otherwise choose **N**")
    st.write(":point_right: If you want to save your data to SQLITE through the tool, choose **Y** option in the **SAVE MONGO_DB (Y/N)** field, otherwise choose **N**")
    st.write(":arrow_down: User can download file through the **Click Here!!!** option")
    st.image("dashboard/collect.png")
    st.write("**:exclamation::exclamation::exclamation:More over, we are going to develop this tool for analysis on 2 more page: Shopee and Travelkola. But sometimes bugs still appear because our code is not compatible with these page's source code.**")
    # st.write("**Hơn nữa chúng em vẫn đang định phát triển tools ở những trang web khác như là Shopee và Travelkola nhưng vẫn chưa hoàn thiện do là code chưa phù hợp với mã nguồn của những trang web ấy.**")
    # st.image("crawl_data_utube.png",width=350)
    st.write("--")
    st.subheader(":bulb: Advantage of MongoDB and SQLITE for the tool")
    st.write("When user chooses to save the data file on **MongoDB** or **SQLITE**, the data file will be stored to these DB. If the user want to do another process such as **DATA PROCESSING**, user can download these cleaned data file as input from **MONGODB** tab or **SQLITE** tab in each section of the tool. (Some section hasn't have these tab yet).")

    st.markdown("--")

    st.header(":hourglass_flowing_sand: DATA PROCESSING")
    st.subheader("This section cleans data from the file, then chooses 3 columns user_name, time_post, comment_post to create a new data file begin with CLEAN.")
    st.write(":one: Upload your .csv file from your computer through **Browse files** button.")
    st.write(":two: Then choose to save on MongoDB or not.")
    st.write(":three: Then choose to save on SQLITE or not.")
    st.write(":four: Finally click in the **PROCESSING** button.")
    st.write(":five: After processing, You can download the file through the **CLICK HERE** option")
    st.image("dashboard/processing.png")

    st.markdown("--")

    st.header(":bar_chart: DATA ANALYSIS")
    st.subheader("This section has 2 tabs: PREDICT EMOTION and VISUALIZE.")
    st.write(":small_blue_diamond: **PREDICT EMOTION** This tab will predict your data file base on 2 models: Naive Bayes and Bert")
    st.write(":zap: First, you need to upload your data file which is cleaned.")
    st.write(":zap: Second, choosing the model you want.")
    st.write(":zap: Then choose to save your output data file after process to MongoDB or SQLITE or not.")
    st.write(":arrow_down: After clicking the **process** button, the tool will predict your data file base on the model you have chosen then store the data to a new file begin with **PREDICT**. You can download this file such as **CLEAN** file")
    st.image("dashboard/predict.png")
    st.write(":small_blue_diamond: **VISUALIZE** This tab will visualize your data file through chart.")
    st.write(":chart_with_upwards_trend: Just upload your data file then let the tool do the remaining!")
    st.image("dashboard/visualize.png")

    st.markdown("--")

    st.header(":triangular_flag_on_post: END TO END PROCESSING")
    st.subheader("This section will do all function from the begining to the end in order: CLEAN DATA - PREDICT DATA - VISUALIZE")
    st.write(":low_brightness: You just need to upload your raw data file then the tool will **clean** it then **predict** and finally **visualize** the result data.")
    st.image("dashboard/endtoend.png")

    st.markdown("--")

    st.header(":hourglass: DATA STREAMING")

def page_clean(state):
    # st.write("CLEAN DATA")
    menu_clean = [
        {'label':"CSV"},
        {'label':"MONGODB"},
        {'label':"SQLITE"},
    ]
    menu_id = hc.nav_bar(menu_definition=menu_clean)
    if menu_id == "CSV":
        streamlit_clean_data.processingCSV()
    elif menu_id == "MONGODB":
        streamlit_clean_data.processingMongoDB()
    else:
        processing_db.processing_sqlite_db()

def page_output(state):
    menu_clean = [
        {'label':"PREDICT EMOTION"},
        {'label':"VISUALIZE"}
    ]
    menu_id = hc.nav_bar(menu_definition=menu_clean)
    if menu_id == "PREDICT EMOTION":
        streamlit_predict_emotion.predict()
    else:
        streamlit_visualize_data.visualizeDT()

def page_streaming_data(state):
    st.title("STREAMING DATA")
    st.write("=============COMING SOON=============")
    pass
    
def page_end_to_end(state):
    menu_end_to_end = [
        {'label':"CSV"},
        {'label':"MONGODB"},
        {'label':"SQLITE"}
    ]
    menu_id = hc.nav_bar(menu_definition=menu_end_to_end)
    if menu_id == "CSV":
        end_to_end_process()
    elif menu_id == "MONGODB":
        end_to_end_process(mode="MONGODB")
    else:
        end_to_end_process(mode="TRAVELOKA")
    
def main():
    st.set_page_config(layout = "wide",page_title="server")
    state = _get_state()
    
    pages = {}
    
    pages["DASHBOARD"] = page_dashboard
    pages["DATA COLLECTION"] = page_crawling
    pages["DATA PROCESSING"] = page_clean
    pages["DATA ANALYSIS"] = page_output
    pages["END TO END PROCESSING"] = page_end_to_end
    pages["DATA STREAMING"] = page_streaming_data
    
    st.sidebar.title(":floppy_disk: Dashboard")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))
    
    pages[page](state)
    state.sync()
    
if __name__ == "__main__":
    main()