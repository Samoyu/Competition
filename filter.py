import spacy
import nltk
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import FreqDist

nltk.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
sia = SentimentIntensityAnalyzer()

score_dic = {}
neg_score_list = []
neu_score_list = []
pos_score_list = []
pos_select = ["VERB", "NOUN", "ADJ", "ADV", "PART"]

def remove_stopwords_and_pos_select(df):
    df_preprocess = []
    
    for comment in df['comment']:
      doc = nlp(comment)

      token_lemma = " ".join([token.lemma_.lower() for token in doc if (token.pos_ in pos_select and not token.is_stop)])
      df_preprocess.append(token_lemma)
      
    return df_preprocess

def filter(google_comment_df):
    google_negative_comment = google_comment_df[google_comment_df['grade'] == 0]
    google_positive_comment = google_comment_df[google_comment_df['grade'] == 1]

    # Remove stopwords and do pos select
    google_negative_comment['comment'] = remove_stopwords_and_pos_select(google_negative_comment)
    google_positive_comment['comment'] = remove_stopwords_and_pos_select(google_positive_comment)
    google_negative_comment = google_negative_comment.drop(google_negative_comment[google_negative_comment['comment'] == ''].index)
    google_negative_comment.reset_index(drop=True)
    google_positive_comment = google_positive_comment.drop(google_positive_comment[google_positive_comment['comment'] == ''].index)
    google_positive_comment.reset_index(drop=True)

    # Delete neutral comments
    for comment in google_negative_comment['comment']:
        score_dic = sia.polarity_scores(comment)
        neg_score_list.append(score_dic['compound'])

    for comment in google_positive_comment['comment']:
        score_dic = sia.polarity_scores(comment)
        pos_score_list.append(score_dic['compound'])

    google_negative_comment['compound'] = neg_score_list
    google_positive_comment['compound'] = pos_score_list
    sorted_negative_dataframe = google_negative_comment.sort_values('compound', ascending=True)
    sorted_negative_dataframe = sorted_negative_dataframe.reset_index(drop=True)
    sorted_positive_dataframe = google_positive_comment.sort_values('compound', ascending=False)
    sorted_positive_dataframe = sorted_positive_dataframe.reset_index(drop=True)

    # Choose only top 30% of comments and turn it into list
    total_neg_rows = len(sorted_negative_dataframe)
    total_pos_rows = len(sorted_positive_dataframe)

    top_30_neg_rows = int(total_neg_rows * 0.3)
    top_30_pos_rows = int(total_pos_rows * 0.3)

    google_negative_comment_df = sorted_negative_dataframe.head(top_30_neg_rows)
    google_positive_comment_df = sorted_positive_dataframe.head(top_30_pos_rows)

    google_negative_comment_list = google_negative_comment_df['comment'].tolist()
    google_positive_comment_list = google_positive_comment_df['comment'].tolist()

    # Turn all comments into a string
    google_negative_mix = " ".join(google_negative_comment_list) 
    google_positive_mix = " ".join(google_positive_comment_list) 

    # Build fre list
    Negative_fre_list = google_negative_mix.split(" ")
    Positive_fre_list = google_positive_mix.split(" ")

    Neg_fdist = FreqDist(Negative_fre_list)
    Pos_fdist = FreqDist(Positive_fre_list)

    return Neg_fdist, Pos_fdist