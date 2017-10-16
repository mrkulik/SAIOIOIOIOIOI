import json


def diejkstra(g, n):
	inf = 1000
	s = 0
	d = [inf] * n
	p = [0] * n
	d[s] = 0
	used = [False] * n
	
	for i in range(n):
		v = -1
		for j in range(n):
			if not used[j] and (v == -1 or d[j] < d[v]):
				v = j

		if d[v] == inf:
			break
		used[v] = True

		for j in range(len(g[v])):
			to = g[v][j][0]
			l = g[v][j][1]

			if d[v] + l < d[to]:
				d[to] = d[v] + l
				p[to] = v

	print(d)

if __name__ == '__main__':
	with open('6_in.json') as f_d:
		g = json.load(f_d)
	n = len(g)
	
	diejkstra(g, n)