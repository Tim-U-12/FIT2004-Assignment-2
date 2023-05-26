def convert_to_adj_list(connections: list, maxIn: list, maxOut: list) -> list:
    n = len(maxIn)
    adj_list = [[] for _ in range(2 * n)]

    for node in range(n):
        in_node, out_node = 2 * node, 2 * node + 1
        adj_list[in_node].append((out_node, min(maxIn[node], maxOut[node])))
        adj_list[out_node].append((in_node, 0))  # Add reverse flow edge with 0 capacity

    for from_node, to_node, capacity in connections:
        out_from, in_to = 2 * from_node + 1, 2 * to_node
        adj_list[out_from].append((in_to, capacity))
        adj_list[in_to].append((out_from, 0))  # Add reverse flow edge with 0 capacity

    return adj_list

def dfs(node: int, bottleneck: float, visited: list, adj_list: list, targets_out: list) -> float:
    for i in targets_out:
        if node == i:
            return bottleneck

    visited[node] = True
    for i in range(len(adj_list[node])):
        neighbour, capacity = adj_list[node][i]

        if not visited[neighbour] and capacity > 0:
            new_min_capacity = min(bottleneck, capacity)
            flow = dfs(neighbour, new_min_capacity, visited, adj_list, targets_out)
            if flow > 0:
                adj_list[node][i] = (neighbour, capacity - flow)
                for j in range(len(adj_list[neighbour])):
                    rev_node, rev_capacity = adj_list[neighbour][j]
                    if rev_node == node:
                        adj_list[neighbour][j] = (rev_node, rev_capacity + flow)
                        break
                else:
                    adj_list[neighbour].append((node, flow))  # Add reverse flow edge with capacity
                return flow
    return 0

def maxThroughput(connections, maxIn, maxOut, origin, targets):
    adj_list = convert_to_adj_list(connections, maxIn, maxOut)
    origin = 2 * origin + 1
    targets = [2 * t + 1 for t in targets]

    max_flow = 0
    while True:
        visited = [False] * len(adj_list)
        flow = dfs(origin, float('inf'), visited, adj_list, targets)
        if flow == 0:
            break
        max_flow += flow
    return max_flow



connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]
origin = 0
targets = [4, 2]
print(maxThroughput(connections, maxIn, maxOut, origin, targets))

connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]
origin = 1
targets = [4, 2]
print(maxThroughput(connections, maxIn, maxOut, origin, targets))


connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]
origin = 0
targets = [1, 3]
print(maxThroughput(connections, maxIn, maxOut, origin, targets))

connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]
origin = 0
targets = [4, 2]

print(maxThroughput(connections, maxIn, maxOut, origin, targets))
