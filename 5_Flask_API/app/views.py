import json
import logging
import pandas as pd
from flask import request, Response
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

        lda_model.get_related_transcripts(input_df)

        logging.info('Retrieving topic for {}'.format(input_df))

        # get topic from LDA

        logging.info(
            'Retrieving transcript with higher score for {}'.format(input_df))

        # get more persuasive transcript

        res = {}
        res['persuasion_score'] = 0.123
        return json.dumps(res)

register_api()