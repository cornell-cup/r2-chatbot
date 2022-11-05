MORSE_MAP =  {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "!": "-.-.--",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-.",
    "(": "-.--.",
    ")": "-.--.-",
    " ": " ",
    "=": "-...-",
    "+": ".-.-.",
    "\"": ".-..-.",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "*": "..-.-",
    "$": "...-..-",
    "#": ".-.-.",
    "\\": ".-..-.",
    "^": "..--.-",
    "_": "..--.-",
    "`": ".`-"
}

class TrieNode:
    def __init__(self, word=None, value = None, _char = None, parent = None):
        self.parent = parent
        # Should be same as key
        self._char = _char
        self.children = {}
        self.value = None
        if word is not None:
            self.insert(word, value)
    
    def insert(self, word, value, allow_multiple = False):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(_char = char, parent = node, value=[] if allow_multiple else value)
            node = node.children[char]
        if allow_multiple:
            node.value = [] if node.value is None else node.value
            node.value.append(value)
        else:
            node.value = value
    
    def get(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value
    
    def exists(self, word):
        return self.get(word) is not None
    
    def get_spelling(self):
        spelling = []
        node = self
        while node.parent is not None:
            spelling.append(node._char)
            node = node.parent
        return ''.join(reversed(spelling))

    def traverse(self, word):
        if word == '':
            return self.value, self.get_spelling(), ''
        node = self
        last_match = ''
        last_satisfactory = None
        next_piece = ''
        while len(word) and word[0] in node.children:
            next_piece += word[0]
            node = node.children[word[0]]
            if node.value is not None:
                last_match += next_piece
                next_piece = ''
                last_satisfactory = node
            word = word[1:]
        try:
            return last_satisfactory.value if last_satisfactory is not None else None, last_match, word
        except AttributeError:
            raise ValueError(f"No chirp found for morse code: '{word}'")


class Trie:
    def __init__(self, word = None, value = None, allow_multiple = False):
        self.root = TrieNode(word, value)
        self.allow_multiple = allow_multiple
    
    def insert(self, word, value):
        self.root.insert(word, value, allow_multiple=self.allow_multiple)
    
    def __setitem__(self, key, value):
        self.insert(key, value)

    def get(self, word):
        return self.root.get(word)

    def __getitem__(self, key):
        return self.get(key)

    def exists(self, word):
        return self.root.exists(word)
    
    def traverse(self, word):
        return self.root.traverse(word)

# Debugging code
if __name__ == '__main__':
    t = Trie('...-.-.---', 'ye')
    t.insert('..', 'boo-ya')
    val0, last_match0, left = t.traverse('...-.-.---..')
    print(val0, last_match0, left)
    val1, last_match1, left = t.traverse(left)
    print(val1, last_match1, left)