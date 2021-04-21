import path_planning as path
import nlp_util
import sentiment
from ast import literal_eval as make_tuple


def check_result(phrase, result, expected_result):
    if expected_result is not None:
        # print(result)
        # print(correct)
        if expected_result == result:
            return 1
        else:
            print("The phrase is: "+str(phrase)+", correct output should be: " +
                  str(expected_result)+", instead we have: "+str(result))
            return 0
        # assert (expected_result == result), f"Result: {result} \t Expected: {expected_result}"
    else:
        if result is None:
            return 1
        else:
            print("The phrase is: "+str(phrase) +
                  ", correct output should be None, instead we have: "+str(result))
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
        return check_result(phrase, (label, result), (expected_bool, expected_result))
    else:
        print("invalid file_desc")
        return 0


def test(file_path, file_desc):
    print("Test: " + file_desc)
    file_path = file_path
    total_commands = 0
    correct_commands = 0
    with open(file_path) as f:
        for line in f:
            total_commands += 1
            expected_result = None
            tup = make_tuple(line)
            phrase = tup[0]
            # print(f"Testing phrase: {phrase}")
            expected_bool = tup[1]
            if len(tup) == 3:
                expected_result = tup[2]
            correct_commands += compare(phrase,
                                        expected_bool, file_desc, expected_result)
            # print("GOOD")
    print("Total accuracy is "+str(correct_commands/total_commands*100)+"%")


if __name__ == "__main__":
    test('tests/path_planning_phrases.txt', "path planning")
    test('tests/is_question_phrases.txt', "is question")
    test('tests/sentiment_phrases.txt', "sentiment")
