import streamlit as st
import pandas as pd
import numpy as np
import time
import os 
import base64

st.set_page_config(layout="wide")

st.title('DataDIY')

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


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


tcol1, tcol2, tcol3,tcol4 = st.beta_columns((2,2,1,1))
col1_sub1, col1_sub2, col1_sub3, col1_sub4, col1_sub5, col1_sub6 = st.beta_columns(6)
bcol1, bcol2, bcol3 = st.beta_columns(3)

file1 = tcol1.file_uploader('Upload File 1')

if file1:
    df1 = pd.read_csv(file1)

    col_list_1 = list()

    for c in df1:
        col_list_1.append(c)

    selected_col_df1 = tcol1.multiselect('Select Columns to use [File 1]', col_list_1)

    if selected_col_df1:
        df1_1 = df1[selected_col_df1]
    else:
        selected_col_df1 = col_list_1
        df1_1 = df1[selected_col_df1]

    #=================================



    col_list_2 = list()

    for c in df1_1:
        col_list_2.append(c)

    selected_col_df1_1_null = col1_sub1.multiselect('Select Columns to remove NULL [File 1]', col_list_2)
    if selected_col_df1_1_null:

        pass
    else:
        selected_col_df1_1_null = selected_col_df1


    if col1_sub1.checkbox('Remove NaN rows'):
        df1_1 = df1_1.dropna(subset=selected_col_df1_1_null)

    #=================================

    selected_col_df1_1_replace = col1_sub2.multiselect('Select Columns to replace NULL values [File 1]', col_list_2)

    if selected_col_df1_1_replace:
        pass
    else:
        selected_col_df1_1_replace = selected_col_df1

    replace_null_f1 = col1_sub2.radio('Replace NULL with [File 1]:', ('No action','0','Mean', 'Median'))

    if replace_null_f1 == 'No action':
        pass
    if replace_null_f1 == '0':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(0)
    if replace_null_f1 == 'Mean':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(df1_1.mean())
    if replace_null_f1 == 'Median':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(df1_1.median())


    bcol1.write(df1_1)
    bcol1.write(df1_1.shape)


    if bcol1.button('Download [File 1] as CSV'):
        tmp_download_link_file_1 = download_link(df1_1, 'file_1.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link_file_1, unsafe_allow_html=True)


    #=================================



###FILE 2####

file2 = tcol2.file_uploader('Upload File 2')

if file2:
    df2 = pd.read_csv(file2)

    col_list_3 = list()


    for c in df2:
        col_list_3.append(c)

    selected_col_df2 = tcol2.multiselect('Select Columns to use [File 2]', col_list_3)

    if selected_col_df2:
        df2_1 = df2[selected_col_df2]
    else:
        selected_col_df2 = col_list_3
        df2_1 = df2[selected_col_df2]

    #=================================

    col_list_4 = list()

    for c in df2_1:
        col_list_4.append(c)

    selected_col_df2_1_null = col1_sub3.multiselect('Select Columns to remove NULL [File 2]', col_list_4)
    if selected_col_df2_1_null:
        pass
    else:
        selected_col_df2_1_null = selected_col_df2

    if col1_sub3.checkbox('Remove NaN rows [File 2]'):
        df2_1 = df2_1.dropna(subset=selected_col_df2_1_null)



    #=================================

	
    selected_col_df2_1_replace = col1_sub4.multiselect('Select Columns to replace NULL values [File 2]', col_list_4)

    if selected_col_df2_1_replace:
        pass
    else:
        selected_col_df2_1_replace = selected_col_df2

    replace_null_f2 = col1_sub4.radio('Replace NULL with [File 2]:', ('No action', '0','Mean', 'Median'))

    if replace_null_f2 == 'No action':
        pass
    if replace_null_f2 == '0':
        df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].fillna(0)
    if replace_null_f2 == 'Mean':
        df2_1[selected_col_df2_1_replace] = df2_1.fillna(df2_1[selected_col_df2_1_replace].mean())
    if replace_null_f2 == 'Median':
        df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].fillna(df2_1.median())


    bcol2.write(df2_1)
    bcol2.write(df2_1.shape)

    if bcol2.button('Download [File 2] as CSV'):
        tmp_download_link_file_2 = download_link(df2_1, 'file_2.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link_file_2, unsafe_allow_html=True)



###FILE MERGE####

try:
    if (df1_1, df2_1) is not None:
        tcol3.header('Join Dataframe')
        key1 = tcol3.selectbox('[File 1] Column',col_list_2)
        key2 = tcol3.selectbox('[File 2] Column',col_list_4)

        join_type = tcol3.selectbox('Type of Join',['inner','outer','right'])

        if tcol3.button('Execute Join'):
            df_merge = pd.merge(df1_1, df2_1, how=join_type, on=[key1, key2])
            bcol3.write(df_merge)
            tmp_download_link_file_merge = download_link(df_merge, 'file_merge.csv', 'Click here to download your data!')
            tcol3.markdown(tmp_download_link_file_merge, unsafe_allow_html=True)


        tcol4.header('Append DataFrame')

        if tcol4.button('Execute Append'):
            df_append = df1_1.append(df2_1, ignore_index=True, sort=False)
            bcol3.write(df_append)
            tmp_download_link_file_append = download_link(df_append, 'file_append.csv', 'Click here to download your data!')
            tcol4.markdown(tmp_download_link_file_append, unsafe_allow_html=True)


except:
    pass
