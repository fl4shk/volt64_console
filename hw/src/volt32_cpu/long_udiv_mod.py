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

	def NUM_PSTAGES(self):
		return 1 \
			if not self.PIPELINED() \
			else self.NUM_CHUNKS()
	def PSD_LST_SIZE(self):
		return (self.NUM_PSTAGES() + 1)
	def psd_lst(self, elem_width, name_prefix):
		ret = []
		for i in range(self.PSD_LST_SIZE()):
			ret.append(Signal(elem_width, attrs=sig_keep(),
				name=f"{name_prefix}_{i}"))
		return ret
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

		loc.pl_temp_numer = self.psd_lst(bus.TEMP_T_WIDTH(),
			"pl_temp_numer")
		loc.pl_temp_quot = self.psd_lst(bus.TEMP_T_WIDTH(), "pl_temp_quot")
		loc.pl_temp_rema = self.psd_lst(bus.TEMP_T_WIDTH(), "pl_temp_rema")
		loc.pl_denom_mult_lut \
			= bus.psd_lst(bus.DML_ELEM_WIDTH() * bus.DML_SIZE(),
			"pl_denom_mult_lut")

		if bus.PIPELINED():
			loc.pl_tag = self.psd_lst(bus.TAG_WIDTH(), "pl_tag")

		if bus.FORMAL():
			#--------
			loc.formal = Blank()
			#--------
			loc.formal.pl_formal_numer = self.psd_lst(bus.TEMP_T_WIDTH(),
				"pl_formal_numer")
			loc.formal.pl_formal_denom = self.psd_lst(bus.DENOM_WIDTH(),
				"pl_formal_denom")

			loc.formal.pl_oracle_quot = self.psd_lst(bus.TEMP_T_WIDTH(),
				"pl_oracle_quot")
			loc.formal.pl_oracle_rema = self.psd_lst(bus.TEMP_T_WIDTH(),
				"pl_oracle_rema")
			#--------
			loc.formal.pl_formal_denom_mult_lut \
				= self.psd_lst(bus.DML_ELEM_WIDTH() * bus.DML_SIZE(),
					"pl_formal_denom_mult_lut")
			#--------

		# Connect the pstages together
		def connect_ports(bus, loc, i)
			ps_bus = loc.m[i].bus()
			psd_in = ps_bus.psd_in
			psd_out = ps_bus.psd_out

			m.d.comb \
			+= [
				#--------
				psd_in.temp_numer.eq(loc.pl_temp_numer[i]),
				loc.pl_temp_numer[i + 1].eq(psd_out.temp_numer),
				#--------
				psd_in.temp_quot.eq(loc.pl_temp_quot[i]),
				loc.pl_temp_quot[i + 1].eq(psd_out.temp_quot),
				#--------
				psd_in.temp_rema.eq(loc.pl_temp_rema[i]),
				loc.pl_temp_rema[i + 1].eq(psd_out.temp_rema),
				#--------
				psd_in.denom_mult_lut.eq(loc.pl_denom_mult_lut[i]),
				loc.pl_denom_mult_lut[i + 1]
					.eq(psd_out.denom_mult_lut),
				#--------
			]

			if bus.PIPELINED()():
				m.d.comb \
				+= [
					#--------
					psd_in.tag.eq(loc.pl_tag[i]),
					loc.pl_tag[i + 1].eq(psd_out.tag),
					#--------
				]

			if bus.FORMAL():
				m.d.comb \
				+= [
					#--------
					psd_in.formal.formal_numer
						.eq(loc.formal.pl_formal_numer[i]),
					loc.formal.pl_formal_numer[i + 1]
						.eq(psd_out.formal.formal_numer),
					#--------
					psd_in.formal.formal_denom
						.eq(loc.formal.pl_formal_denom[i]),
					loc.formal.pl_formal_denom[i + 1]
						.eq(psd_out.formal.formal_denom),
					#--------
					psd_in.formal.oracle_quot
						.eq(loc.formal.pl_oracle_quot[i]),
					loc.formal.pl_oracle_quot[i + 1]
						.eq(psd_out.formal.oracle_quot),
					#--------
					psd_in.formal.oracle_rema
						.eq(loc.formal.pl_oracle_rema[i]),
					loc.formal.pl_oracle_rema[i + 1]
						.eq(psd_out.formal.oracle_rema),
					#--------
					psd_in.formal.formal_denom_mult_lut
						.eq(loc.formal.pl_formal_denom_mult_lut[i]),
					loc.formal.pl_formal_denom_mult_lut[i + 1]
						.eq(psd_out.formal.formal_denom_mult_lut),
					#--------
				]

		for i in range(self.NUM_PSTAGES()):
			connect_ports \
			(
				bus=bus,
				loc=loc,
				i=i
			)

		# Set the value of `ps_bus.chunk_start` for all the pstages if we
		# are pipelined 
		if bus.PIPELINED():
			for i in range(self.NUM_PSTAGES()):
				ps_bus = loc.m[i].bus()
				m.d.comb \
				+= [
					ps_bus.chunk_start.eq((self.NUM_PSTAGES() - 1) - i)
				]
		#--------
		# Code implementing the state machine
		if not bus.PIPELINED():
			with m.If(ResetSignal()):
			with m.Else(): # If(~ResetSignal()):
		else: # if bus.PIPELINED():
			with m.If(~ResetSignal()):
				m.d.comb \
				+= [
				]
		#--------
		return m
		#--------
	#--------
#--------
