import logging
import pandas as pd
import pickle
import nltk
import os

from app import app

class PersuasionModel(object):
    def _preprocess_input(self, input_df):
        transcript = input_df['transcript']

        vec_url = os.path.join(app.config['SITE_ROOT'], "app/models", "count_vectorizer.sav")
        vec = pickle.load(open(vec_url, 'rb'))
        vec.fit(transcript)
        features_df = pd.DataFrame(vec.transform(
            transcript).toarray(), columns=vec.get_feature_names())

        return features_df

    def get_persuasion_score(self, input_df):
        preprocessed_input_df = self._preprocess_input(input_df)
        
        model_url = os.path.join(app.config['SITE_ROOT'], "app/models", "persuasion_model.sav")
        persuasion_model = pickle.load(open(model_url, 'rb'))

        persuasion_score = persuasion_model.predict_proba(preprocessed_input_df)[:, 1]
        return persuasion_score[0]

persuasion_model = PersuasionModel()