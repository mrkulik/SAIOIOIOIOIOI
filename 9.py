import json


def floyd(D, R, m):
	for k in range(m):
		for i in range(m):
			for j in range(m):
				if D[i][k] + D[k][j] < D[i][j]:
					R[i][j] = R[i][k]
				D[i][j] = min([D[i][j], D[i][k] + D[k][j]])
	return D, R


if __name__ == '__main__':
	with open('9_D_in.json') as f_d:
		D = json.load(f_d)§
	with open('9_R_in.json') as f_r:
		R = json.load(f_r)
	m = len(D)
	
	floyd(D, R, m)
	
	for n in D:
		print(n)

	for n in R:
		print(n)