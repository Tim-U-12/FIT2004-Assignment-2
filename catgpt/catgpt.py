class Node:
    def __init__(self, char: str) -> None:
        '''
        Function description:
        This function initialises the class. It serves as the foundation of the node class by storing 
        several variables.

        :Input:
        argv1 "char": a string that represents a character

        :Output, return or postcondition:

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        '''
        self.head = char                                                    # represents a character in the Trie
        self.is_end = False                                                 # boolean used to check whether or not the character is the end of a sentence
        self.alphabet = [None]*26                                           # represents the next possible chars
        self.freq = 0                                                       # how often the word is used
        self.completed_word = None                                          # what word is completed

class CatsTrie:
    def __init__(self, sentences: list) -> None:
        '''
        Function description:
        initialises the class by creating a root node. the function then proceeds to add the characters from the sentence
        in the given sentences list, into a trie.

        :Input:
        argv1 "sentences": a list of words used to "train" the CatsTrie model
        
        :Output, return or postcondition:
        the CatsTrie stores the sentence in sentences as a Trie.

        :Time complexity:
        O(N), where N is the number of characters in sentences

        :Aux space complexity:
        O(N), where N is the number of characters in sentences
        '''
        self.root = Node("")                                                # cretes the first node and dub it to be the root node
        self.most_freq_word = ("", 0)                                       # initialises a tuple containing the most frequent word and it's frequency
        for sentence in sentences:                                          # loops through all of the sentence in sentences 
            self.add(sentence)                                              # then proceeds to add them to the Trie represented by nodes

    def char_to_index(self, char:str) -> int:
        '''
        Function description:
        basic function to calculate the relative index of a character

        :Input:
        argv1 "char": a character to be converted

        :Output, return or postcondition:
        returns an integer valure representing the index of the input character

        :Time complexity:
        O(1)

        :Aux space complexity:
        O(1)
        '''
        char_index_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']          # the alphabet

        for i in range(len(char_index_list)):                               
            if char == char_index_list[i]:
                return int(i)

    def add(self, sentence: str) -> None:
        '''
        Function description:
        Adds a sentence to the CatsTrie. It does so by iterating through a given sentence and traversing through
        the linked list representing a trie, and creating new nodes representing each character in the sentence.
        It then updates the attributes of the last node. After that, it goes back to all the nodes that it has visited
        and updates the attributes of those nodes. Lastly the function keeps track of the most frequent nodes.  

        :Input:
        argv1 "sentence": a string that has its characters placed within the Trie

        :Output, return or postcondition:
        None

        :Time complexity:
        O(M), where M is the length of the sentence
                
        :Aux space complexity:
        O(M), where M is the length of the sentence
        '''
        node = self.root                                                    # makes the start node the root node
        for char in sentence:
            index = self.char_to_index(char)
            if node.alphabet[index] is None:                                # if the next character in the sentence isn't represented in the trie
                node.alphabet[index] = Node(char)                           # create a new node at the index of the new character symbolizing a branch off from an existing branch)
            node = node.alphabet[index]                                     # appoint the new node as the starting node to run it back through the loop
        node.is_end = True                                                  # once the loop finishes, it symbolizes the end of a word, thus the end node will update the boolean to represent that
        node.freq += 1                                                      # updates the freq of that word being used
        node.completed_word = sentence                                      # stores the completed sentence in the node
        self.update(sentence, self.root, node.freq)                         # updates the frequency of all the previous node/char it went by

        if node.freq > self.most_freq_word[1]:                              # checkss whether or not the current word has a greater frequency then all the other ones we've seen
            self.most_freq_word = (node.completed_word, node.freq)          # updates the most frequent word

    def update(self, sentence: str, node: Node, freq: int) -> None:
        '''
        Function description:
        iterates through a given sentence, and then it checks to see whether or not the character is none and whether
        or not the frequency of the sentence is greater than that of the frequency of the word in the current node.
        it then updates accordingly and moves on to the next node.

        :Input:
        argv1 "sentence": a string representing the sentence
        argv2 "node": a node representing the current position in the trie
        argv3 "freq": the frequency to be updated

        :Output, return or postcondition:
        None

        :Time complexity:
        O(M), where M is the length of the sentence

        :Aux space complexity:
        O(1)
        '''
        for char in sentence:
            index = self.char_to_index(char)
            next_char = node.alphabet[index]
            if next_char is not None and next_char.freq < freq:             # it checks to see if the next sentence has a higher frequency.
                next_char.freq = freq                                       # this section is extremely important since it dictates the most likely sentence from each prompt
                next_char.completed_word = sentence
            node = next_char

    def autoComplete(self, prompt:str) ->str:
        '''
        Function description:
        the function takes in a given prompt, using the characters from the prompt it iterates through the trie. 
        Once it completes it's iteration, the node that it finishes on will have stored in it the most likely word.

        Approach description (if main function):
        :Input:
        argv1 "prompt": a given string

        :Output, return or postcondition:

        :Time complexity:
        O(X + Y), where X is the length of the prompt and Y is the length of the most frequence sentence in sentences

        :Aux space complexity:
        O(1)
        '''
        if prompt == "":                                                    # checks to see if there was a prompt given
            return self.most_freq_word[0]                                   # if not then it will return the most frequent word

        node = self.root
        for char in prompt:                                                 # iterates through the characters in the prompt
            index = self.char_to_index(char)                                # converts the character into an index
            if node.alphabet[index] is None:                                # checks to se if the prompt can be predicted 
                return None                                                 # if it is an unpredictable prompt, it returns None
            node = node.alphabet[index]                                     # updates the current node to reflect the next next character in the prompt
        return node.completed_word

