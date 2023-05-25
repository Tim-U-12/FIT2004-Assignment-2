from convert_to_adj_list import convert_to_adj_list
from dfs import dfs

if __name__ == '__main__':
    # Example input
    connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
    maxIn = [5000, 3000, 3000, 3000, 2000]
    maxOut = [5000, 3000, 3000, 2500, 1500]
    origin = 0
    targets = [4, 2]

    # Expected output: 4500

    # convert to adjacency list
    adj_list = convert_to_adj_list(connections, maxIn, maxOut)
    
    # run dfs
    visited = []
    dfs(visited, adj_list, 0)
