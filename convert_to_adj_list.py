def convert_to_adj_list(connections: list, maxIn: list, maxOut: list) -> list:
    '''
    Function description:
    This function transforms the provided graph into an adjacency list. 
    The adjacency list have two nodes representing the flow in and flow out of the each data centre.
    There are 

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
    n = len(maxIn)
    adj_list = [[] for _ in range(2*n)]
    
    for node in range(n):
        in_node, out_node = 2*node, 2*node + 1
        adj_list[in_node].append((out_node, min(maxIn[node], maxOut[node])))

    for from_node, to_node, capacity in connections:
        out_from, in_to = 2*from_node + 1, 2*to_node
        adj_list[out_from].append((in_to, capacity))

    return adj_list