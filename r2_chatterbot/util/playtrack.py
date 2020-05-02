from playsound import playsound

def playtrack(s):
    """
    Plays the track at s

    Parameter s: The string containing the file location
    Precondition: s is a string
    """
    assert type(s) == str
    for i in range(3):
        playsound(s)
