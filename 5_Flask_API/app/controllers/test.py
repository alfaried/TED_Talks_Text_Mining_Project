import pandas as pd
import nltk
import pickle 

def _preprocess_input(input_df):
    transcript = input_df['transcript']

    vec = pickle.load(open('../models/count_vectorizer.sav', 'rb'))
    vec.fit(transcript)
    features_df = pd.DataFrame(vec.transform(transcript).toarray(), columns=vec.get_feature_names())

    return features_df

def _get_persuasion_score(input_df):
    persuasion_model = pickle.load(open('../models/persuasion_model.sav', 'rb'))
    y_pred_proba = persuasion_model.predict_proba(input_df)[:, 1]
    return y_pred_proba

def get_tag():
    input_df = pd.read_csv('../input.csv')
    preprocessed_input = _preprocess_input(input_df)
    persuasion_score = _get_persuasion_score(preprocessed_input)
    print(persuasion_score)

get_tag()
