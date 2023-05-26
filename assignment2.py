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