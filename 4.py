#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json


def belman(c, n):
	# step 1.1 Matrix B - pick 1st str from input matrix + another [0], create matrix x of indexes [0], count Belman func
	B = [table[0]] + [[0 for i in range(c)] for j in range(1, n)]
	x = [[0 for i in range(c)] for j in range(n)]
	for i in range(1, n):
		for j in range(1, c):
			values = []
			for k in range(0, j+1):
				values += [table[i][k] + B[i-1][j-k]]
			B[i][j] = max(values)
			x[i][j] = values.index(B[i][j])
	return B, x


if __name__ == '__main__':
	table = []
	with open("4.json") as fp:
		table = json.load(fp)
	c = len(table[0])
	n = len(table)
	#step 1: count Belman func(return dostig maximum func matrix + indexes of max)
	B, x = belman(c, n)
	for b in B:
		print(b)
	print("---------------------------------")
	for x_i in x:
		print(x_i)
	print("---------------------------------")
	
	left = c - 1
	x_max = []
	
	# step 2: count result
	# step 2.1 find max profit of task
	x_max += [x[n-1][B[n-1].index(max(B[n-1]))]]
	# step 2.2: count left resourses
	left -= x[n-1][B[n-1].index(max(B[n-1]))]
	# allocate left resourses between left agents
	for i in range(n - 2, 0, -1):
		x_max += [x[i][left]]
		left -= x[i][left]

	x_max += [left]
	print(x_max)