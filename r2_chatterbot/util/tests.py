import path_planning as path
import nlp_util
import sentiment
from ast import literal_eval as make_tuple
import time
import requests

url = "http://3.13.116.251/"
route = "chatbot_qa/"

def check_result(phrase, result, expected_result):
    if result == expected_result:
        return 1
    else:
        print(f"Incorrect result for: {phrase} \t Expected: {expected_result} \t Result: {result}")
        return 0


def compare(phrase, expected_bool, file_desc, expected_result=None):
    if file_desc == "path planning":
        is_command = path.isLocCommand(phrase)
        if is_command == expected_bool:
            if is_command:
                result = path.process_loc(phrase)
                return check_result(phrase, result, expected_result)
            else:
                return 1
        else:
            print("The phrase is: "+str(phrase)+", correct output should be: " +
                  str(expected_bool)+", instead we have: "+str(is_command))
            return 0
    elif file_desc == "is question":
        result = nlp_util.is_question(phrase)
        return check_result(phrase, result, (expected_bool, expected_result))
    elif file_desc == "sentiment":
        label, result = sentiment.analyze(phrase)
        return check_result(phrase, label, expected_bool)        
    else:
        print("invalid file_desc")
        return 0


def test(file_path, file_desc):
    print("Test: " + file_desc)
    file_path = file_path
    total_commands = 0
    correct_commands = 0
    total_time = 0
    with open(file_path) as f:
        for line in f:
            total_commands += 1
            if file_desc != "question answering":
                expected_result = None
                tup = make_tuple(line)
                phrase = tup[0]
                expected_bool = tup[1]
                if len(tup) == 3:
                    expected_result = tup[2]
                before = time.time()
                correct_commands += compare(phrase, expected_bool, file_desc, expected_result)
                total_time += time.time() - before
            else:
                before = time.time()
                response = requests.get(url+route, params={'speech': line})
                if response.ok:
                    response = response.text
                    response = make_tuple(response)
                    response = response['answers'][0]['answer']
                    print(f"Question: {line} \nAnswer: {response}")
                else:
                    print("AWS is not responding.")
                total_time = time.time() - before

    if file_desc != "question answering":
        print("Total accuracy is "+str(correct_commands/total_commands*100)+"%")
    print("Average time is "+str(total_time/total_commands)+" s")


if __name__ == "__main__":
    test('../tests/testcases/path_planning_phrases.txt', "path planning")
    test('../tests/testcases/is_question_phrases.txt', "is question")
    test('../tests/testcases/sentiment_phrases.txt', "sentiment")
    test('../tests/testcases/question_tests.txt', 'question answering')
