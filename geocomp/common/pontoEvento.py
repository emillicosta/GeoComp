class PontoEvento:
	def __init__(self, point, seg, esq, index, angle):
		self.point = point
		self.seg = seg
		self.esq = esq
		self.index = index
		self.angle = angle

	def getPoint(self):
		return self.point

	def getSeg(self):
		return self.seg

	def getEsq(self):
		return self.esq

	def setEsq(self, esq):
		self.esq = esq

	def getIndex(self):
		return self.index

	def setIndex(self, index):
		self.index = index