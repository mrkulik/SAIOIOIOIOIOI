#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

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


def FordFulkerson(start, end):
    parent = [-1] * len(graph)

    max_flow = 0
	#step 1: run untill we can reach t from s
    while BFS(start, end, parent):
        path_flow = 1000
        s = end
        while s != start:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        t = end
        while t != start:
            u = parent[t]
            graph[u][t] -= path_flow
            graph[t][u] += path_flow
            t = parent[t]

    return max_flow


if __name__ == '__main__':
    with open('8.json') as fp:
        graph = json.load(fp)

    print("Max:", FordFulkerson(0, 5))
