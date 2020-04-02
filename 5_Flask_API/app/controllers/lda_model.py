import logging
import pandas as pd

from app import app
from app.models.LDA_Module import Setup


class LDAModel(object):
    def _preprocess_input(self, input_df):
        transcript = input_df['transcript'][0]

        text_file = open("transcript.txt", "w")
        text_file.write(transcript)
        text_file.close()

        mallet_path = '/Users/Junxiang/mallet-2.0.8/bin/mallet'
        Setup.auto_setup(mallet_path)

        return None

    def get_related_transcripts(self, input_df):
        self._preprocess_input(input_df)
        
        return None
        
lda_model = LDAModel()