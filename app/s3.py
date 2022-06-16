# uses boto3 to read files stored on s3
import pandas as pd
import awswrangler as wr


class S3Handler:
    @staticmethod
    def read_from_s3(public_key:str) -> pd.DataFrame:
        '''reads file from s3 to pandas data frame
        arguments: 
            public key: str - public key to file stored on s3'''
        return wr.s3.read_parquet(public_key)
        