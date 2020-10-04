#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

#--------
class LongUdivBus:
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH):
		#--------
		self.__MAIN_WIDTH, self.__DENOM_WIDTH = MAIN_WIDTH, DENOM_WIDTH
		#--------

		#--------
		# Inputs
		self.start = Signal()

		self.numer = Signal(self.MAIN_WIDTH())
		self.denom = Signal(self.DENOM_WIDTH())
		#--------

		#--------
		# Outputs
		self.valid = Signal()
		self.busy = Signal()

		self.quot = Signal(self.MAIN_WIDTH())
		self.rema = Signal(self.MAIN_WIDTH())
		#--------

	def MAIN_WIDTH(self):
		return self.__MAIN_WIDTH
	def DENOM_WIDTH(self):
		return self.__DENOM_WIDTH
#--------

#--------
class LongUdiv(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH):
		self.__bus = LongUdivBus \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH
			)
		self.__CHUNK_WIDTH = CHUNK_WIDTH
	#--------

	#--------
	def bus(self):
		return self.__bus
	def CHUNK_WIDTH(self):
		return self.__CHUNK_WIDTH

	def TEMP_T_WIDTH(self):
		return self.CHUNK_WIDTH() * ((self.bus().MAIN_WIDTH() \
			// self.CHUNK_WIDTH) + 2)
		#return self.CHUNK_WIDTH() * ((self.bus().MAIN_WIDTH() \
		#	// self.CHUNK_WIDTH) + 1)
	#--------

	#--------
	#def CHUNK_WIDTH(self):
	#	return 3

	#def TEMP_T_WIDTH(self):
	#	#return self.CHUNK_WIDTH() * ((self.bus().MAIN_WIDTH() \
	#	#	// self.CHUNK_WIDTH) + 2)
	#	return self.CHUNK_WIDTH() * ((self.bus().MAIN_WIDTH() \
	#		// self.CHUNK_WIDTH) + 1)

	#def NUM_CHUNKS(self):
	#	return self.TEMP_T_WIDTH() // self.CHUNK_WIDTH()
	#--------

	##--------
	## 2 ** 3 = 8 bits
	#def GT_VEC_WIDTH(self):
	#	return 2 ** self.CHUNK_WIDTH()

	#def bsearch(gt_vec):
	#	z = self.GT_VEC_WIDTH() // 2
	#	m = z

	#	while z > 0:
	#		temp = z // 2
	#		old_z = z
	#		z = temp

	#		if old_z == 1:
	#			temp = 1

	#		if (gt_vec & (1 << m)) == 1:
	#			m -= temp
	#		elif old_z > 1:
	#			m += temp
	#	return m

	## 2 ** 8 = 256 entries
	#def BSEARCH_LUT_SIZE(self):
	#	return 2 ** self.GT_VEC_WIDTH()

	#def BSEARCH_LUT(self):
	#	return Array([Const(self.bsearch(i), self.CHUNK_WIDTH())
	#		for i in range(self.BSEARCH_LUT_SIZE())])
	##--------

	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------

		#--------
		# Local variables
		bus = self.bus()

		loc = Blank()
		#--------

		#--------
		return m
		#--------
	#--------
#--------
