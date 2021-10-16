#!/usr/bin/env python3

import math
from misc_util import *

from nmigen import *
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto

from general.container_types import *
from volt32_cpu.long_div_iter_mods import *
#--------
class LongDivBus:
	#--------
	def __init__(self, constants, *, shape_func=unsigned):
		#--------
		self.__constants = constants
		self.__shape_func = shape_func
		#--------
		# Inputs

		if not constants.PIPELINED():
			self.ready = Signal()

		self.numer = Signal(shape_func(constants.MAIN_WIDTH()))
		self.denom = Signal(shape_func(constants.DENOM_WIDTH()))

		if constants.PIPELINED():
			self.tag_in = Signal(constants.TAG_WIDTH())
		#--------
		# Outputs

		if not constants.PIPELINED():
			self.valid = Signal()

		self.quot = Signal(shape_func(constants.MAIN_WIDTH()))
		self.rema = Signal(shape_func(constants.MAIN_WIDTH()))

		if constants.PIPELINED():
			self.tag_out = Signal(constants.TAG_WIDTH())
		#--------
	#--------
	def constants(self):
		return self.__constants
	def shape_func(self):
		return self.__shape_func
	#--------
#--------
class LongDivMultiCycle(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False,
		*, shape_func=unsigned):
		self.__constants \
			= LongDivConstants \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				PIPELINED=False,
				FORMAL=FORMAL,
			)
		self.__bus = LongDivBus(self.__constants, shape_func=shape_func)
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

		zero_d = bus.denom == 0
		State = LongDivMultiCycle.State

		loc = Blank()
		# Submodules go here
		loc.m = [LongUdivIter(constants=self.__constants)]
		m.submodules += loc.m
		loc.state = Signal(shape=Shape.cast(State),
			reset=State.IDLE, attrs=sig_keep())

		if bus.constants().FORMAL():
			loc.formal = Blank()
			loc.formal.past_valid \
				= Signal \
				(
					attrs=sig_keep(),
					name="formal_past_valid"
				)
			past_valid = loc.formal.past_valid
		#--------
		it_bus = loc.m[0].bus()
		chunk_start = it_bus.chunk_start
		itd_in = it_bus.itd_in
		itd_out = it_bus.itd_out
		#--------
		if bus.constants().FORMAL():
			#--------
			m.d.sync += past_valid.eq(0b1)
			#--------
			skip_cond = itd_in.formal.formal_denom == 0
			#--------
		#--------
		with m.If(~ResetSignal()):
			with m.Switch(loc.state):
				with m.Case(State.IDLE):
					#--------
					m.d.sync \
					+= [
						chunk_start.eq(bus.constants().NUM_CHUNKS() - 1),

						itd_in.temp_numer.eq(bus.numer),
						itd_in.temp_quot.eq(0x0),
						itd_in.temp_rema.eq(0x0),
					]
					m.d.sync \
					+= [
						itd_in.denom_mult_lut[i].eq(bus.denom * i)
							for i in range(bus.constants().DML_SIZE())
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
				with m.Case(State.RUNNING):
					#--------
					with m.If(chunk_start > 0):
						# Since `itd_in` and `itd_out` are `Splitrec`s, we
						# can do a simple `.eq()` regardless of whether or
						# not `bus.constants().FORMAL()` is true.
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
			if bus.constants().FORMAL():
				with m.If(past_valid):
					m.d.comb \
					+= [
						Assume(Stable(bus.numer)),
						Assume(Stable(bus.denom)),
					]
				with m.Switch(loc.state):
					with m.Case(State.IDLE):
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
							itd_in.formal_dml_elem(i).eq(bus.denom * i)
								for i in range(bus.constants().DML_SIZE())
						]
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
					with m.Case(State.RUNNING):
						with m.If(past_valid & (~Stable(loc.state))):
							m.d.comb \
							+= [
								#--------
								Assert(chunk_start
									== (bus.constants().NUM_CHUNKS() - 1)),
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
									for i in range
										(bus.constants().DML_SIZE())
							]
							m.d.comb \
							+= [
								Assert(itd_in.formal_dml_elem(i)
									== (itd_in.formal.formal_denom * i))
									for i in range
										(bus.constants().DML_SIZE())
							]
		#--------
		return m
		#--------
	#--------
