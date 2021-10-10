#!/usr/bin/env python3

import math
from misc_util import *

from nmigen import *
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto

from general.container_types import *
from volt32_cpu.long_udiv_iter_mods import *
#--------
class LongUdivBus:
	#--------
	def __init__(self, constants):
		#--------
		self.__constants = constants
		#--------
		# Inputs

		if not self.PIPELINED():
			self.ready = Signal()

		self.numer = Signal(self.MAIN_WIDTH())
		self.denom = Signal(self.DENOM_WIDTH())

		if self.PIPELINED():
			self.tag_in = Signal(self.TAG_WIDTH())
		#--------
		# Outputs

		if not self.PIPELINED():
			self.valid = Signal()

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
class LongUdivMultiCycle(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False):
		self.__constants \
			= LongUdivConstants \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				PIPELINED=False,
				FORMAL=FORMAL,
			)
		self.__bus = LongUdivBus(self.__constants)
	#--------
	def bus(self):
		return self.__bus
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

		zero_d = (bus.denom == 0)

		State = LongUdivMultiCycle.State

		loc = Blank()

		# Submodules go here
		loc.m = [LongUdivIter(constants=self.__constants)]
		m.submodules += loc.m

		loc.state = Signal(shape=Shape.cast(State),
			reset=State.IDLE, attrs=sig_keep())

		if bus.FORMAL():
			loc.formal = Blank()
			loc.formal.past_valid \
				= Signal \
				(
					attrs=sig_keep(),
					name="formal_past_valid"
				)
			past_valid = loc.formal.past_valid
		#--------
		its_bus = loc.m[0].bus()
		chunk_start = its_bus.chunk_start
		itd_in = its_bus.itd_in
		itd_out = its_bus.itd_out
		#--------
		if bus.FORMAL():
			#--------
			m.d.sync += past_valid.eq(0b1)
			#--------
			skip_cond = (itd_in.formal.formal_denom == 0)
			#--------
		#--------
		with m.If(~ResetSignal()):
			if bus.FORMAL():
				with m.If(past_valid):
					m.d.comb \
					+= [
						Assume(Stable(bus.numer)),
						Assume(Stable(bus.denom)),
					]
			with m.Switch(loc.state):
				with m.Case(State.IDLE):
					#--------
					m.d.sync \
					+= [
						chunk_start.eq(bus.NUM_CHUNKS() - 1),

						itd_in.temp_numer.eq(bus.numer),
						itd_in.temp_quot.eq(0x0),
						itd_in.temp_rema.eq(0x0),
					]
					m.d.sync \
					+= [
						itd_in.denom_mult_lut[i].eq(bus.denom * i)
							for i in range(bus.DML_SIZE())
					]
					#--------
					if bus.FORMAL():
						m.d.sync \
						+= [
							itd_in.formal.formal_numer.eq(bus.numer),
							itd_in.formal.formal_denom.eq(bus.denom),

							itd_in.formal.oracle_quot
								.eq(bus.numer // bus.denom),
							itd_in.formal.oracle_rema
								.eq(bus.numer % bus.denom),
						]
						m.d.sync \
						+= [
							itd_in.formal.formal_denom_mult_lut[i]
								.eq(bus.denom * i)
								for i in range(bus.DML_SIZE())
						]
					#--------
					with m.If(bus.ready):
						m.d.sync \
						+= [
							bus.quot.eq(0x0),
							bus.rema.eq(0x0),
							bus.valid.eq(0b0),

							loc.state.eq(State.RUNNING),
						]
					#--------
					if bus.FORMAL():
						with m.If(past_valid & (~Stable(loc.state))):
							m.d.comb \
							+= [
								#--------
								Assert(skip_cond
									| (bus.quot
										== Past(itd_out.temp_quot))),
								Assert(skip_cond
									| (bus.rema
										== Past(itd_out.temp_rema))),
								Assert(bus.valid),
								#--------
							]
						#with m.Elif(past_valid & Stable(loc.state)):
					#--------
				with m.Case(State.RUNNING):
					#--------
					with m.If(chunk_start > 0):
						# Since `itd_in` and `itd_out` are `Splitrec`s, we
						# can do a simple `.eq()` regardless of whether or
						# not `bus.FORMAL()` is true.
						m.d.sync += itd_in.eq(itd_out)

					with m.Else(): # m.If(chunk_start <= 0):
						m.d.sync \
						+= [
							bus.quot.eq(itd_out.temp_quot),
							bus.rema.eq(itd_out.temp_rema),
							bus.valid.eq(0b1),

							loc.state.eq(State.IDLE),
						]
					m.d.sync \
					+= [
						chunk_start.eq(chunk_start - 1),
					]
					#--------
					if bus.FORMAL():
						with m.If(past_valid & (~Stable(loc.state))):
							m.d.comb \
							+= [
								#--------
								Assert(chunk_start
									== (bus.NUM_CHUNKS() - 1)),
								#--------
								Assert(itd_in.temp_numer
									== Past(bus.numer)),
								Assert(itd_in.temp_quot == 0x0),
								Assert(itd_in.temp_rema == 0x0),
								#--------
								Assert(itd_in.formal.formal_numer
									== Past(bus.numer)),
								Assert(itd_in.formal.formal_denom
									== Past(bus.denom)),

								Assert(itd_in.formal.oracle_quot
									== (Past(bus.numer)
										// Past(bus.denom))),
								Assert(itd_in.formal.oracle_rema
									== (Past(bus.numer)
										% Past(bus.denom))),
								#--------
							]

						with m.Elif(past_valid & Stable(loc.state)):
							m.d.comb \
							+= [
								#--------
								Assert(chunk_start
									== (Past(chunk_start) - 1)),
								#--------
								Assert(itd_out.temp_numer
									== Past(itd_in.temp_numer)),

								#Assert(itd_out.temp_quot
								#	== Past(bus.temp_quot)),
								#Assert(itd_out.temp_rema
								#	== Past(bus.temp_rema)),
								#Assert(itd_out.temp_quot
								#	== Past(itd_out.temp_quot)),
								#Assert(itd_out.temp_rema
								#	== Past(itd_out.temp_rema)),
								#--------
								Assert(itd_out.denom_mult_lut
									== Past(itd_in.denom_mult_lut)),
								#--------
								Assert(itd_out.formal.formal_numer
									== Past(itd_in.formal.formal_numer)),
								Assert(itd_out.formal.formal_denom
									== Past(itd_in.formal.formal_denom)),

								Assert(itd_out.formal.oracle_quot
									== Past(itd_in.formal.oracle_quot)),
								Assert(itd_out.formal.oracle_rema
									== Past(itd_in.formal.oracle_rema)),
								#--------
								Assert(itd_out.formal
									.formal_denom_mult_lut
									== Past(itd_in.formal
										.formal_denom_mult_lut)),
								#--------
							]

						with m.If(past_valid):
							m.d.comb \
							+= [
								Assert(itd_in.denom_mult_lut[i]
									== (itd_in.formal.formal_denom * i))
									for i in range(bus.DML_SIZE())
							]
							m.d.comb \
							+= [
								Assert(itd_in.formal_dml_elem(i)
									== (itd_in.formal.formal_denom * i))
									for i in range(bus.DML_SIZE())
							]
					#--------
		#--------
		return m
		#--------
	#--------
#--------
