'''
return format for all functions in this module

{
    "test_result": boolean,
    "info": {
        <specific info for each topic, only if test_result is True>
    }
}
'''

def weather(text):
    '''
    Tests if the text contains the word weather and identifies any
    time words
    '''
    output = {
        "test_result": False,
        "info": {}
    }
    
    target_words = ["weather", "temperature"]
    split_text = text.split()
    
    for word in target_words:
        if word in split_text:
            output["test_result"] = True

    if output["test_result"] == False
        return output

    #maybe factor out into text file
    time_words = ["today", "tommorrow", "current"]

def restaurant(text):
    return "restaurant" in text.split()

