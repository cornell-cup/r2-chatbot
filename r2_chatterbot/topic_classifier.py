from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import json
import numpy as np
import pandas as pd

current_topics = ['Red', 'Kanye_West', 'Northwestern_University',
                  'Portugal', 'Dell', 'Mandolin', 'Miami', 'Time', 'Napoleon', 'Windows_8']


def import_data():
    '''
    Imports data for training a model and converts it to a DF.
    '''
    # Import data from file
    f = open('train-v2.0.json')
    data = json.load(f)

    # Choose relevant topics
    to_choose = current_topics

    # Create list of question_title_pairs
    question_title_pairs = []
    for item in data['data']:
        topic = item['title']
        if item['title'] in to_choose:
            for paragraph in item['paragraphs']:
                for qa in paragraph['qas']:
                    question_title_pairs.append(
                        {'question': qa['question'], 'topic': topic})

    # Convert question_title_pairs to dataframe
    df = pd.DataFrame(question_title_pairs)

    # Assign unique code to every topic
    codes = {}
    for index, value in enumerate(to_choose):
        codes[value] = index
        df['topic_code'] = df['topic']
        df = df.replace({'topic_code': codes})

    # Remove punctuation and uppercase from questions
    df['question_processed'] = df['question'].apply(process)

    return df


def process(question):
    '''
    Converts a string to lowercase and removes puncutation.
    Requires:
        - question: str -> the question
    Returns:
        - the processed question (str)
    '''
    question = question.lower()
    punctuation_signs = list("?:!.,;")
    for punct_sign in punctuation_signs:
        question = question.replace(punct_sign, '')
    return question


def get_topic(question):
    '''
    Loads the topic classification model from "text_classification.sav" and returns the topic of a question (in words)
    Requires:
        question: str -> the question
    Returns:
        - the label of the topic (str)
    '''
    question = process(question)
    model = pickle.load(open("text_classification.sav", 'rb'))
    labels = current_topics
    predicted_code = model.predict([question])[0]
    predicted_prob = model.predict_proba([question])[0][predicted_code]
    predicted_label = labels[predicted_code]
    response = "I think this is most likely a question about {}. The probability of this is {}.".format(
        predicted_label, predicted_prob)
    return response


def train(df):
    '''
    Splits the data into training set and testing set.
    Fits training data to combined tfidf vectorizer and multinomial logistic regression model
    Saves model to file 'text_classification.sav'. 
    Requires:
        - df: DataFrame -> dataframe that holds all question data. Should have 
        at least two columns, 'question_processed' and 'topic_code'. 
    Returns:
        - Test features (DataFrame), test labels (DataFrame), and model.
    '''
    X = df['question_processed']
    y = df['topic_code']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=101)
    log_reg_model = LogisticRegression(C=100, solver='newton-cg')
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', log_reg_model)
    ])
    pipeline.fit(X_train, y_train)
    filename = 'text_classification.sav'
    pickle.dump(pipeline, open(filename, 'wb'))
    return X_test, y_test, pipeline


if __name__ == '__main__':
    print("Importing data...")
    df = import_data()
    print("Data imported and converted. Model Training...")
    X_test, y_test, model = train(df)
    print("Model trained and saved. Testing model...")
    pred = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, pred))
