def dfs(node, min_capacity, visited, adj_list, targets_out):
    '''
    Function description:
    Approach description (if main function):
    :Input:
    argv1:
    argv2:
    :Output, return or postcondition:
    :Time complexity:
    :Aux space complexity:
    '''
    if node in targets_out:
        return min_capacity

    visited[node] = True
    for i, (neighbor, capacity) in enumerate(adj_list[node]):
        if not visited[neighbor] and capacity > 0:
            new_min_capacity = min(min_capacity, capacity)
            flow = dfs(neighbor, new_min_capacity, visited, adj_list, targets_out)
            if flow > 0:
                adj_list[node][i] = (neighbor, capacity - flow)
                for j, (rev_node, rev_capacity) in enumerate(adj_list[neighbor]):
                    if rev_node == node:
                        adj_list[neighbor][j] = (rev_node, rev_capacity + flow)
                        break
                else:
                    adj_list[neighbor].append((node, flow))
                return flow
    return 0