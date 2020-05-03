#!/usr/bin/env python
"""Algoritmo forca-bruta"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common.ray import Ray
from geocomp.common.vector import Vector
from geocomp.common.avl import AVL
from geocomp.common.pontoEvento import PontoEvento
from geocomp.common import control
from geocomp.common.guiprim import *
import math


def VisibilityPoint (l):
	"Algoritmo forca bruta para encontrar o par de pontos mais proximo"
	p = l[0]; l = l[1::]
	l = MergeSort(l,p)

	fila = FilaEvento(l)

	#preprocessamento
	fila = MergeSort_ang(fila, p)
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
			if angle(f, p) == 0 and seno(f.getSeg().init, p) < 0:
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
		#l[i].hilight(color_line = "blue")		
		#control.sleep ()
		if ray.intersects(l[i]):
			root = myTree.insert(root,i, l[i])
			print('ADD: ', i)
			#l[i].hilight(color_line = "green")
		else:
			l[i].plot()
	ray.hide()

	minroot = myTree.getMinValueNode(root)
	if minroot != None:
		minroot.segment.hilight(color_line = "yellow")
	iguais = []
	for i in range(len(fila)):
		p1 = fila[i].getPoint().x
		p2 = fila[i].getPoint().y

		dist = fila[i].getIndex()
		froot = myTree.getNode(root, dist)
		if i != len(fila)-1 and angle(fila[i],p) == angle(fila[i+1],p):
			iguais.append(fila[i])
			if froot is None:
				root = myTree.insert(root, dist, l[dist])
				print('ADD iguais: ', dist)
		else:
			id = control.plot_ray(p.x, p.y, p1, p2, 'white')
			if len(iguais) !=0:
				iguais.append(fila[i])
				if froot is None:
					root = myTree.insert(root, dist, l[dist])
					print('ADD iguais: ', dist)
				minroot = myTree.getMinValueNode(root)
				if minroot != None:
					print('menor:',minroot.val)
					l[minroot.val].hilight(color_line = "yellow")
				for a in iguais:
					if a.getEsq() == False:
						root = myTree.delete(root, a.getIndex())
						print('DEL iguais: ', a.getIndex())

				minroot = myTree.getMinValueNode(root)
				if minroot != None:
					print('menor iniciando:',minroot.val)
					l[minroot.val].hilight(color_line = "yellow")
				iguais = []
				print("__________")
				control.sleep ()
				control.plot_delete(id)
				continue

			if froot is None:
			
				root = myTree.insert(root, dist, l[dist])
				#l[dist].hilight(color_line = "green")
				print('ADD: ', dist)
			else:
				root = myTree.delete(root, dist)
				print('DEL: ', dist)
				#l[dist].plot()

			minroot = myTree.getMinValueNode(root)
			if minroot != None:
				print('menor:',minroot.val)
				l[minroot.val].hilight(color_line = "yellow")
			print("__________")
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
			if (angle(L[i],p) <= angle(R[j],p) ): 
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

def MergeSort(arr,p): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]  

		MergeSort(L,p)  
		MergeSort(R,p)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if distPontoReta(p, L[i]) < distPontoReta(p, R[j]): 
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


def seno(s,p):
	seno = angle_(s,p)
	seno = math.sin(seno)
	return seno

def angle_(s,p):
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
	for i in range(len(l)):
		p1, p2 = l[i].endpoints()
		fila.append( PontoEvento(p1, l[i], True, i) )
		fila.append( PontoEvento(p2, l[i], False, i) )
	return fila

def distPontoReta(p, seg):
	p1, p2 = seg.endpoints()
	d = prim.dist2(p, p1)
	d1 = prim.dist2(p, p2)
	if d1 < d:
		d = d1
	pm = Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)
	d1 = prim.dist2(p,pm)
	if d1 < d:
		d = d1
	return (d)

