'''this module contains text 
descrpitons for applications'''
from enum import Enum


class TextDescription(Enum):
    
    HEADER = """<h1 style='text-align: center;
color: blue;'>Bob Dylan Songs App</h1>"""

    IMAGE = 'picture.png'

    DESCRIPTION = """<b>DESCRIPTION</b>

This app enables you to see Bob Dylan songs distribution by year, 
download dataset for particular album and make cloud of words for particular year

<b>Content</b>:

There are 4 columns:

* release_year - year when song was released first time,
* album - name of the album where track occurs,
* title - title of the song,
* lyrics - lyrics of the track 

<b>Acknowledgements</b>:

contains only songs that Bob Dylan himself has 
written and published. There's many songs that Bob Dylan 
only covered so I didn't include them. 
For instance album <i>World Gone Wrong</i> contains 
only old folks songs.

<b>Inspiration</b>:

I'm great Bob Dylan fan. I listen to his songs almost every
day from many years. 
I also play them and sing them so now 
I decided to make dataset and play with them on this app as well. """
    
    PICTURE = 'picture.png'
    
    DATASET = '<b>Dataset:</b>'
    
    PLOT_SUBHEADER = """<h1 style='text-align: center;
color: blue;'>SONGS DISTRIBUTION BY YEARS</h1>"""
    
    ALBUM_SELECTION = 'Select album: '
    
    DOWNLOAD_DATAFRAME = 'DOWNLOAD YOUR DATAFRAME'
    
    WORDCOUD_DESCRIPTION = """If you want to generate wordcloud for particular year, select 
this year on the slider, wordcloud will be generated 
automatically"""
    DOWLOAD_WORDCLOUD = 'DOWNLOAD YOUR WORDCLOUD'

