import streamlit as st
from wordcloud import WordCloud, STOPWORDS
from text_descriptions import TextDescription
import pandas as pd
import plotly.express as px
from collections import Counter
from s3 import S3Handler
from typing import List
import nltk.corpus
nltk.download('stopwords')
from nltk.corpus import stopwords as STOPWORDS
WORDCLOUD_FILE = 'wordcloud.png'
PUBLIC_KEY = 's3://bob-dylan-songs/dylan_songs.parquet'


def plotly_bar_chart(data_frame:pd.DataFrame):
    count_values:pd.Series = data_frame['release_year'].value_counts().sort_index()
    fig = px.bar(x=count_values.index, 
                 y=count_values.values)

    fig.update_layout(font=dict(family='Lato', size=18, color='white'),
                    title=dict(text='<b>Bob Dylan songs in years 1961- 2020<b>',
                            font=dict(size=30), x=.5),
                    paper_bgcolor= 'black', plot_bgcolor='black',
                    xaxis = dict(title='Year of release', 
                                 showgrid=False),
                    yaxis=dict(title= 'number_of_songs', 
                               showgrid=False))
    
    return fig
def get_selected_album_from_user(options:List[str]):
    '''takes user input as an input using
    streamlit''' 
    pass


def make_wordcloud(frequency:Counter):
    
    wc: WordCloud = (WordCloud(min_font_size=10, max_font_size=60,
                               width=800, height=500,
                               random_state=1,
                               colormap='rainbow',
                               collocations=False)
                    .generate_from_frequencies(frequency))
    return wc


def get_counter(lyrics_list):
    lst = []
    for lyric in lyrics_list:
        cur_lyrics = lyric.split()
        lst.extend(cur_lyrics)
    return Counter(lst)

    
def remove_stop_words(text:str):
    stopwords = STOPWORDS.words('english')
    return " ".join([word for word in text.split() if word not in (stopwords)])


def clean_lyrics(data_frame:pd.DataFrame):
    lyrics:pd.Series = data_frame['lyrics'].str.lower()
    regex = r"[^a-zA-Z0-9 \n\.]"
    lyrics:pd.Series =lyrics.replace(to_replace=regex, value='', regex=True)
    lyrics:pd.Series = lyrics.map(remove_stop_words)
    lyrics = lyrics.tolist()
    return lyrics
    
    
if __name__ == '__main__':
    st.write(TextDescription.HEADER.value, 
             unsafe_allow_html=True)
    st.image(TextDescription.PICTURE.value)
    st.write(TextDescription.DESCRIPTION.value,
             unsafe_allow_html=True)
    df:pd.DataFrame = S3Handler.read_from_s3(PUBLIC_KEY)
    df_copy:pd.DataFrame = df.copy()
    st.write(TextDescription.DATASET.value,
             unsafe_allow_html=True)
    st.dataframe(df)
    fig = plotly_bar_chart(df)
    st.write(TextDescription.PLOT_SUBHEADER.value,
             unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.write(TextDescription.ALBUM_SELECTION.value,
             unsafe_allow_html=True)
    options:List[str] = ['select'] + list(df['album'].unique())
    option = st.selectbox('Album name:', options)
    if option != 'select':
        st.write(f'you selected {option}')
        selected_df = df[df['album'] == option]
        st.dataframe(selected_df)
        output_format = 'csv'
        df_to_download:pd.DataFrame = selected_df.to_csv().encode('utf8')
        file_name_for_download:str = f'songs_from_album_{"_".join(option.lower().split())}.csv'
        st.download_button(TextDescription.DOWNLOAD_DATAFRAME.value, 
                           data=df_to_download,
                            file_name=file_name_for_download,
                            mime='text/csv')
    
    st.write(TextDescription.WORDCOUD_DESCRIPTION.value,
             unsafe_allow_html=True)
    years = list(df['release_year'].unique())
    selected_year = st.selectbox('Year:', years)
    if option != 'select':
        df_for_one_year = df[df['release_year'] == selected_year]
        lyrics: list = clean_lyrics(df_for_one_year)
        lyrics_counter:Counter = get_counter(lyrics)
        wc:WordCloud = make_wordcloud(lyrics_counter).to_file('wordcloud.png')
        # wordcloud save as image in the background
        st.image(WORDCLOUD_FILE)
        with open(WORDCLOUD_FILE, 'rb') as file:
            st.download_button(
                label=TextDescription.DOWLOAD_WORDCLOUD.value,
                data=file,
                file_name=WORDCLOUD_FILE,
                mime='image/png'
            )
        