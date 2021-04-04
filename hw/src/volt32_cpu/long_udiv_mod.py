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
	def NUM_PSTAGES(self):
		if not self.PIPELINED():
			return 1
		else: # if self.PIPELINED():
			return self.NUM_CHUNKS()
	def PS_ARR_SIZE(self):
		#return (self.NUM_PSTAGES() + 1)
		return self.NUM_PSTAGES()
	def psd_arr(self, elem_width, name_prefix):
		temp = []
		for i in range(self.PS_ARR_SIZE()):
			temp.append(Signal(elem_width, attrs=sig_keep(),
				name=f"{name_prefix}_{i}"))

		return Array(temp)
	#--------
#--------
class LongUdiv(Elaboratable)
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
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		bus = self.bus()

		loc = Blank()

		# Submodules go here
		loc.m = [LongUdivPstage(constants=self.__constants)
			for i in range(bus.NUM_PSTAGES()]
		m.submodules += loc.m

		loc.pa_temp_numer = bus.psd_arr(bus.TEMP_T_WIDTH(),
			"pa_temp_numer")
		loc.pa_temp_quot = bus.psd_arr(bus.TEMP_T_WIDTH(), "pa_temp_quot")
		loc.pa_temp_rema = bus.psd_arr(bus.TEMP_T_WIDTH(), "pa_temp_rema")
		loc.pa_denom_mult_lut \
			= bus.psd_arr(bus.DML_ELEM_WIDTH() * bus.DML_SIZE(),
			"pa_denom_mult_lut")

		if bus.PIPELINED():
			loc.pa_tag = bus.psd_arr(bus.TAG_WIDTH(), "pa_tag")

		if bus.FORMAL():
			#--------
			loc.formal = Blank()
			#--------
			loc.formal.pa_numer = bus.psd_arr(bus.TEMP_T_WIDTH(),
				"formal_pa_numer")
			loc.formal.pa_denom = bus.psd_arr(bus.DENOM_WIDTH(),
				"formal_pa_denom")

			loc.formal.pa_oracle_quot = bus.psd_arr(bus.TEMP_T_WIDTH(),
				"formal_pa_oracle_quot")
			loc.formal.pa_oracle_rema = bus.psd_arr(bus.TEMP_T_WIDTH(),
				"formal_pa_oracle_rema")
			#--------
			loc.formal.pa_denom_mult_lut \
				= bus.psd_arr(bus.DML_ELEM_WIDTH() * bus.DML_SIZE(),
					"formal_pa_denom_mult_lut")
			#--------

		#if not bus.PIPELINED():
		#	ps_bus = loc.m[0].bus()
		#	m.d.comb \
		#	+= [
		#		ps_bus
		#	]
		# Connect the pstages together
		#if bus.PIPELINED():
		#	for i in range(len(loc.m) - 1):
		#		curr_ps_bus = loc.m[i].bus()
		#		next_ps_bus = loc.m[i + 1].bus()
		#		m.d.comb \
		#		+= [
		#		]
		#--------
		# Connect the ports of the pstages

		#--------
		return m
		#--------
	#--------
#--------
