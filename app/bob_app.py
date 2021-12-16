import streamlit as st
from wordcloud import WordCloud, STOPWORDS

import pandas as pd
import plotly.express as px
from collections import Counter


df = pd.read_csv('dylan_songs.csv')
# this copy will be useful further
df_copy = pd.read_csv('dylan_songs_copy.csv')

st.markdown("<h1 style='text-align: center; "
            "color: blue;'>Bob Dylan Songs"
            "</h1>", unsafe_allow_html=True)

st.image('picture.png')

st.write("""Decription of dataset:

Context:
 
This dataset contains songs from years between 1961 to 2020 
written by Bob Dylan.

Content:

There are 4 columns:

* release_year - year when song was released first time,
* album - name of the album where track occurs,
* title - title of the song,
* lyrics - lyrics of the track 

Acknowledgements:

contains only songs that Bob Dylan himself has 
written and published. There's many songs that Bob Dylan 
only covered so I didn't include them because he's not the 
original author. For instance album World Gone Wrong contains 
only old folks songs.

Inspiration:
 
 I'm great Bob Dylan fan. I listen to his songs almost every
 day from many years. 
 I also play them and sing them so now 
 I decided to make dataset and play with them on this app as well. 
""")


st.write('Dataset:')
st.dataframe(df)


count_values = df['release_year'].value_counts().sort_index()

fig = px.bar(x=count_values.index, y=count_values.values)

st.subheader('SONGS DISTRIBUTION BY YEARS')

fig.update_layout(font=dict(family='Lato', size=18, color='white'),
                  title=dict(text='<b>Bob Dylan songs in years 1961- 2020<b>',
                           font=dict(size=30), x=.5),
                  paper_bgcolor= 'black', plot_bgcolor='black',
                 xaxis = dict(title='Year of release', showgrid=False),
                 yaxis=dict(title= 'number_of_songs', showgrid=False))

st.plotly_chart(fig)

st.write('Select album: ')

# option might be select or unique album from dataset
options = ['select'] + list(df['album'].unique)
option = st.selectbox('Album name:', options)


if option != 'select':

    st.write(f'you selected {option}')
    selected_df = df[df['album'] == option]
    st.dataframe(selected_df)
    df_to_download = selected_df.to_csv().encode('utf8')

    st.download_button('DOWNLOAD YOUR DATAFRAME', data=df_to_download,
                       file_name=f'songs_from_album_{"_".join(word for word in option.split())}.csv,
                       mime='text/csv')


st.write("""If you want to generate wordcloud for particular year, select 
this year on the slider, wordcloud will be generated 
automatically, if there's no songs for this year
announcement will occur""")


def make_wordcloud(year:int):
    """this function takes integer(year when song was published)
    returns freq_table of words from songs from based on this particular year

    arguments: year: int

    returns: frequency table: dict"""

    data_frame_for_year = df_copy[df_copy['release_year'] == year]
    clean = []

    for lyric in data_frame_for_year['lyrics']:

        words = lyric.split()

        for word in words:

            word = (word.strip().replace('’', "'").replace(' ', '').
                    replace(',', '').replace('"', '').replace('”', '')
                    .replace(";", "").replace('.',''))

            if word not in STOPWORDS:
                clean.append(word)

    frequency = Counter(clean)

    wc: WordCloud = (WordCloud(min_font_size=10, max_font_size=60, width=800, height=500,
                               random_state=1,
                               colormap='rainbow',
                               collocations=False)
                    .generate_from_frequencies(frequency))
    return wc


year: int = st.slider('choose year:', min_value=1961, max_value=2020)

unique_years: set = set(df['release_year'].values)

if year in unique_years:
    cloud = make_wordcloud(year).to_file('download.png')
    st.image('download.png')

    with open('download.png', 'rb') as file:
        st.download_button(
            label='DOWNLOAD ME!',
            data=file,
            file_name='download.png',
            mime='image/png'
        )
else:
    st.write(f"there's no songs for this year: {year}")
