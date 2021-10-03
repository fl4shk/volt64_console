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

from volt32_cpu.long_udiv_pstage_mod import *


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
			#self.busy = Signal()

		self.quot = Signal(self.MAIN_WIDTH())
		self.rema = Signal(self.MAIN_WIDTH())

		if self.PIPELINED():
			self.tag_out = Signal(self.TAG_WIDTH())
		#--------
	#--------
	def MAIN_WIDTH(self):
		return self.__constants.MAIN_WIDTH()
	def DENOM_WIDTH(self):
		return self.__constants.DENOM_WIDTH()
	def CHUNK_WIDTH(self):
		return self.__constants.CHUNK_WIDTH()
	def TAG_WIDTH(self):
		return self.__constants.TAG_WIDTH()
	def PIPELINED(self):
		return self.__constants.PIPELINED()
	def FORMAL(self):
		return self.__constants.FORMAL()
	#--------
	def TEMP_T_WIDTH(self):
		return self.__constants.TEMP_T_WIDTH()

	def NUM_CHUNKS(self):
		return self.__constants.NUM_CHUNKS()

	def RADIX(self):
		return self.__constants.RADIX()
	#--------
	def DML_ELEM_WIDTH(self):
		return self.__constants.DML_ELEM_WIDTH()
	def DML_SIZE(self):
		return self.__constants.DML_SIZE()
	#--------
	def MAIN_MAX_VAL(self):
		return (1 << self.MAIN_WIDTH())
	def DENOM_MAX_VAL(self):
		return (1 << self.DENOM_WIDTH())
	#--------
#--------
class LongUdiv(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH,
		PIPELINED=False, FORMAL=False):
		self.__constants \
			= LongUdivConstants \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				# This `TAG_WIDTH` is just a heuristic
				TAG_WIDTH=math.log2(MAIN_WIDTH // CHUNK_WIDTH) + 2,
				PIPELINED=PIPELINED,
				FORMAL=FORMAL
			)
		self.__bus = LongUdivBus(constants=self.__constants)
	#--------
	def bus(self):
		return self.__bus

	def NUM_PSTAGES(self):
		return 1 \
			if not self.PIPELINED() \
			else self.NUM_CHUNKS()
	#--------
	class State(Enum):
		IDLE = 0
		RUNNING = auto()
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		bus = self.bus()

		loc = Blank()

		# Submodules go here
		loc.m = [LongUdivPstage(constants=self.__constants)
			for i in range(bus.NUM_PSTAGES())]
		m.submodules += loc.m

		# Connect the pipeline stages to one another.
		for i in range(self.NUM_PSTAGES() - 1):
			m.d.comb \
			+= [
				loc.m[i + 1].bus().psd_in.eq(loc.m[i].bus().psd_out)
			]

		if not bus.PIPELINED():
			loc.state = Signal(shape=Shape.cast(LongUdiv.State),
				reset=LongUdiv.State.IDLE, attrs=sig_keep())
		else: # if bus.PIPELINED():
			# Set the value of `ps_bus.chunk_start` for all the pstages if
			# we are pipelined 
			for i in range(self.NUM_PSTAGES()):
				ps_bus = loc.m[i].bus()
				m.d.comb \
				+= [
					ps_bus.chunk_start.eq((self.NUM_PSTAGES() - 1) - i)
				]
		#--------
		psd_in_first = loc.m[0].bus().psd_in
		psd_out_last = loc.m[-1].bus().psd_out

		m.d.comb \
		+= [
			#--------
			psd_in_first.temp_numer.eq(bus.numer),
			#psd_in_first.temp_quot.eq(0x0),
			#psd_in_first.temp_rema.eq(0x0),
			#--------
			bus.quot.eq(psd_out_last.temp_quot[:len(bus.quot)]),
			bus.rema.eq(psd_out_last.temp_rema[:len(bus.rema)]),
			#--------
		]
		for i in range(loc.m[0].bus().DML_SIZE()):
			m.d.comb \
			+= [
				psd_in_first.dml_elem(i).eq(bus.denom * i),
			]

		if bus.FORMAL():
			m.d.comb \
			+= [
				psd_in_first.formal.formal_numer.eq(bus.numer),
				psd_in_first.formal.formal_denom.eq(bus.denom),
				psd_in_first.formal.oracle_quot.eq(bus.numer // bus.denom),
				psd_in_first.formal.oracle_rema.eq(bus.numer % bus.denom),
			]
			for i in range(loc.m[0].bus().DML_SIZE()):
				m.d.comb \
				+= [
					psd_in_first.formal.formal_dml_elem(i)
						.eq(psd_in_first.formal.formal_denom * i),
				]
		#--------
		if not bus.PIPELINED():
			chunk_start_first = loc.m[0].bus().chunk_start

			with m.If(ResetSignal()):
				m.d.comb \
				+= [
					psd_in_first.temp_quot.eq(0x0),
					psd_in_first.temp_rema.eq(0x0),
				]
			with m.Else(): # If(~ResetSignal())
				with m.If(loc.state == LongUdiv.State.IDLE):
					m.d.comb \
					+= [
						psd_in_first.temp_quot.eq(0x0),
						psd_in_first.temp_rema.eq(0x0),
					]

					with m.If(bus.start):
						m.d.sync \
						+= [
							bus.valid.eq(0b0),
							chunk_start_first.eq(bus.NUM_CHUNKS() - 1),
							loc.state.eq(LongUdiv.State.RUNNING),
						]
				with m.Else(): # If(loc.state == LongUdiv.State.RUNNING):
					m.d.comb \
					+= [
						psd_in_first.temp_quot.eq(psd_out_last.temp_quot),
						psd_in_first.temp_rema.eq(psd_out_last.temp_rema),
					]

					with m.If(chunk_start >= 0x0):
						m.d.sync \
						+= [
							chunk_start_first.eq(chunk_start_first - 1)
						]
					with m.Else: # If(chunk_start_first < 0x0):
						m.d.sync \
						+= [
							bus.valid.eq(0b1),
							loc.state.eq(LongUdiv.State.IDLE)
						]
						
		else: # if bus.PIPELINED():
			m.d.comb \
			+= [
			]
		#--------
		return m
		#--------
	#--------
#--------
