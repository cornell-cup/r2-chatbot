import path_planning as path
from ast import literal_eval
import time
import requests

def compare(phrase, expected_bool, expected_result = None):
    is_command = path.isLocCommand(phrase)
    if is_command == expected_bool:
        if is_command:
            result = path.process_loc(phrase)
            if expected_result is not None:
            # print(result)
            # print(correct)
                if expected_result == result:
                    return 1
                else:
                    print("The phrase is: "+str(phrase)+", correct output should be: "+str(expected_result)+", instead we have: "+str(result))
                    return 0
                # assert (expected_result == result), f"Result: {result} \t Expected: {expected_result}"
            else:
                if result is None:
                    return 1
                else:
                    print("The phrase is: "+str(phrase)+", correct output should be None, instead we have: "+str(result))
                    return 0
        else:
            return 1
    else:
        print("The phrase is: "+str(phrase)+", correct is_command output should be: "+str(expected_bool)+", instead we have: "+str(is_command))
        return 0

def test_path_planning():
    file_path = 'tests/path_planning_phrases.txt'
    total_time = 0
    total_commands = 0
    correct_commands = 0
    with open(file_path) as f:
        for line in f:
            total_commands += 1
            expected_result = None
            tup = literal_eval(line)
            phrase = tup[0]
            expected_bool = tup[1]
            if len(tup) == 3:
                expected_result = tup[2]
            before = time.time()
            correct_commands += compare(phrase, expected_bool, expected_result)
            total_time += time.time() - before
            # print("GOOD")
    return correct_commands/total_commands*100, total_time/total_commands

def test_question_answering():
    USE_AWS = True
    url = "http://3.13.116.251/"
    route = "chatbot_qa/"
    file_path = 'tests/question_tests.txt'
    total_time = 0
    total_qs = 0
    if USE_AWS:
        with open(file_path) as f:
            for line in f:
                before = time.time()
                response = requests.get(url+route, params={'speech': line})
                if response.ok:
                    response = response.text
                    response = literal_eval(response)
                    response = response['answers'][0]['answer']
                    print(f"Question: {line}")
                    print(f"Answer: {response}")
                else:
                    print("Bad request")
                after = time.time()
                total_time += after - before
                total_qs += 1
        return total_time/total_qs
    else:
        print("AWS not active.")
        return 0


if __name__ == "__main__":
    path_plan = test_path_planning()
    print(f"Path Planning Accuracy: {path_plan[0]}% \t Average Time: {path_plan[1]}")
    avg_q_time = test_question_answering()
    print("Question-Answering Average Response Time (AWS): ", avg_q_time)
            
        
