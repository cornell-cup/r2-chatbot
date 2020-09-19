from sklearn.feature_extraction.text import TfidfVectorizer
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

def fit_tfidf(X, training):
  '''
  Produces features from text using a TfIDF score. 
  Inputs:
    X (list): List containing the question inputs
    training (bool): True if training a model, false if just converting
    a single question
  Output: Array of features
  '''


def get_topic(question, model): 
  '''
  Returns the topic of a question (in words)
  Inputs:
    question (string): the question
    model: the trained model
  '''

def train():
  '''
  Splits the data into training set and testing set.
  Gets tfidf features from training set and trains model.
  Saves model as a file using pickle.
  Still need to finish this declaration
  '''
  
  




if __name__ == '__main__':
  #this should be run whenever the model needs to be trained
  #import data, process, convert to DF
  #perform tfidf vectorization and save the vectorizer
  #train model on tfidf features
  #save model as a file
  #test model