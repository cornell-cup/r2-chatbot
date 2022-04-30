import json
import random
import os

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, "response_options.json")
with open(filepath, "r") as f:
  response_options = json.load(f)


def get_category(user_in): 
  """
    Given a user's speech user_in, return a category such that response_options[category]["inputs"] contains
    exactly user_in.
    Assume "Hey c1c0" is already filtered out and the speech is completely lowercase and has no punctuation.
  
    params:
      - user_in (str): input speech
  """

  for cat in response_options:
    for inputs in response_options[cat]["inputs"]:
      if (inputs == user_in): return cat
  
  return None

def get_response(category, name): 
  """
    Returns a random response from a list of responses stored under the outputs for the "category" label.
    (response_options[category]["outputs"]) 
    Anywhere that the placeholder '<>' is found, replace the placeholder with the provided name. 
    
    params:
      - category (str): the category corresponding to the type of response
      - name (str): the name of the person to respond to
  """

  outputs = response_options[category]["outputs"]
  output = outputs[random.randrange(len(outputs))]
  return output.replace("<>", name)


def get_response_combined(user_in, name):
  """
    Returns a random response from a list of responses stored under the outputs for the "category" label 
    that also stores inputs that should contain exactly user_in
    Anywhere that the placeholder '<>' is found, replace the placeholder with the provided name. 

    params: 
      - user_in (str): input speech
      - name (str): the name of the person to respond to
  """

  return get_response(get_category(user_in), name)


if __name__ == "__main__":
  user_in = ""
  print(get_response_combined(user_in, "Vincent"))