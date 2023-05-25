def convert_to_adj_list(connections, maxIn, maxOut) -> list:
    num_data_centres = len(maxIn)
    adj_list = [[] for _ in range(num_data_centres)]

    for connection in connections:
        start_node, end_node, edge_capacity = connection

        adj_list[start_node].append((end_node, edge_capacity))

    return adj_list

        
        



g = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]

print(convert_to_adj_list(g, maxIn, maxOut))