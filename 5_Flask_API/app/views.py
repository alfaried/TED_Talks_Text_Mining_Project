import json
import logging

from flask import request, Response
from flask.views import MethodView

from app import app
from app.controllers.persuasion_model import persuasion_model


# Helper Function
def register_api():
    app.add_url_rule(
        '/api/persuasion-score', view_func=PersuasionScore.as_view('persuasion-score'))  # POST

class PersuasionScore(MethodView):

    def post(self):
        input_file = request.files.get('input')

        logging.info(input_file)
        if not input_file:
            return json.dumps({'error': 'no file uploaded'})

        logging.info('Retrieving persuasion score for {}'.format(input_file))

        persuasion_score = persuasion_model.get_persuasion_score(input_file)
        logging.info(persuasion_score)

        # get persuasion score

        logging.info('Retrieving topic for {}'.format(input_file))

        # get topic from LDA

        logging.info(
            'Retrieving transcript with higher score for {}'.format(input_file))

        # get more persuasive transcript

        res = {}
        res['persuasion_score'] = 0.123
        return json.dumps(res)

register_api()