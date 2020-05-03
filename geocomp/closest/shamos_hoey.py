#!/usr/bin/env python
"""Algoritmo Shamos e Hoey"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math


def ShamosHoey (l):
	"Algoritmo Shamos E Hoey para encontrar o par de pontos mais proximo"

	if len (l) < 2: return None
	
	l = MergeSort(l)
	
	closest = float("inf")
	a = b = None
	id = None
	
	a,b,closest,id = DistanciaRecSH(l, 0, len(l), a, b, closest, id)
	
	a.hilight('green')
	b.hilight('green')
	ret = Segment(a, b)
	ret.hilight('blue')
	ret.extra_info = 'Distância: %.2f'%math.sqrt (closest)
	return ret

def MergeSort(arr): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]  

		MergeSort(L)  
		MergeSort(R)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if L[i].x < R[j].x: 
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
 
def Intercale(l, p, q, r):
	B = []
	for i in range(len(l)):
		B.append(0)
	B[p:q+1] = l[p:q+1]
	B2 = l[q+1:r]
	B2.reverse()
	B[q+1:r] = B2
	i=p; j = r-1
	for k in range(p,r):
		if B[i].y<= B[j].y:
			l[k] = B[i]
			i = i+1
		else:
			l[k] = B[j]
			j = j-1
	return l

def DistanciaRecSH (l, p, r, a, b, closest, id):
	if r <= p + 3:
		return distan(l, p, r, a, b, closest, id)
	else:
		q = math.floor(((p+r)/2))-1
		
		x = l[q].x
		id_ = control.plot_vert_line(x)
		control.sleep ()
		
		ae, be, de, ide =  DistanciaRecSH (l, p, q+1, a, b, closest, id)
		ad, bd, dd, idd =  DistanciaRecSH (l, q+1, r, a, b, closest, id)
		
		closest = min(de, dd)
		if de < dd:
			a = ae; b = be; id = ide
			control.plot_delete (idd)
		else:
			a = ad; b = bd; id = idd
			control.plot_delete (ide)
		
		id1 = control.plot_vert_line(x-math.sqrt(closest), 'orange')
		id2 = control.plot_vert_line(x+math.sqrt(closest), 'orange')
		
		l = Intercale(l, p, q, r)
		a,b, closest, id = Combine(l, p, r, a, b, closest, id, x)
		
		control.plot_delete(id1)
		control.plot_delete(id2)
		control.plot_delete(id_)
		control.sleep ()
		
		return (a, b, closest, id)

def distan(l, p, r, a, b, closest, id):
	for i in range (p,r):
		for j in range (i + 1, r):
			dist = dist2 (l[i], l[j])
			if dist < closest:
				control.freeze_update ()
				if id != None: control.plot_delete (id)

				closest = dist
				a = l[i]
				b = l[j]
				id = a.lineto (b)
				control.thaw_update() 
				control.update ()
	return (a, b, closest, id)

def Combine(l, p, r, a, b, closest, id, x):
	f = Candidatos(l, p, r,closest, x)
	t = len(f)
	
	for i in range(t-1):
		for j in range(i+1, min(i+7,t) ):
			dist = dist2 (l[f[i]], l[f[j]])
			if dist < closest:
				control.freeze_update ()
				if id != None: control.plot_delete (id)

				closest = dist
				a = l[f[i]]
				b = l[f[j]]

				id = a.lineto (b)
				control.thaw_update() 
				control.update ()
	return (a,b,closest,id)

def Candidatos(l, p, r,closest, x):
	f=[]
	for k in range(p,r):
		if abs(l[k].x - x) < math.sqrt(closest):
			f.append(k)
	return f