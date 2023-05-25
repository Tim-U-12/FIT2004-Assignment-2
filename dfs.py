def dfs(visited, graph, data_centre):
    if data_centre not in visited:
        print(data_centre)
        visited.append(data_centre)

        for neighbour in graph[data_centre]:
            dfs(visited, graph, neighbour[0])