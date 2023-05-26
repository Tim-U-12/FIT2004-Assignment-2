def convert_to_adj_list(connections: list, maxIn: list, maxOut: list) -> list:
    '''
    Function description:
    This function transforms the provided graph into an adjacency list. 
    The adjacency list have two nodes representing the flow in and flow out of the each data centre.
    We only care about adding 1 additional node per node of the original graph, because only the smaller
    capacity restriction matters, since it dictates the flow the total flow through that node.

    :Input:
    argv1 "connections" : list of list representing the connection and capacities between data centres
    argv2 "maxIn": list of integers representing the maximum flow into each data centre, which are represented by the index.
    argv2 "maxOut": list of integers representing the maximum flow out of each data centre, which are represented by the index.

    :Output, return or postcondition:
    returns an adjacency list representing the connections between data centres.
    
    :postcondidtiton: 
    the returned list must be in order, since the index determines where the datacentres are receiving the flow from

    :Time complexity:
    O(n), where n is the number of datacentres 

    :Aux space complexity:
    O(2n) where n is the size of the adj_list, which is the size of the graph
    '''
    n = len(maxIn)                                                              # n represents the number of datacentres
    adj_list = [[] for _ in range(2 * n)]                                       # creates empty adjacency list

    for node in range(n):                                                       # loops over the number of datacentres
        in_node, out_node = 2 * node, 2 * node + 1                              # appoints 
        adj_list[in_node].append((out_node, min(maxIn[node], maxOut[node])))    # adds the connection between the in and out node 
        adj_list[out_node].append((in_node, 0))                                 # adds the reverse capacity 

    for from_node, to_node, capacity in connections:                            
        out_from, in_to = 2 * from_node + 1, 2 * to_node                        # calculates the index of the in and out nodes
        adj_list[out_from].append((in_to, capacity))                            # adds the connection between datacentres
        adj_list[in_to].append((out_from, 0))                                   # adds the reverse capacity

    return adj_list

def dfs(node: int, bottleneck: float, visited: list, adj_list: list, targets_out: list) -> float:
    '''
    Function description:
    This function is a depth first seach that returns the capcity of the augmenting path found.
    starting from the given node, it checks to see if the neigbouring datacentres have been explored.
    if it hasn't and it still has a capcity greater than 0, it will compare the bottleneck with the capcity
    of the newly discovered datacentre. It will then perform another dfs with the updated minumum capacity, 
    till it reaches the target node. once reaching the target node, it updates both the forward and backward
    flow capcity of all the explored edges.

    :Input:
    argv1 "node": int value representing the index of the node in the adj_list being explored
    argv2 "bottleneck": float value representing the maximum capacity along the augmenting path
    argv3 "visited": a list of booleans representing whether a node has been explored, where the index represents the node
    argv4 "adj_list": an adjacency list representation of the orginal graph
    argv5 "targets_out": list of integers representing the target data centre we're trying to get to.

    :Output, return or postcondition:
    returns a float value representing the minimum capacity along the augmenting path.

    :Time complexity:
    O(V+E), where V is the number of nodes and E is the number of edges.

    :Aux space complexity:
    O(V), where V is the number of nodes.
    '''
    for i in targets_out:                                                           # segement checks to see if the dfs has reached the target node
        if node == i:                                                               # if it does, it returns the bottleneck flow
            return bottleneck

    visited[node] = True                                                            
    for i in range(len(adj_list[node])):
        neighbour, capacity = adj_list[node][i]

        if not visited[neighbour] and capacity > 0:                                 # checks to see if there is an adjacent datacentre that can be explored
            new_min_capacity = min(bottleneck, capacity)                            # updates the bottle neck if the adjacent edge has a smaller capacity than the bottleneck
            flow = dfs(neighbour, new_min_capacity, visited, adj_list, targets_out) # performs dfs to find the target node
            if flow > 0:                                                            # if the flow to the target is greater than zero
                adj_list[node][i] = (neighbour, capacity - flow)                    # it proceeds to update the capacity of all the edges it visited
                for j in range(len(adj_list[neighbour])):                           # iterates over the edges in the adjacent datacentre
                    rev_node, rev_capacity = adj_list[neighbour][j]                 
                    if rev_node == node:                                            # checks to see if the original node is reached
                        adj_list[neighbour][j] = (rev_node, rev_capacity + flow)    # updates the reverse flow
                        break
                    else:
                        adj_list[neighbour].append((node, flow))                    # Add reverse flow edge with capacity if the reverse flow doesnt exist
                return flow
    return 0

def maxThroughput(connections:list, maxIn:list, maxOut:list, origin_out:int, targets_out:list) -> float:
    '''
    Function description:
    The following function calculates the maximum flow from the given origin node to the given target nodes.
    It does so by converting the given graph 'connections' into a adjacency list that ford fulkerson can be 
    performed on. It uses depth first search to find the maximum flow from the the origin to the targets.
    it continues to perform dfs until there isn't anymore flow can pass through the network flow graph.

    Approach description (if main function):
    The approach to the problem was to transform the connections graph such that it contains the maxIn and maxOut
    capacities. This would then allow me to perform the ford fulkerson algorithm to determine the maximum flow.

    :Input:
    argv1 "connections": a list of tuples representing the connections between datacentres, in addition to 
    the edge capacity. 
    argv2 "maxIn": a list of numeric values that dictates the total maximum flow into a datacentre
    argv3 "maxOut": a list numeric values that dictates the total maximum flow out from a datacentre 
    argv4 "origin": an integer representing the starting node
    argv5 "targets": a list of integers representing the end nodes

    :Output, return or postcondition:
    returns the maximum flow from the origin to the targets.

    :Time complexity: 
    O(V+E), where V represents the number of datacentres and E represents the number of edges
    
    :Aux space complexity:
    O(V), where V represents the number of datacentres
    '''
    adj_list = convert_to_adj_list(connections, maxIn, maxOut)                      
    origin_out = 2*origin_out + 1                                                   # determines the new origin value
    targets_out = [2*t + 1 for t in targets_out]                                    # calculates the new target values

    max_flow = 0
    while True:                                                                    
        visited = [False] * len(adj_list)                                           # initialises a list with all values set to false to indicate whether a node has been visited in the adjacency list
        flow = dfs(origin_out, float('inf'), visited, adj_list, targets_out)        # performs dfs
        if flow == 0:                                                               # if there are not changes, break from the while loop
            break
        max_flow += flow                                                            
    return max_flow

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

        if node.freq > self.most_freq_word[1]:                              # checks whether or not the current word has a greater frequency then all the other ones we've seen
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