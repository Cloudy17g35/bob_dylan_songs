import plotly.express as px
from collections import Counter
from collections import Counter
import pandas as pd
from wordcloud import WordCloud


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
                    yaxis=dict(title= 'Number of songs', 
                               showgrid=False))
    
    return fig


def make_wordcloud(frequency:Counter):
    
    wc: WordCloud = (WordCloud(min_font_size=10, max_font_size=60,
                               width=800, height=500,
                               random_state=1,
                               colormap='rainbow',
                               collocations=False)
                    .generate_from_frequencies(frequency))
    return wc