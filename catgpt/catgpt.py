class Node:
    def __init__(self, char: str) -> None:
        self.head = char
        self.is_end = False
        self.alphabet = [None]*26
        self.freq = 0
        self.completed_word = None

class CatsTrie:
    def __init__(self, sentences: list) -> None:
        self.root = Node("")
        for sentence in sentences:
            self.add(sentence)

    def char_to_index(self, char:str) -> int:
        # Helper function to convert character to index
        char_index_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        for i in range(len(char_index_list)):
            if char == char_index_list[i]:
                return int(i)

    def add(self, sentence:str) -> None:
        node = self.root
        for char in sentence:
            index = self.char_to_index(char)
            if node.alphabet[index] is None:
                node.alphabet[index] = Node(char)
            node = node.alphabet[index]
        node.is_end = True
        node.freq += 1
        node.completed_word = sentence
        self.update(sentence, self.root, node.freq)

    def update(self, sentence:str, node:Node, count:int) -> None:
        for char in sentence:
            index = self.char_to_index(char)
            child = node.children[index]
            if child is not None and child.count < count:
                child.count = count
                child.completed_word = sentence
            node = child

    def autoComplete(self, prompt:str) ->str:
        node = self.root
        for char in prompt:
            index = self.char_to_index(char)
            if node.alphabet[index] is None:
                return None
            node = node.alphabet[index]
        if prompt == "":
            return self.root.completed_word
        return node.completed_word