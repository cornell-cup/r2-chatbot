from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def import_data():
  '''
  Imports data for training a model and converts it to a DF.
  
  '''
  
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
