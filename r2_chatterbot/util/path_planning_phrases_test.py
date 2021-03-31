import path_planning as path

def compare(phrase, correct):
    is_command = path.isLocCommand(phrase)
    if is_command:
        result = str(path.process_loc(phrase))

        print(result)
        print(correct)
        assert (correct == result)
    else:
        assert correct == 'error'

if __name__ == "__main__":
    file_path = 'tests/path_planning_phrases.txt'
    with open(file_path) as f:
        line = f.readline().split(':')
        phrase = line[0]
        correct = line[1]
        while line:
            compare(phrase, correct)
