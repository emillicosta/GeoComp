# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Proximo:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles seja minima

Algoritmos disponveis:
- Forca bruta
"""
from . import visibility_point


children = (   ( 'visibility_point',  'VisibilityPoint', 'Visibilidade de ponto (com ABBB)'  ),
	)

__all__ = [a[0] for a in children]
