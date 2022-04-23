import json

with open("response_options.json", "r") as f:
  response_options = json.load(f)


def get_category(user_in): 
  """
    Given a user's speech user_in, return a category such that response_options[category]["inputs"] contains
    exactly user_in.
    Assume "Hey c1c0" is already filtered out and the speech is completely lowercase and has no punctuation.
  
    params:
      - user_in (str): input speech
  """
  

def get_response(category, name): 
  """
    Returns a random response from a list of responses stored under the outputs for the "category" label.
    (response_options[category]["outputs"]) 
    Anywhere that the placeholder '<>' is found, replace the placeholder with the provided name. 
    
    params:
      - category (str): the category corresponding to the type of response
      - name (str): the name of the person to respond to
  
  """