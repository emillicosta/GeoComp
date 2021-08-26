#!/usr/bin/env python
"""Algoritmo MergeHull"""

from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.avl import AVL
from geocomp.common.ray import Ray
from geocomp.common.point import Point
from geocomp.common.vector import Vector
from geocomp.common.segment import Segment
from geocomp.common.circularLinkedList import CircularLinkedList

import math

def MergeHull (l):

	if len (l) < 1: return None
	
	l = MergeSort(l)

	#Ignorando os repetidos
	L = []
	L.append(l[0])
	for i in range(1,len(l)):
		if l[i-1] != l[i]:
			L.append(l[i])

	MergeHullRec(L, 0, len(L))
	return None
	
def MergeSort(arr): 
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid]  
		R = arr[mid:]  

		MergeSort(L)  
		MergeSort(R)  

		i = j = k = 0

		while i < len(L) and j < len(R): 
			if L[i].x < R[j].x or (L[i].x == R[j].x and L[i].y < R[j].y) : 
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

def MergeHullRec(l, p, r):
	if r <= p + 1:
		H = CircularLinkedList()
		H.push(p)
		r3 = []
	else:
		q = math.floor(((p+r)/2))-1

		x = l[q].x
		id_ = control.plot_vert_line(x)

		H1,r1 = MergeHullRec(l, p, q+1)
		H2,r2 = MergeHullRec(l, q+1, r)
		DeletehHull(r1,r2)
		r1 = DrawHull(l,H1, "red")
		r2 = DrawHull(l,H2, "blue")
		H = JuntaHull(l, H1, H2)

		control.plot_delete(id_)
		DeletehHull(r1,r2)
		r3 = DrawHull(l,H)
	return H, r3

def DeletehHull(r1,r2):
	for i in range(len(r1)):
		control.plot_delete(r1[i])
	for j in range(len(r2)):
		control.plot_delete(r2[j])

def DrawHull(l,H, color="orange"):
	temp = H.head
	rets = []
	while(True):  
		a = l[temp.data];	b = l[temp.next.data]
		id = control.plot_segment(a.x, a.y, b.x, b.y, color)
		rets.append(id)
		temp = temp.next
		if (temp == H.head): 
			break
	return rets

def JuntaHull(l, H1, H2):
	h1b, h2b = TangenteInferior(l, H1, H2)
	a = l[h1b.data]; 	b = l[h2b.data]
	idb = control.plot_segment(a.x, a.y, b.x, b.y, "cyan")
	
	h1t, h2t = TangenteSuperior(l, H1, H2)
	a = l[h1t.data]; 	b = l[h2t.data]
	idt = control.plot_segment(a.x, a.y, b.x, b.y, "cyan")
	
	control.sleep()

	H = CircularLinkedList()
	H.push(h1t.data)

	
	i = h1t.next
	while i.prev.data != h1b.data:
		H.push(i.data);	i = i.next
	
	H.push(h2b.data)
	j = h2b.next
	while j.prev.data != h2t.data:
	 	H.push(j.data);	j = j.next

	control.plot_delete(idb)
	control.plot_delete(idt)

	return H

def TangenteInferior(l, H1, H2):
	h1x = float("-inf")
	h1y = float("inf")
	temp = H1.head
	h1 = temp
	while(True):
		if l[temp.data].x > h1x or (l[temp.data].x == h1x and l[temp.data].y < h1y):
			h1x = l[temp.data].x
			h1y = l[temp.data].y
			h1 = temp
		temp = temp.next
		if (temp == H1.head): 
			break

	h2x = float("inf")
	h2y = float("inf")
	temp = H2.head
	h2 = temp
	while(True):
		if l[temp.data].x < h2x or (l[temp.data].x == h2x and l[temp.data].y < h2y):
			h2x = l[temp.data].x
			h2y = l[temp.data].y
			h2 = temp
		temp = temp.next
		if (temp == H2.head): 
			break
	if H1.head != H1.head.next or H2.head != H2.head.next:
		while right(l[h1.data], l[h2.data], l[h1.prev.data]) or right(l[h1.data], l[h2.data], l[h2.next.data]):
			if H1.head != H1.head.next:
				while right(l[h1.data], l[h2.data], l[h1.prev.data]):
					h1 = h1.prev
			if H2.head != H2.head.next:
				while right(l[h1.data], l[h2.data], l[h2.next.data]):
					h2 = h2.next


	if H1.head != H1.head.next and collinear(l[h1.data], l[h2.data], l[h1.prev.data]):
		if l[h1.data].y > l[h1.prev.data].y:
			h1 = h1.prev
	if H2.head != H2.head.next and collinear(l[h1.data], l[h2.data], l[h2.next.data]):
		if l[h2.data].y > l[h2.next.data].y:
			h2 = h2.next
	return h1, h2

def TangenteSuperior(l, H1, H2):
	h1x = float("-inf")
	h1y = float("-inf")
	temp = H1.head
	h1 = temp
	while(True):
		if l[temp.data].x > h1x or (l[temp.data].x == h1x and l[temp.data].y > h1y):
			h1x = l[temp.data].x
			h1y = l[temp.data].y
			h1 = temp

		temp = temp.next
		if (temp == H1.head): 
			break

	h2x = float("inf")
	hey = float("-inf")
	temp = H2.head
	h2 = temp
	while(True):
		if l[temp.data].x < h2x or (l[temp.data].x == h2x and l[temp.data].y > h2y):
			h2x = l[temp.data].x
			h2y = l[temp.data].y
			h2 = temp
		temp = temp.next
		if (temp == H2.head): 
			break

	if H1.head != H1.head.next or H2.head != H2.head.next:
		while left(l[h1.data], l[h2.data], l[h1.next.data]) or left(l[h1.data], l[h2.data], l[h2.prev.data]):
			if H1.head != H1.head.next:
				while left(l[h1.data], l[h2.data], l[h1.next.data]):
					h1 = h1.next
			if H2.head != H2.head.next:
				while left(l[h1.data], l[h2.data], l[h2.prev.data]):
					h2 = h2.prev

	if H1.head != H1.head.next and collinear(l[h1.data], l[h2.data], l[h1.next.data]):
		if l[h1.data].y < l[h1.next.data].y:
			h1 = h1.next
	if H2.head != H2.head.next and collinear(l[h1.data], l[h2.data], l[h2.prev.data]):
		if l[h2.data].y < l[h2.prev.data].y:
			h2 = h2.prev
	return h1, h2
