from s3 import S3Handler
import pandas as pd
PUBLIC_KEY = 's3://bob-dylan-songs/dylan_songs.parquet'


s3_handler = S3Handler()
class TestS3Handler:
    def test_dataframe_from_s3(self):
        df = s3_handler.read_from_s3(PUBLIC_KEY)
        assert list(df.columns) == ['release_year', 'album', 'title', 'lyrics']
        assert df.shape == (345, 4)
        # there should be no null values
        assert sum(df.isnull().sum().values) == 0
        # should be no duplicates
        assert df[df.duplicated()].empty == True

