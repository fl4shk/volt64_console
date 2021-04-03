#!/usr/bin/env python3

import math
from misc_util import *
from volt32_cpu.long_udiv_pstage_mod import *

from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto


#--------
class LongUdivBus:
	#--------
	def __init__(self, constants):
		#--------
		self.__constants = constants
		#--------
		# Inputs

		if not self.PIPELINED():
			self.start = Signal()

		self.numer = Signal(self.MAIN_WIDTH())
		self.denom = Signal(self.DENOM_WIDTH())

		if self.PIPELINED():
			self.tag_in = Signal(self.TAG_WIDTH())
		#--------
		# Outputs

		if not self.PIPELINED():
			self.valid = Signal()
			self.busy = Signal()

		self.quot = Signal(self.MAIN_WIDTH())
		self.rema = Signal(self.MAIN_WIDTH())

		if self.PIPELINED():
			self.tag_out = Signal(self.TAG_WIDTH())
		#--------
	#--------
	def MAIN_WIDTH(self):
		return self.__constants.MAIN_WIDTH()
	def MAIN_MAX_VAL(self):
		return (1 << self.MAIN_WIDTH())

	def DENOM_WIDTH(self):
		return self.__constants.DENOM_WIDTH()
	def DENOM_MAX_VAL(self):
		return (1 << self.DENOM_WIDTH())

	def CHUNK_WIDTH(self):
		return self.__constants.CHUNK_WIDTH()
	#def TAG_WIDTH(self):
	#	return (math.log2(self.MAIN_WIDTH() // self.CHUNK_WIDTH()) + 2)
	def TAG_WIDTH(self):
		return self.__constants.TAG_WIDTH()

	def NUM_CHUNKS(self):
		return (self.TEMP_T_WIDTH() // self.CHUNK_WIDTH())

	def PIPELINED(self):
		return self.__constants.PIPELINED()

	def FORMAL(self):
		return self.__constants.FORMAL()
	#--------
#--------
class LongUdiv(Elaboratable)
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH,
		PIPELINED=False, FORMAL=False):
		constants \
			= LongUdivConstants \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				TAG_WIDTH=math.log2(MAIN_WIDTH // CHUNK_WIDTH) + 2,
				PIPELINED=PIPELINED,
				FORMAL=FORMAL
			)
		self.__bus \
			= LongUdivBus \
			(
				constants=constants
			)
	#--------
	def bus(self):
		return self.__bus
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		bus = self.bus()

		loc = Blank()

		# Submodules go here
		loc.m = m.submodules

		if not bus.PIPELINED():
			loc.m.pstage = LongUdivPstage
		else: # if bus.PIPELINED():
			
		#--------
		return m
		#--------
	#--------
#--------
