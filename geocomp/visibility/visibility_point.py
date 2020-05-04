#!/usr/bin/env python
"""Algoritmo visibilidade de um ponto"""

from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.avl import AVL
from geocomp.common.ray import Ray
from geocomp.common.point import Point
from geocomp.common.vector import Vector
from geocomp.common.segment import Segment
from geocomp.common.pontoEvento import PontoEvento

import math

def VisibilityPoint (l):
	p = l[0]; l = l[1::]

	dist = []
	for i in range(len(l)):
		d = distPontoReta(p, l[i])
		dist.append(d)
	l = MergeSort(l,dist)

	fila = FilaEvento(l,p)

	#preprocessamento
	fila = MergeSort_ang(fila)
	seg = []
	for f in fila:
		find = False
		f.getPoint().plot('red')
		p2 = f.getSeg().to
		if p2 == f.getPoint():
			p2 = f.getSeg().init
		for i in range(len(seg)):
			if seg[i] == f.getSeg():
				find = True
				f.setEsq(False)

				if (f.getPoint().x >= 0 and f.getPoint().y > 0) \
				or (f.getPoint().x <= 0 and f.getPoint().y < 0) :
					f.setEsq(False)

				seg.remove(f.getSeg())
				break
		if(find == False):
			f.setEsq(True)
			seg.append(f.getSeg())
			if  f.getPoint().y - p.y == 0 and math.sin(angle(p2, p)) < 0:
				f.setEsq(False)
				seg.remove(f.getSeg())
			if (f.getPoint().x >= 0 and f.getPoint().y > 0) \
			or (f.getPoint().x <= 0 and f.getPoint().y < 0) :
				f.setEsq(True)

	#Linha de varredura
	ray = Ray(p, Vector([1, 0]))
	ray.plot('white')

	myTree = AVL() 
	root = None


	#verifica se a linha intersecta em algum segmento e add na árvore
	for i in range(len(l)):
		l[i].hilight(color_line = "pink")		
		control.sleep ()
		if ray.intersects(l[i]):
			root = myTree.insert(root,i, l[i])
			l[i].unhilight()
			l[i].hilight(color_line = "cyan")
		else:
			l[i].plot()
	ray.hide()

	light(myTree, root, l)

	#começa o processamento da linha de varredura
	equals = []
	for i in range(len(fila)):
		index = fila[i].getIndex()
		froot = myTree.getNode(root, index)

		#verifica se o próximo ponto possui o mesmo angulo
		if i != len(fila)-1 and fila[i].angle == fila[i+1].angle:
			equals.append(fila[i])
			if froot is None:
				root = myTree.insert(root, index, l[index])
				l[index].hilight(color_line = "cyan")
		else:
			id = control.plot_ray(p.x, p.y, fila[i].getPoint().x, fila[i].getPoint().y, 'white')
			
			#verifica se há mais de um ponto com o mesmo angulo
			if len(equals) !=0:
				equals.append(fila[i])
				if froot is None:
					root = myTree.insert(root, index, l[index])
					l[index].hilight(color_line = "cyan")
				
				#ilumina o segmento mais perto do ponto
				light(myTree, root, l)

				#remove os segmentos que terminam neste ponto
				for e in equals:
					if e.getEsq() == False:
						root = myTree.delete(root, e.getIndex())
						l[e.getIndex()].unhilight()

				light(myTree, root, l)

				equals = []
				control.sleep ()
				control.plot_delete(id)
			else:

				if froot is None:
				
					root = myTree.insert(root, index, l[index])
					l[index].hilight(color_line = "cyan")
				else:
					root = myTree.delete(root, index)
					l[index].unhilight()

				light(myTree, root, l)
				control.sleep ()
				control.plot_delete(id)
	return None

def MergeSort_ang(arr): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]  

		MergeSort_ang(L)  
		MergeSort_ang(R)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if L[i].angle <= R[j].angle: 
				arr[k] = L[i] 
				i+=1
			else: 
				arr[k] = R[j] 
				j+=1
			k+=1

		while i < len(L): 
			arr[k] = L[i] 
			i+=1
			k+=1

		while j < len(R): 
			arr[k] = R[j] 
			j+=1
			k+=1
	return arr

def MergeSort(arr, dist): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]
		distL = dist[:mid]
		distR = dist[mid:]  

		MergeSort(L, distL)  
		MergeSort(R, distR)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if distL[i] < distR[j]: 
				arr[k] = L[i] 
				dist[k] = distL[i]
				i+=1
			else: 
				arr[k] = R[j] 
				dist[k] = distR[j]
				j+=1
			k+=1

		while i < len(L): 
			arr[k] = L[i] 
			dist[k] = distL[i]
			i+=1
			k+=1

		while j < len(R): 
			arr[k] = R[j]
			dist[k] = distR[j] 
			j+=1
			k+=1
	return arr

def angle(s,p):
	x1 = 1; y1 = 0
	x2 = s.x - p.x; y2 = s.y - p.y

	cos1 = (x2*x2) + (y2*y2)
	cos2 =  math.sqrt(cos1)
	cos = x2/cos2

	degree = math.acos(cos)
	if y2 < 0 :
		degree = 180 - degree 
	degree = round(degree,2)
	return degree

def FilaEvento(l,p):
	fila = []
	for i in range(len(l)):
		p1, p2 = l[i].endpoints()
		fila.append( PontoEvento(p1, l[i], True, i, angle(p1,p)) )
		fila.append( PontoEvento(p2, l[i], False, i, angle(p2,p)) )
	return fila

def distPontoReta(p, seg):
	p1, p2 = seg.endpoints()

	pm = Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)
	d = prim.dist2(p,pm)

	return (d)

def light(myTree, root, l):
	minroot = myTree.getMinValueNode(root)
	if minroot != None:
		p1, p2 = l[minroot.val].endpoints()
		control.plot_segment(p1.x, p1.y, p2.x, p2.y, 'yellow')
