import logging
import pandas as pd

from app import app
from app.models.LDA_Module import Setup

class LDAModel(object):
    def _preprocess_input(self, input_df):
        transcript = input_df['transcript'][0]

        file_path = app.config['UPLOAD_FOLDER'] + "transcript.txt"
        text_file = open(file_path, "w")
        text_file.write(transcript)
        text_file.close()

        mallet_path = '/Library/NLTK/mallet/mallet-2.0.8/bin/mallet'
        result_hash = Setup.upload_transcript(file_path, mallet_path)
        
        return result_hash

    def get_related_transcripts(self, input_df):
        result_hash = self._preprocess_input(input_df)
        
        return result_hash
        
lda_model = LDAModel()