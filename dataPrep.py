
from matplotlib.pyplot import xcorr
import streamlit as st
import pandas as pd
import numpy as np
import time
import os 
import base64
from pandas.api.types import is_numeric_dtype
import missingno as msno


uf = st.sidebar.file_uploader('Upload')
if uf:
    df_raw = pd.read_csv(uf)
    st.sidebar.write(df_raw.shape)

selection = st.sidebar.radio('Option',['Keep Original','Remove','Include'])

if uf:    
    # create empty list to get columns of raw dataframe
    col_list_raw = list()
    for col in df_raw:
        col_list_raw.append(col)

    if selection != 'Keep Original':
        # create expander for [a]
        choose_col_expander = st.sidebar.expander("Columns to " + selection)
        # create a NEW dataframe based on user selection
        selected_col = choose_col_expander.multiselect('If none selected, all data fields will be retained',col_list_raw)

    if selection == 'Keep Original':
        df_modify = df_raw

    elif (selected_col != []) and (selection == 'Include'):
        df_modify = df_raw[selected_col]        

    elif (selected_col != []) and (selection == 'Remove'):
        df_modify = df_raw.drop(columns=selected_col, axis=1)

    else:
        df_modify = df_raw

    # create column list based on modified dataframe
    #col_list_modify = list()

    #for col in df_modify:
       # col_list_modify.append(col)

    newlist = [x for x in df_modify.columns]

    remove_null = st.sidebar.expander("Remove null rows")
    newcolnull = remove_null.multiselect('tester',newlist)

    if newcolnull != []:
        df_modify = df_modify.dropna(subset=newcolnull)

    st.sidebar.write(df_modify.shape)

@st.cache

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')

# Notify the reader that the data was successfully loaded.
#data_load_state.text("Cache Loaded! (using st.cache)")


#====== DOWNLOAD FILE FUNCTION ======#

def download_link(object_to_download, download_filename, download_link_text):
    
    #Generates a link to download the given object_to_download.

    #object_to_download (str, pd.DataFrame):  The object to be downloaded.
    #download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    #download_link_text (str): Text to display for download link.

    #Examples:
    #download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    #download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

#======================================

st.title('DataPrep')

if uf:
    df = pd.DataFrame()
    for i in df_modify.columns:
        dict = {}
        dict = {'Column':i, 'Dtype': str(df_modify[i].dtype), 'Unique Values': len(df_modify[i].unique()), 'null': sum(df_modify[i].isnull())}
        df = df.append(dict, ignore_index=True)
    st.write(df)

    # crreate missingo chart to display data completeness
    fig = msno.matrix(df_modify)
    fig_copy = fig.get_figure()
    fig_copy.savefig('raw.png', bbox_inches = 'tight')

    # display missingno chart
    st.image('raw.png')


    st.write(df_modify)

    tmp_download_link_file_append = download_link(df_modify, 'df_modify.csv', 'Click here to download your data!')
    st.markdown(tmp_download_link_file_append, unsafe_allow_html=True)

