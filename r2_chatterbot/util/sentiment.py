from transformers import pipeline

classifier = pipeline('sentiment-analysis')
'''
Takes in [s: str] and returns either 'POSITIVE', 'NEGATIVE' or 'NEUTRAL'
Optionally: [confidence_thresh] to make 'NEUTRAL' more or less sensitive
'''
def analyze(s: str, confidence_thresh: int = .99) -> str:
  classification = classifier(s)
  confidence = classification[0]['score'] 
  label = classification[0]['label']
  if confidence > confidence_thresh:
    return label
  return 'NEUTRAL'