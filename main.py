from convert_to_adj_list import convert_to_adj_list
from maxThroughput import maxThroughput
# from dfs import dfs

if __name__ == '__main__':
    # Original graph
    connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
    maxIn = [5000, 3000, 3000, 3000, 2000]
    maxOut = [5000, 3000, 3000, 2500, 1500]
    origin = 0
    targets = [4, 2]

    # Transform the graph
    adj_list = convert_to_adj_list(connections, maxIn, maxOut)
    print(adj_list)
    origin_out = 2*origin + 1
    targets_out = [2*t + 1 for t in targets]

    # Compute the maximum flow
    max_flow_value = maxThroughput(adj_list, origin_out, targets_out)
    print(max_flow_value)

