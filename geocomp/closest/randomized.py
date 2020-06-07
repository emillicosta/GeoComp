#!/usr/bin/env python
"""Algoritmo aleatorizado"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math
import random


def Randomized (l):
	"Algoritmo aleatorizado para encontrar o par de pontos mais proximo"

	if len (l) < 2: return None
	
	closest = float("inf")
	a = l[0]; b = l[1]
	list_id = []
	id = None

	x_min = y_min = float("inf")
	x_max = y_max = float("-inf")
	for i in range(len(l)):
		if x_min > l[i].x:
			x_min = l[i].x
		if y_min > l[i].y:
			y_min = l[i].y
		if x_max < l[i].x:
			x_max = l[i].x
		if y_max < l[i].y:
			y_max = l[i].y

	random.shuffle(l) #embaralha os pontos

	closest = dist2(l[0],l[1])
	
	list_id = Grid(x_min, y_min, x_max, y_max, closest, list_id)
	
	s0, t0 = CalculaST(l[0], closest, x_min, y_min); s1, t1 = CalculaST(l[1], closest, x_min, y_min)
	H = dict();	H = Insira(H, l[0], s0, t0, 0); H = Insira(H, l[1], s1, t1, 1)
	
	for j in range(2,len(l)):
		
		l[j].hilight("yellow")
		control.sleep ()
		distancia = closest

		s,t = CalculaST(l[j], closest,x_min,y_min)
		
		for u in range(-2,3):
			for w in range(-2,3):
				
				if H.get(s+u) is not None and H.get(s+u).get(t+w) is not None:
					p = H.get(s+u).get(t+w)
					closest_ = dist2(l[j],l[p])
					
					if closest > closest_:
						closest = closest_
						a = l[p]; b = l[j]
						
		if distancia != closest:
			H, list_id = Reconstrua(closest,l, j, x_min, y_min, x_max, y_max, list_id)	
		else:
			H = Insira(H, l[j], s, t, j)

	#apaga o grid
	for i in range(len(list_id)):
		control.plot_delete(list_id[i])
	
	#apaga os pontos
	for i in range(j+1):
		l[i].hilight('white')

	a.hilight('red')
	b.hilight('red')
	ret = Segment (a, b)
	ret.hilight('red')
	ret.extra_info = 'distancia: %.2f'%math.sqrt (closest)
	return ret

def CalculaST(p, closest, x_min, y_min):
	closest_2 = (math.sqrt(closest))/2
	if closest_2 == 0:
		closest_2 = 0.01
	if p.x != x_min:
		s = math.floor(((p.x - x_min) / closest_2)- 0.00000001)
	else:
		s = 0
	if p.y != y_min:
		t = math.floor(((p.y - y_min) / closest_2)- 0.0000001)
	else:
		t=0
	return s,t

def Insira(H, p, s, t, i):
	p.hilight('blue')
	if s not in H.keys():
		H[s] = {}
	H[s][t] = i
	control.sleep ()
	return H

def Grid(x_min, y_min, x_max, y_max, closest, list_id):
	for i in range(len(list_id)):
		control.plot_delete(list_id[i])

	closest = (math.sqrt(closest))/2
	if closest == 0:
		closest = 0.01

	X =  math.ceil((x_max-x_min)/closest)
	Y =  math.ceil((y_max-y_min)/closest)

	#vertical
	for i in range(X+1):
		x = x_min + (i*closest)
		y=y_min+Y*closest
		id = control.plot_segment(x, y_min,x, y)
		list_id.append(id)
	
	#horizontal
	for i in range(Y+1):
		y = y_min + (i*closest)
		x = x_min+ X*closest
		id = control.plot_segment(x_min, y,x, y)
		list_id.append(id)

	control.sleep ()
	return list_id

def Reconstrua(closest,l,j,x_min, y_min, x_max, y_max, list_id):
	H = dict()
	for i in range(j+1):
		l[i].hilight('white')
	list_id = Grid(x_min, y_min, x_max, y_max, closest, list_id)
	for i in range(j+1):
		s,t = CalculaST(l[i], closest, x_min, y_min)
		H = Insira(H, l[i], s, t, i)
	return H, list_id