import json

# Поиск в ширину, O(N+M)
def BFS(s, t, parent):
    visited = [False] * (len(graph))

    queue = [s]

    visited[s] = True

    while queue:

        u = queue.pop(0)

        for ind, val in enumerate(graph[u]):
            if visited[ind] == False and val > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u

    return True if visited[t] else False


# Возвращает максимальный поток из s в t
def FordFulkerson(source, sink):
    parent = [-1] * len(graph)

    max_flow = 0

    # Пока имеются пути из s в t
    while BFS(source, sink, parent):
        path_flow = float("Inf")
        s = sink
        # Находим ребро с минимальной пропускной способностью
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        t = sink
        # Для прямых дуг увеличиваем поток на мин. пропускн. способн.
        # Для обратных - уменьшаем поток на мин. пропускн. способн.
        while t != source:
            u = parent[t]
            graph[u][t] -= path_flow
            graph[t][u] += path_flow
            t = parent[t]

    return max_flow


if __name__ == '__main__':
    with open('8.json') as fp:
        graph = json.load(fp)

    print("Максимальный поток:", FordFulkerson(0, 5))
