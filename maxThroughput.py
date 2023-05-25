from dfs import dfs

def maxThroughput(adj_list, origin_out, targets_out):
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
    max_flow = 0
    while True:
        visited = [False] * len(adj_list)
        flow = dfs(origin_out, float('inf'), visited, adj_list, targets_out)
        if flow == 0:
            break
        max_flow += flow
    return max_flow