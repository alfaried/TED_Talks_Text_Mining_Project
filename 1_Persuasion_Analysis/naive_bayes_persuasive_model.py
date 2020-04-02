import pandas as pd
from empath import Empath
import ast 
import pickle

df = pd.read_csv('../Processed_Dataset/cleaned_dataset.csv')

lexicon = Empath()
lexicon.create_category("persuasion",["anger","anticipation","disgust","fear","joy","negative","positive","sadness","surprise","trust"])

ratings_list = df["ratings"].tolist()

#Identify all the possible rating types that mentions persuasiveness

persuasive_ratings_counts = []
for i,rating in enumerate(ratings_list):
    rating = ast.literal_eval(rating)
    for categories in rating:
        if categories['name'] == 'Persuasive':
            persuasive_ratings_counts.append({'per_count':categories['count']})
            break
    if len(persuasive_ratings_counts)!=i+1:
        persuasive_ratings_counts.append({'per_count':0})

df["per_count"] = pd.DataFrame(persuasive_ratings_counts)

df["per_count"] = df["per_count"].replace(0,1)

df["count_per_view"] = df["per_count"]/df["views"]

df["count_per_view"].plot(kind='box')

df["normalised_count_per_view"] = (df["count_per_view"]-df["count_per_view"].min())/(df["count_per_view"].max()-df["count_per_view"].min())

t_df = pd.DataFrame()
t_df["transcript"] = df["transcript"]

transcripts = df["transcript"]
scores_list = []

for i,script in enumerate(transcripts):
  lexi_dict = lexicon.analyze(script,categories=["persuasion"],normalize=True)
  scores_list.append(lexi_dict)

t_df["persuasion_score"] = pd.DataFrame(scores_list)

t_df["persuasion_score"].max()

lexicon.create_category("ny_per",["anger","anticipation","disgust","fear","joy","negative","positive","sadness","surprise","trust"], model="nytimes")

ny_score_list = []

for i,script in enumerate(transcripts):
  lexi_dict = lexicon.analyze(script,categories=["ny_per"],normalize=True)
  ny_score_list.append(lexi_dict)

t_df["ny_persuasion_score"] = pd.DataFrame(ny_score_list)

t_df["ny_persuasion_score"].max()

#t_df["ratings"] = df["ratings"]

t_df[t_df["persuasion_score"].max()==t_df["persuasion_score"]]

t_df[t_df["ny_persuasion_score"].max()==t_df["ny_persuasion_score"]]

lexicon.create_category("reddit_per",["anger","anticipation","disgust","fear","joy","negative","positive","sadness","surprise","trust"], model="reddit")

reddit_score_list = []

for i,script in enumerate(transcripts):
  lexi_dict = lexicon.analyze(script,categories=["reddit_per"],normalize=True)
  reddit_score_list.append(lexi_dict)

t_df["reddit_persuasion_score"] = pd.DataFrame(reddit_score_list)

t_df[t_df["reddit_persuasion_score"].max()==t_df["reddit_persuasion_score"]]

