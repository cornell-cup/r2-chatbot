from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import json


def import_data():
    '''
    Imports data for training a model and converts it to a DF.
    '''


def get_topic(question):
    '''
    Loads the topic classification model from "text_classification.sav" and returns the topic of a question (in words)
    Requires:
        question: str -> the question
    Returns:
        - the label of the topic (str)
    '''
    model = pickle.load(open("text_classification.sav", 'rb'))
    labels = ['Red', 'Kanye_West', 'Northwestern_University', 'Portugal',
              'Dell', 'Mandolin', 'Miami', 'Time', 'Napoleon', 'Windows_8']
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
    pass
