from matplotlib.pyplot import xcorr
import streamlit as st
import pandas as pd
import numpy as np
import time
import os 
import base64
from pandas.api.types import is_numeric_dtype
import missingno as msno


st.set_page_config(layout="wide")

st.sidebar.write("1. Upload CSV file (currently CSV only)")
st.sidebar.write("2. Dataframe shows your data real time")
st.sidebar.write("3. Missingno show completeness of data")
st.sidebar.write("4. Data fields to keep")
st.sidebar.write(" -- Keep blank to retain all colums")
st.sidebar.write(" -- Select columns to resize dataframe")
st.sidebar.write("5. Replace null values")
st.sidebar.write(" -- Replace with 0, mean, median")
st.sidebar.write(" -- It will only work for numeric fields")
st.sidebar.write("6. Remove null values")
st.sidebar.write(" -- Keep blank to remove all rows with null")
st.sidebar.write(" -- Select columns to remove null if exist in selected column")
st.sidebar.write("7. Replace values")
st.sidebar.write(" -- Keep blank to replace across all data fields")
st.sidebar.write(" -- Select column to effect change on selected column")
st.sidebar.write("8. Show distribution range")
st.sidebar.write(" -- Only works for numeric values.")
st.sidebar.write(" -- Show distribution of values for exploration")
st.sidebar.write("9. Show unique values")
st.sidebar.write(" -- Show unique values in selected column")
st.sidebar.write("10. Download File")
st.sidebar.write(" -- Export modified file in csv format")


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

st.title('DataDIY')

tcol1, tcol2, tcol3 = st.beta_columns((1,1,1))


def datacleanser():
    
    # create UI container

    uploaded_file = tcol1.file_uploader('Upload CSV File')

    # to show following if 
    if uploaded_file:
        
        # read raw data file
        df_raw = pd.read_csv(uploaded_file)


        ### end of first segment ###
#=================================================================================================================================================================
        
        #create second segment
        #this segment is to hold 3 functions
        
        ## [a] Choose what column to keep
        ## [b] Replace NULL value
        ## [c] Remove NULL value

        # create UI container
        mcol1, mcol2, mcol3 = st.beta_columns((1,1,1))

        # create empty list to get columns of raw dataframe
        col_list_raw = list()
        for col in df_raw:
            col_list_raw.append(col)

        # create expander for [a]
        choose_col_expander = mcol1.beta_expander("Data fields to keep")

        # create a NEW dataframe based on user selection
        selected_col = choose_col_expander.multiselect('Select data fields to keep. If none selection, all data fields will be retained',col_list_raw)
        if selected_col:
            df_modify = df_raw[selected_col]
        else:
            selected_col = col_list_raw
            df_modify = df_raw[selected_col]

        # create column list based on modified dataframe
        col_list_modify = list()

        for col in df_modify:
            col_list_modify.append(col)

#=================================================================================================================================================================
        # create expander for [b]
        replace_null_expander = mcol1.beta_expander("Replace NULL values")

        selected_col_replace = replace_null_expander.multiselect('Select Columns to replace NULL values [File 1]', col_list_modify)

        if selected_col_replace:
            pass
        else:
            selected_col_replace = col_list_modify

        replace_null = replace_null_expander.radio('Replace NULL:', ('No action','0','Mean', 'Median'))

        if replace_null == 'No action':
            pass
        if replace_null == '0':
            df_modify[selected_col_replace] = df_modify[selected_col_replace].fillna(0)
        if replace_null == 'Mean':
            df_modify[selected_col_replace] = df_modify[selected_col_replace].fillna(df_modify[selected_col_replace].mean())
        if replace_null == 'Median':
            df_modify[selected_col_replace] = df_modify[selected_col_replace].fillna(df_modify[selected_col_replace].median())

#=================================================================================================================================================================

        # create expander for [c]
        remove_null_expander = mcol1.beta_expander("Remove NULL values")

        selected_col_remove = remove_null_expander.multiselect('Select data fields to have rows removed if NULL. If no selection, all columns will be used', col_list_modify)
        if selected_col_remove:
            pass
        else:
            selected_col_remove = col_list_modify

        if remove_null_expander.checkbox('Remove NULL rows'):
            df_modify = df_modify.dropna(subset=selected_col_remove)

#=================================================================================================================================================================

        ## [d] Replace value
        ## [e] Spare Placeholder
        ## [f] Spare Placeholder

        # create expander for [f]
        replace_value= mcol2.beta_expander("Replace Values")

        selected_col_replace_value = replace_value.multiselect('Select columns to replace', col_list_modify)
        
        old_value= replace_value.text_input('Old Value')
        new_value= replace_value.text_input('New Value')

        if old_value != "" and new_value != "":
            if selected_col_replace_value:
                df_modify[selected_col_replace_value] = df_modify[selected_col_replace_value].replace(old_value, new_value)
                replace_value.write('Values replaced')

            else:
                df_modify = df_modify.replace(old_value,new_value)
                replace_value.write('Values replaced')

        placeholder_1= mcol2.beta_expander("placeholder_1")
        placeholder_2= mcol2.beta_expander("placeholder_2")

#=================================================================================================================================================================

        ## [g] Replace value
        ## [h] Spare Placeholder
        ## [i] Spare Placeholder

        # create expander for [g]
        distribution_expander = mcol3.beta_expander("Show distribution range (for numeric values only)")

        selected_col_distribution = distribution_expander.selectbox('Select data field to display distribution', col_list_modify)

        if selected_col_distribution and is_numeric_dtype(df_modify[selected_col_distribution]):

            distribution_expander.write('Minimum : ' + str(df_modify[selected_col_distribution].min()))
            distribution_expander.write('Maximum : ' + str(df_modify[selected_col_distribution].max()))
            distribution_expander.write('Mean : ' + str(df_modify[selected_col_distribution].mean()))
            distribution_expander.write('Median : ' + str(df_modify[selected_col_distribution].median()))
            distribution_expander.bar_chart(df_modify[selected_col_distribution])
    
        else:
            distribution_expander.write('Invalid column (Non numeric)')

#=================================================================================================================================================================

        # create expander for [h]
        unique_value = mcol3.beta_expander("Show unique values")

        selected_col_unique = unique_value.selectbox('Select data field to show total unique value', col_list_modify)
        
        if selected_col_unique:
            unique_set = set(df_modify[selected_col_unique])
            unique_len = len(unique_set)
            
            unique_value.write('Number of items: ' + str(unique_len))
            unique_value.write(unique_set)

#=================================================================================================================================================================
        
        # create expander for [i]
        download_file = mcol3.beta_expander("Download File")
        if download_file.button('Export csv'):
            x = download_link(df_modify, 'output.csv', 'Click here to download file')
            download_file.markdown(x, unsafe_allow_html=True)

        # display raw dataframe
        tcol2.write("Dataframe")
        tcol2.write(df_modify)

        # crreate missingo chart to display data completeness
        fig = msno.matrix(df_modify)
        fig_copy = fig.get_figure()
        fig_copy.savefig('raw.png', bbox_inches = 'tight')

        # display missingno chart
        tcol3.write('Missingno chart')
        tcol3.image('raw.png')

#=================================================================================================================================================================

datacleanser()


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