per_word_list = ["fear", "sadness", "anger", "disappointment", "guilt", "desperation", "regret", "uncertainty", "emotion", "rage", "hatred", "sorrow", "happiness", "jealousy", "resentment", "worry", "mixed_emotions", "terror", "anguish", "panic", "despair", "sympathy", "anxiousness", "anxiety", "fury", "jealously", "pity", "apprehension", "longing", "determination", "dissapointment", "insecurity", "emotions", "trepidation", "hurt", "elation", "curiousity", "eagerness", "betrayal", "grief", "excitement", "remorse", "dread", "hostility", "malice", "pride", "pain", "contempt", "nervousness", "shock", "concern", "confusion", "curiosity", "irritation", "joy", "helplessness", "fear", "bitterness", "revulsion", "uneasiness", "hatred", "humiliation", "pure_fear", "Fear", "many_emotions", "vulnerability", "hopelessness", "satisfaction", "so_much_anger", "seriousness", "loathing", "denial", "lust", "unease", "unhappiness", "impatience", "certainty", "aggression", "so_many_emotions", "recognition", "hysteria", "calmness", "sincerity", "saddness", "agitation", "wariness", "feeling", "conflicting_emotions", "Shock", "envy", "annoyance", "Anger", "compassion", "pure_terror", "fright", "Worry", "deep_sadness", "madness", "admiration", "raw_emotion"]
per_word_list += ["anger", "apprehension", "anxiety", "elation", "regret", "disgust", "disappointment", "unhappiness", "impatience", "irritation", "fear", "frustration", "dread", "nervousness", "bewilderment", "indignation", "revulsion", "bitterness", "anguish", "wariness", "feeling", "pessimism", "puzzlement", "incredulity", "unease", "emotion", "feelings", "insecurity", "weariness", "satisfaction", "exasperation", "euphoria", "resentment", "discomfort", "trepidation", "bafflement", "uneasiness", "shock", "helplessness", "disbelief", "annoyance", "grief", "despair", "joy", "hysteria", "cynicism", "exhilaration", "outrage", "desperation", "fury", "remorse", "optimism", "discouragement", "apathy", "sadness", "panic", "ambivalence", "ill_will", "perplexity", "rancor", "jubilation", "astonishment", "distress", "worry", "sentiment", "sympathy", "disapproval", "hurt", "dissatisfaction", "dismay", "distrust", "rage", "glee", "agitation", "fatalism", "sense", "enthusiasm", "inevitability", "hesitancy", "hostility", "equanimity", "deep_sense", "indifference", "emotions", "anxieties", "skepticism", "negativity", "hopelessness", "empathy", "amazement", "strong_emotions", "disillusionment", "growing_sense", "disquiet", "frustrations", "bravado", "admiration", "powerlessness", "awkwardness", "affection"]
per_word_list += ["anger", "sadness", "fear", "uneasiness", "strong_emotion", "feeling", "regret", "disgust", "indifference", "sorrow", "jealousy", "negative_emotion", "negative_feeling", "joy", "emotion", "helplessness", "indignation", "negative_emotions", "frustration", "elation", "pity", "intense_feelings", "revulsion", "unease", "anguish", "other_emotion", "only_emotion", "dissatisfaction", "feelings", "disappointment", "catharsis", "strong_emotions", "excitement", "other_emotions", "overwhelming_sense", "positive_emotions", "apprehension", "ambivalence", "emotions", "negative_feelings", "fears", "happiness", "hopelessness", "satisfaction", "longing", "good_feelings", "grief", "overwhelming_feeling", "powerlessness", "hopefulness", "embarassment", "negativity", "saddness", "desperation", "own_fear", "giddiness", "trepidation", "disapproval", "deep_sense", "emotional_response", "sympathy", "bad_feelings", "desire", "other_feelings", "such_feelings", "deep_sadness", "resentment", "vague_sense", "dread", "true_feeling", "dissapointment", "inadequacy", "realisation", "deep_feeling", "righteous_anger", "anxiousness", "revel", "discontent", "anger/frustration", "natural_response", "loneliness", "dejection", "more_sadness", "just_anger", "insecurity", "such_anger", "deep_fear", "worry", "self_hatred", "self_loathing", "intense_feeling", "worthlessness", "sympathy", "powerful_emotions", "positive_feelings", "jubilation", "hurt", "self_doubt"]

per_word_list = list(set(per_word_list))

cleaned_word_list = []
cleaned_multiple_word_list = []

for word in per_word_list:
  if "_" in word:
    new_word = word.replace("_"," ")
    cleaned_multiple_word_list.append(new_word)
  else:
    new_word = word
    cleaned_word_list.append(new_word)

tokenised_transcript_list = [transcript.split(" ") for transcript in transcripts]

tokenised_terms_list = []

for d in tokenised_transcript_list:
  tokenised_terms_list.append(list(set(d)))

final_df = pd.DataFrame()
final_df["transcript"] = df["transcript"]

#One-hot encoding for single words

for word in cleaned_word_list:
  column_list = []
  for transcript in tokenised_terms_list:
    column_dict = {}
    column_dict[word] = 0
    if word in transcript:
      column_dict[word] += 1
    column_list.append(column_dict)
  
  final_df[word] = pd.DataFrame(column_list)

#One hot encoding for multiple words

for words in cleaned_multiple_word_list:
  column_list = []
  for transcript in transcripts:
    column_dict = {}
    column_dict[words] = 0
    if words in transcript:
      column_dict[words] += 1
    column_list.append(column_dict)

  final_df[words] = pd.DataFrame(column_list)

def noramlise_per_score(scores,str_val):
  new_scores = []
  max_score = max(scores)
  min_score = min(scores)
  for score in scores:
    norm_score = (score-min_score)/(max_score-min_score)
    new_scores.append({str_val:norm_score})

  return new_scores

norm_per_score = noramlise_per_score(t_df["persuasion_score"],"norm_persuasion_score")
ny_norm_per_score = noramlise_per_score(t_df["ny_persuasion_score"],"norm_ny_persuasion_score")
reddit_norm_per_score = noramlise_per_score(t_df["reddit_persuasion_score"],"norm_reddit_persuasion_score")

