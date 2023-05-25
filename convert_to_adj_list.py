def convert_to_adj_list(connections, maxIn, maxOut) -> list:
    num_data_centres = len(maxIn)
    adj_list = [[] for _ in range(num_data_centres)]

    # convert connections into a adjacency list
    for connection in connections:
        start_node, end_node, edge_capacity = connection

        adj_list[start_node].append((end_node, edge_capacity))

    # adds the maximum output into the adjacency list
    for i, connection in enumerate(adj_list):
        adj_list[i].append((len(adj_list), maxIn[i]))
    
    # adds the maximum input into the adjacency list
    temp = []
    for i, connection in enumerate(adj_list):
        temp.append((i, maxOut[i]))
    adj_list.append(temp)

    return adj_list