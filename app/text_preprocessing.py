import pandas as pd
from collections import Counter
import nltk.corpus
nltk.download('stopwords')
from nltk.corpus import stopwords as STOPWORDS
from typing import List


class TextPreprocessing:
    
    @staticmethod
    def get_counter(lyrics_list:List[str]):
        lst = []
        for lyric in lyrics_list:
            cur_lyrics = lyric.split()
            lst.extend(cur_lyrics)
        return Counter(lst)
    
    @staticmethod
    def remove_stop_words(text:str):
        stopwords = STOPWORDS.words('english')
        return " ".join([word for word in text.split() if word not in (stopwords)])
    
    def clean_lyrics(self, data_frame:pd.DataFrame) -> List[str]:
        lyrics:pd.Series = data_frame['lyrics'].str.lower()
        regex = r"[^a-zA-Z0-9 \n\.]"
        lyrics:pd.Series =lyrics.replace(to_replace=regex, value='', regex=True)
        lyrics:pd.Series = lyrics.map(self.remove_stop_words)
        lyrics = lyrics.tolist()
        return lyrics

    