t_df["norm_persuasion_score"] = pd.DataFrame(norm_per_score)
t_df["norm_ny_persuasion_score"] = pd.DataFrame(ny_norm_per_score)
t_df["reddit_ny_persuasion_score"] = pd.DataFrame(reddit_norm_per_score)

t_df["final_per_score"] = (t_df["norm_persuasion_score"] + t_df["norm_ny_persuasion_score"] + t_df["reddit_ny_persuasion_score"]) / 3

final_df["final_per_score"] = t_df["final_per_score"]

feature_col_names = final_df.columns[1:-1]
features_df = final_df[feature_col_names]

final_df["final_per_score"].median()

# Can change score to 0
final_df["binary_score"] = final_df["final_per_score"].apply(lambda score: 1 if score > final_df["final_per_score"].median() else 0)
#final_df["binary_score"] = final_df["final_per_score"].apply(lambda score: 1 if score > 0 else 0)

target_df = pd.DataFrame()
target_df["binary_score"] = final_df["binary_score"]

final_target_df = pd.DataFrame()

prop_vote_persuasive = 0.02
df["normalised_count_per_view"].apply(lambda x: 1 if x > prop_vote_persuasive else 0).value_counts().plot(kind='bar')

(df["normalised_count_per_view"] < 0.01).sum()

final_target_df["normalised_count_per_view"] = df["normalised_count_per_view"].apply(lambda score: 1 if score > prop_vote_persuasive else 0)
#final_target_df["normalised_count_per_view"] = df["normalised_count_per_view"].apply(lambda score: 1 if score > df["normalised_count_per_view"].quantile(.2) else 0)
#final_target_df["normalised_count_per_view"] = df["normalised_count_per_view"].apply(lambda score: 1 if score > 0 else 0)

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import *

X_train, X_test, y_train, y_test = train_test_split(features_df, final_target_df, test_size=0.2)

classifier = MultinomialNB()
classifier.fit(X_train,y_train)

y_pred = classifier.predict_proba(X_test)
y_pred = y_pred[:, 1]
y_pred.shape

import matplotlib.pyplot as plt

plt.hist(y_pred)

from sklearn import metrics

metrics.roc_auc_score(y_test, y_pred)

final_target_df.to_csv('exported.csv')



unigram_df = pd.read_csv('../Processed_Dataset/features_unigram.csv')
bigram_df = pd.read_csv('../Processed_Dataset/features_bigram.csv')
trigram_df = pd.read_csv('../Processed_Dataset/features_trigram.csv')

unigram_list = unigram_df.columns[1:-1].tolist()

for word in cleaned_word_list:
  if word in unigram_list:
      unigram_list.remove(word)

bigram_list = bigram_df.columns[1:].tolist()

trigram_list = trigram_df.columns[1:].tolist()

extra_feature_list = unigram_list + bigram_list + trigram_list

for words in cleaned_multiple_word_list:
  if words in extra_feature_list:
    extra_feature_list.remove(words)

extra_feature_list += cleaned_word_list + cleaned_multiple_word_list

X_train, X_test, y_train, y_test = train_test_split(features_df, final_target_df, test_size=0.2)

classifier = MultinomialNB()
classifier.fit(X_train,y_train)

y_pred = classifier.predict_proba(X_test)
y_pred = y_pred[:, 1]
y_pred.shape

import matplotlib.pyplot as plt

plt.hist(y_pred)

metrics.roc_auc_score(y_test, y_pred)

from sklearn.feature_extraction.text import CountVectorizer

vec = CountVectorizer(tokenizer=nltk.word_tokenize, ngram_range=(1, 3), 
                      vocabulary=extra_feature_list)

vec.fit(transcripts)

pickle.dump(vec, open('count_vectorizer.sav', 'wb'))


features_df = pd.DataFrame(vec.transform(transcripts).toarray(), columns=vec.get_feature_names())

features_df

X_train, X_test, y_train, y_test = train_test_split(features_df, final_target_df, test_size=0.2)

classifier = MultinomialNB()
classifier.fit(X_train,y_train)

pickle.dump(classifier, open('persuasion_model.sav', 'wb'))

y_pred_proba = classifier.predict_proba(X_test)
y_pred_proba = y_pred_proba[:, 1]
y_pred = classifier.predict(X_test)
y_pred.shape

plt.hist(y_pred_proba)

metrics.roc_auc_score(y_test, y_pred_proba)

metrics.f1_score(y_test,y_pred)

