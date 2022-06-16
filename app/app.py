import streamlit as st
import pandas as pd
from s3 import S3Handler
from text_descriptions import TextDescription
from text_preprocessing import TextPreprocessing
from data_visualizations import plotly_bar_chart, make_wordcloud
from typing import List
from collections import Counter
from wordcloud import WordCloud
WORDCLOUD_FILE = 'wordcloud.png'
PUBLIC_KEY = 's3://bob-dylan-songs/dylan_songs.parquet'


def header_and_description():
    st.write(TextDescription.HEADER.value, 
             unsafe_allow_html=True)
    st.image(TextDescription.PICTURE.value)
    st.write(TextDescription.DESCRIPTION.value,
             unsafe_allow_html=True)


def show_dataset(data_frame:pd.DataFrame):
    st.write(TextDescription.DATASET.value,
             unsafe_allow_html=True)
    st.dataframe(data_frame)


def barchart(data_frame=pd.DataFrame):
    fig = plotly_bar_chart(data_frame)
    st.write(TextDescription.PLOT_SUBHEADER.value,
             unsafe_allow_html=True)
    st.plotly_chart(fig)


def album_selection(data_frame:pd.DataFrame):
        st.write(TextDescription.ALBUM_SELECTION.value,
                unsafe_allow_html=True)
        options:List[str] = ['select'] + list(data_frame['album'].unique())
        option = st.selectbox('Album name:', options)
        if option != 'select':
            st.write(f'you selected {option}')
            selected_df = data_frame[data_frame['album'] == option]
            st.dataframe(selected_df)
            df_to_download:pd.DataFrame = selected_df.to_csv().encode('utf8')
            file_name_for_download:str = f'songs_from_album_{"_".join(option.lower().split())}.csv'
            st.download_button(TextDescription.DOWNLOAD_DATAFRAME.value, 
                            data=df_to_download,
                                file_name=file_name_for_download,
                                mime='text/csv')

   
def wordcloud(data_frame=pd.DataFrame):
        st.write(TextDescription.WORDCLOUD_SUBHEADER.value,
                unsafe_allow_html=True)
        st.write(TextDescription.WORDCOUD_DESCRIPTION.value,
                unsafe_allow_html=True)
        years = list(data_frame['release_year'].unique())
        selected_year = st.selectbox('Year:', years)
        df_for_one_year = data_frame[data_frame['release_year'] == selected_year]
        tp = TextPreprocessing()
        lyrics: list = tp.clean_lyrics(df_for_one_year)
        lyrics_counter:Counter = tp.get_counter(lyrics)
        # wordcloud is saved as image in the background
        wc:WordCloud = make_wordcloud(lyrics_counter).to_file('wordcloud.png')
        st.image(WORDCLOUD_FILE)
        with open(WORDCLOUD_FILE, 'rb') as file:
            st.download_button(
                label=TextDescription.DOWLOAD_WORDCLOUD.value,
                data=file,
                file_name=WORDCLOUD_FILE,
                mime='image/png'
            )


if __name__ == '__main__':
    header_and_description()
    df:pd.DataFrame = S3Handler.read_from_s3(PUBLIC_KEY)
    show_dataset(df)
    barchart(df)
    album_selection(df)
    wordcloud(df)

