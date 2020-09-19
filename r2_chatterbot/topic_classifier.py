from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import json
import pandas as pd


def import_data():
    '''
    Imports data for training a model and converts it to a DF.

    '''
    #Import data from file
    f = open('train-v2.0.json')
    data = json.load(f)

    #Choose relevant topics
    to_choose = ['Red', 'Kanye_West', 'Northwestern_University', 'Portugal', 'Dell', 'Mandolin', 'Miami', 'Time',
               'Napoleon', 'Windows_8']

    #Create list of question_title_pairs
    question_title_pairs = []
    for item in data['data']:
      topic = item['title']
      if item['title'] in to_choose:
          for paragraph in item['paragraphs']:
              for qa in paragraph['qas']:
                  question_title_pairs.append({'question': qa['question'], 'topic': topic})

    #Convert question_title_pairs to dataframe
    df = pd.DataFrame(question_title_pairs)

    #Assign unique code to every topic
    codes = {}
    for index, value in enumerate(to_choose):
        codes[value] = index
        df['topic_code'] = df['topic']
        df = df.replace({'topic_code': codes})

    #Remove punctuation and uppercase from questions
    df['question_processed'] = df['question'].str.lower()
    punctuation_signs = list("?:!.,;")
    for punct_sign in punctuation_signs:
        df['question_processed'] = df['question_processed'].str.replace(punct_sign, '')

    return df



def get_topic(question, model):
    '''
    Returns the topic of a question (in words)
    Inputs:
      question (string): the question
      model: the trained model
    '''


def train(df):
    '''
    Splits the data into training set and testing set.
    Fits training data to combined tfidf vectorizer and multinomial logistic regression model
    Saves model to file 'text_classification.sav'. 
    Requires:
        - df: DataFrame -> dataframe that holds all question data. Should have 
        at least two columns, 'question_processed' and 'topic_code'. 
    Returns:
        - Test features, test labels, and model.
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
    print(classification_report(y_test, pred))
    print("Classification Report:")
    pass