import path_planning as path
from ast import literal_eval as make_tuple

def compare(phrase, expected_bool, expected_result = None):
    is_command = path.isLocCommand(phrase)
    assert is_command == expected_bool
    if is_command:
        if expected_result is not None:
            result = path.process_loc(phrase)
        # print(result)
        # print(correct)
            assert (expected_result == result), f"Result: {result} \t Expected: {expected_result}"

if __name__ == "__main__":
    file_path = 'tests/path_planning_phrases.txt'
    with open(file_path) as f:
        for line in f:
            expected_result = None
            tup = make_tuple(line)
            phrase = tup[0]
            print(f"Testing phrase: {phrase}")
            expected_bool = tup[1]
            if len(tup) == 3:
                expected_result = tup[2]
            compare(phrase, expected_bool, expected_result)
            print("GOOD")
            
        
