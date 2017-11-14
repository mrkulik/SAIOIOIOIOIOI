#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json


def belman(c, n):
	# берем 1 строку исходного графа, остальные заполняем нулями
	B = [table[0]] + [[0 for i in range(c)] for j in range(1, n)]
	# в x будем записывать индекс, на котором дистигается максимум ф-ции Белмана
	x = [[0 for i in range(c)] for j in range(n)]
	# Считаем функцию Белмана
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
	# колличество столбцов
	c = len(table[0])
	# колличество строк
	n = len(table)
	B, x = belman(c, n)
	for b in B:
		print(b)
	print("\n")
	for x_i in x:
		print(x_i)
	print("\n")
	
	left = c - 1
	x0 = []
	# находим максимальную прибыль в задаче
	x0 += [x[n-1][B[n-1].index(max(B[n-1]))]]
	# колличество рессурсов оставшихся на остальные процессы
	left -= x[n-1][B[n-1].index(max(B[n-1]))]
	# идем по матрице x и смотрим, как распределить оставшиеся ресурсы между
	for i in range(n - 2, 0, -1):
		x0 += [x[i][left]]
		left -= x[i][left]

	x0 += [left]
	print(x0)