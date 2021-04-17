import path_planning as path
from ast import literal_eval as make_tuple

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
    total_commands = 0
    correct_commands = 0
    with open(file_path) as f:
        for line in f:
            total_commands += 1
            expected_result = None
            tup = make_tuple(line)
            phrase = tup[0]
            expected_bool = tup[1]
            if len(tup) == 3:
                expected_result = tup[2]
            correct_commands += compare(phrase, expected_bool, expected_result)
            # print("GOOD")
    return correct_commands/total_commands*100

if __name__ == "__main__":
    print("Path Planning Accuracy: "+str(test_path_planning())+"%")
            
        
