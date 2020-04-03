import json
import logging
import pandas as pd
from flask import request, Response, jsonify
from flask.views import MethodView

from app import app
from app.controllers.persuasion_model import persuasion_model
from app.controllers.lda_model import lda_model


# Helper Function
def register_api():
    app.add_url_rule(
        '/api/persuasion-score', view_func=PersuasionScore.as_view('persuasion-score'))  # POST

class PersuasionScore(MethodView):

    def post(self):
        input_file = request.files.get('input')
    
        if not input_file:
            return json.dumps({'error': 'no file uploaded'})

        input_df = pd.read_csv(input_file)
        logging.info(input_df)

        logging.info('Retrieving persuasion score for {}'.format(input_df))

        persuasion_score = persuasion_model.get_persuasion_score(input_df)
        logging.info(persuasion_score)

        result_hash = lda_model.get_related_transcripts(input_df)
        related_document_list = result_hash["Related_Documents"]
        topic_theme = result_hash["Topic_Theme"]
        topic_keywords = result_hash["Topic_Keywords"]

        logging.info('Retrieving topic for {}'.format(input_df))
        logging.info('Topic {}'.format(topic_theme))
        logging.info('Topic Keywords {}'.format(topic_keywords))
        logging.info('Related transcripts id {}'.format(related_document_list))

        logging.info(
            'Retrieving transcript with higher score for {}'.format(input_df))
        
        all_df = pd.read_csv(app.config['SITE_ROOT'] + '/app/data/cleaned_dataset_with_persuasion_score.csv')

        all_df = all_df[all_df['id'].isin(related_document_list)]
        logging.info(all_df)
        filtered_df = all_df[all_df['persuasion_score'] > persuasion_score]
        filtered_df = filtered_df.sort_values(by=['persuasion_score'])

        top_persuasive_df = filtered_df[['url', 'persuasion_score']].head()

        res = {'persuasion-score': persuasion_score, 'topic-keywords': topic_keywords.split(', '), 'topic-theme': topic_theme, 'top-5-persuasive-talks': top_persuasive_df.to_dict('records')}
        logging.info(res)
        return jsonify(res)

register_api()