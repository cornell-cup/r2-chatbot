from transformers import pipeline
import requests

classifier = pipeline('sentiment-analysis')
# '''
# Takes in [s: str] and returns either 'POSITIVE', 'NEGATIVE' or 'NEUTRAL'
# Optionally: [confidence_thresh] to make 'NEUTRAL' more or less sensitive
# '''
def analyze(s: str, confidence_thresh: int = .99) -> str:
  classification = classifier(s)
  confidence = classification[0]['score'] 
  label = classification[0]['label']
  if confidence > confidence_thresh:
    return label, confidence
  return 'NEUTRAL', confidence


url = "http://3.13.116.251/"
sentiment_qa_route = "sentiment_analysis/"


def get_sentiment(speech, USE_AWS):
  response = "I am sure what you have just said is very interesting, but I can't process it right now."
  if USE_AWS:
     response = requests.get(url + sentiment_qa_route, params={'speech': speech})
     if response.ok:
       response = response.text
  else:
    pass
    # sent, conf = analyze(speech)
    # response = f"Sentiment: {sent} \t Confidence: {conf}"

  if "POSITIVE" in response:
    return "That's great!"
  
  if "NEUTRAL" in response:
    return "Okay."

  if "NEGATIVE" in response:
    return "That isn't good."

  return response

