#!/usr/bin/env python
"""Algoritmo forca-bruta"""

from geocomp.common.segment import Segment
from geocomp.common.ray import Ray
from geocomp.common.vector import Vector
from geocomp.common.avl import AVL
from geocomp.common.pontoEvento import PontoEvento
from geocomp.common import control
from geocomp.common.guiprim import *
import math


def VisibilityPoint (l):
	"Algoritmo forca bruta para encontrar o par de pontos mais proximo"
	fila = FilaEvento(l)
	p = l[0]

	#preprocessamento
	fila = MergeSort_ang(fila, p)
	seg = []
	for f in fila:
		find = False
		f.getPoint().plot('red')
		for i in range(len(seg)):
			if seg[i] == f.getSeg():
				find = True
				f.setEsq(False)
				seg.remove(f.getSeg())
				break
		if(find == False):
			f.setEsq(True)
			seg.append(f.getSeg())
		control.sleep ()

	l = []
	x = 0
	for i in range(len(fila)):
		if fila[i].getEsq() == True:
			l.append(fila[i].getSeg())
			fila[i].setIndex(x)
			for j in range(i+1,len(fila)):
				if fila[i].getSeg() == fila[j].getSeg():
					fila[j].setIndex(x)
			x = x+1

	#Linha de varredura
	ray = Ray(p, Vector([1, 0]))
	ray.plot('white')

	myTree = AVL() 
	root = None

	#verifica se a linha intersecta em algum segmento e add na árvore
	for i in range(len(l)):
		l[i].hilight(color_line = "blue")
		control.sleep ()
		if ray.intersects(l[i]):
			l[i].hilight(color_line = "green")
			p1, p2 = l[i].endpoints()
			root = myTree.insert(root,i, l[i])
		else:
			l[i].plot()
	ray.hide()

	for f in fila:
		p1 = f.getPoint().x
		p2 = f.getPoint().y
		id = control.plot_ray(p.x, p.y, p1, p2, 'white')
		froot = myTree.getNode(root, f.getIndex())
		if froot == None:
			
			root = myTree.insert(root, f.getIndex(), f.getSeg())
			minroot = myTree.getMinValueNode(root)
			if minroot != None:
				minroot.segment.hilight(color_line = "yellow")
		else:
			minroot = myTree.getMinValueNode(root)
			if minroot != None:
				minroot.segment.hilight(color_line = "yellow")

			root = myTree.delete(root, f.getIndex())

			minroot = myTree.getMinValueNode(root)
			if minroot != None:
				minroot.segment.hilight(color_line = "yellow")

		control.sleep ()
		control.plot_delete(id)
	return None

def MergeSort_ang(arr, p): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]  

		MergeSort_ang(L,p)  
		MergeSort_ang(R,p)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if (angle(L[i],p) < angle(R[j],p) ) or (angle(L[i],p) == angle(R[j],p) and prim.dist2(p,L[i].getPoint()) < prim.dist2(p,R[j].getPoint())): 
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

def angle(s,p):
	x1 = 1; y1 = 0
	x2 = s.getPoint().x - p.x; y2 = s.getPoint().y - p.y

	cos1 = (x2*x2) + (y2*y2)
	cos2 =  math.sqrt(cos1)
	cos = x2/cos2

	degree = math.acos(cos)
	if y2 < 0 :
		degree = 180 - degree 
	degree = round(degree,2)
	return degree

def FilaEvento(l):
	fila = []
	for i in range(1, len(l)):
		p1, p2 = l[i].endpoints()
		fila.append( PontoEvento(p1, l[i], True, i) )
		fila.append( PontoEvento(p2, l[i], False, i) )
	return fila