#--------
class LongDivPipelined(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False):
		self.__constants \
			= LongDivConstants \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				# This `TAG_WIDTH` is just a heuristic
				TAG_WIDTH=math.ceil(math.log2(MAIN_WIDTH // CHUNK_WIDTH)
					+ 2),
				PIPELINED=True,
				FORMAL=FORMAL
			)
		self.__bus = LongDivBus(self.__constants)
	#--------
	def bus(self):
		return self.__bus
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		bus = self.bus()

		#NUM_PSTAGES = bus.constants().NUM_CHUNKS() + 1
		NUM_PSTAGES = bus.constants().NUM_CHUNKS()

		loc = Blank()

		# Submodules go here
		loc.m \
			= [
				LongUdivIterSync
				(
					constants=self.__constants,
					chunk_start_val=(NUM_PSTAGES - 1) - i
				)
					for i in range(NUM_PSTAGES)
			]
		m.submodules += loc.m
		#--------
		if bus.constants().FORMAL():
			loc.formal = Blank()
			loc.formal.past_valid \
				= Signal \
				(
					attrs=sig_keep(),
					name="formal_past_valid"
				)
			past_valid = loc.formal.past_valid
		#--------
		its_bus = [loc.m[i].bus() for i in range(len(loc.m))]

		itd_in = [its_bus[i].itd_in for i in range(len(loc.m))]
		itd_out = [its_bus[i].itd_out for i in range(len(loc.m))]
		#--------
		# Connect the pipeline stages together
		m.d.comb \
		+= [
			itd_in[i + 1].eq(itd_out[i]) for i in range(len(loc.m) - 1)
		]
		#--------
		if bus.constants().FORMAL():
			#--------
			m.d.sync += past_valid.eq(0b1)
			#--------
			skip_cond = itd_out[-1].formal.formal_denom == 0
			#--------
		#--------
		m.d.sync \
		+= [
			itd_in[0].temp_numer.eq(bus.numer),

			itd_in[0].temp_quot.eq(0x0),
			itd_in[0].temp_rema.eq(0x0),

			itd_in[0].tag.eq(bus.tag_in),
		]
		m.d.sync \
		+= [
			itd_in[0].denom_mult_lut[i].eq(bus.denom * i)
				for i in range(bus.constants().DML_SIZE())
		]
		m.d.comb \
		+= [
			bus.quot.eq(itd_out[-1].temp_quot),
			bus.rema.eq(itd_out[-1].temp_rema),

			bus.tag_out.eq(itd_out[-1].tag)
		]
		if bus.constants().FORMAL():
			m.d.sync \
			+= [
				itd_in[0].formal.formal_numer.eq(bus.numer),
				itd_in[0].formal.formal_denom.eq(bus.denom),

				itd_in[0].formal.oracle_quot.eq(bus.numer // bus.denom),
				itd_in[0].formal.oracle_rema.eq(bus.numer % bus.denom),
			]
			m.d.sync \
			+= [
				itd_in[0].formal_dml_elem(i).eq(bus.denom * i)
					for i in range(bus.constants().DML_SIZE())
			]
			with m.If((~ResetSignal()) & past_valid):
				m.d.comb \
				+= [
					#--------
					Assert(itd_in[0].temp_numer == Past(bus.numer)),
					Assert(itd_in[0].temp_quot == 0x0),
					Assert(itd_in[0].temp_rema == 0x0),
					#--------
					Assert(itd_in[0].formal.formal_numer
						== Past(bus.numer)),
					Assert(itd_in[0].formal.formal_denom
						== Past(bus.denom)),

					Assert(itd_in[0].formal.oracle_quot
						== (Past(bus.numer) // Past(bus.denom))),
					Assert(itd_in[0].formal.oracle_rema
						== (Past(bus.numer) % Past(bus.denom))),
					#--------
					Assert(skip_cond
						| (itd_out[-1].temp_quot
							== itd_out[-1].formal.oracle_quot)),
					Assert(skip_cond
						| (itd_out[-1].temp_rema
							== itd_out[-1].formal.oracle_rema)),
					#--------
				]
		#--------
		return m
		#--------
	#--------
#--------
