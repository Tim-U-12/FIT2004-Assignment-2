def convert_to_adj_list(connections, maxIn, maxOut) -> list:
    num_data_centres = len(maxIn)
    adj_list = [[] for _ in range(num_data_centres)]

    for connection in connections:
        start_node, end_node, edge_capacity = connection

        adj_list[start_node].append((end_node, edge_capacity))

    return adj_list