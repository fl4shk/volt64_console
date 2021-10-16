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

		self.numer = Signal(constants.MAIN_WIDTH())
		self.denom = Signal(constants.DENOM_WIDTH())

		if constants.PIPELINED():
			self.tag_in = Signal(constants.TAG_WIDTH())
		#--------
		# Outputs

		if not constants.PIPELINED():
			self.valid = Signal()

		self.quot = Signal(constants.MAIN_WIDTH())
		self.rema = Signal(constants.MAIN_WIDTH())

		if constants.PIPELINED():
			self.tag_out = Signal(constants.TAG_WIDTH())
		#--------
	#--------
	def constants(self):
		return self.__constants
	def shape_func(self):
		return self.__shape_func
	def build_main_data_t(self):
		return Signal(self.constants().MAIN_WIDTH())
	def build_denom_t(self):
		return Signal(self.constants().DENOM_WIDTH())
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
		constants = self.__constants
		bus = self.bus()

		zero_d = bus.denom == 0
		State = LongDivMultiCycle.State

		loc = Blank()
		# Submodules go here
		loc.m = [LongUdivIter(constants=constants)]
		m.submodules += loc.m
		loc.state = Signal(shape=Shape.cast(State), reset=State.IDLE,
			attrs=sig_keep())
		loc.numer_abs = bus.build_main_data_t()
		loc.denom_abs = bus.build_denom_t()
		loc.numer_was_lez = Signal()
		loc.denom_was_lez = Signal()

		loc.quot_will_be_lez = Signal()
		loc.rema_will_be_lez = Signal()

		quot_was_lez = Past(loc.quot_will_be_lez)
		rema_was_lez = Past(loc.rema_will_be_lez)

		if constants.FORMAL():
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

		#bus_szd_temp_q = itd_out.temp_quot[:len(bus.quot)]
		#bus_szd_temp_r = itd_out.temp_rema[:len(bus.rema)]

		#past_bus_szd_temp_q = Past(itd_out.temp_quot)[:len(bus.quot)]
		#past_bus_szd_temp_r = Past(itd_out.temp_rema)[:len(bus.rema)]
		bus_szd_temp_q = Signal(len(bus.quot))
		bus_szd_temp_r = Signal(len(bus.rema))

		lez_bus_szd_temp_q = Signal(len(bus.quot))
		lez_bus_szd_temp_r = Signal(len(bus.rema))

		#past_bus_szd_temp_q = Signal(len(bus.quot))
		#past_bus_szd_temp_r = Signal(len(bus.quot))
		#--------
		if constants.FORMAL():
			#--------
			m.d.sync += past_valid.eq(0b1)
			#--------
			skip_cond = itd_in.formal.formal_denom == 0
			#--------
		#--------
		m.d.comb \
		+= [
			loc.numer_abs.eq(Mux(bus.numer[-1], (~bus.numer) + 1,
				bus.numer)),
			loc.denom_abs.eq(Mux(bus.denom[-1], (~bus.denom) + 1,
				bus.denom)),

			loc.quot_will_be_lez.eq(loc.numer_was_lez
				!= loc.denom_was_lez),
			# Implement C's rules for remainder sign
			loc.rema_will_be_lez.eq(loc.numer_was_lez),

			bus_szd_temp_q.eq(itd_out.temp_quot[:len(bus.quot)]),
			bus_szd_temp_r.eq(itd_out.temp_rema[:len(bus.rema)]),

			lez_bus_szd_temp_q.eq((~bus_szd_temp_q) + 1),
			lez_bus_szd_temp_r.eq((~bus_szd_temp_r) + 1),
		]
		#m.d.sync \
		#+= [
		#	past_bus_szd_temp_q.eq(Past(bus_szd_temp_q)),
		#	past_bus_szd_temp_r.eq(Past(bus_szd_temp_r)),
		#]
		#--------
		with m.If(~ResetSignal()):
			with m.Switch(loc.state):
				with m.Case(State.IDLE):
					#--------
					m.d.sync \
					+= [
						loc.numer_was_lez.eq(bus.numer[-1]),
						loc.denom_was_lez.eq(bus.denom[-1]),

						chunk_start.eq(constants.NUM_CHUNKS() - 1),

						itd_in.temp_numer.eq(loc.numer_abs),
						itd_in.temp_quot.eq(0x0),
						itd_in.temp_rema.eq(0x0),
					]
					m.d.sync \
					+= [
						itd_in.denom_mult_lut[i].eq(loc.denom_abs * i)
							for i in range(constants.DML_SIZE())
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
						# not `constants.FORMAL()` is true.
						m.d.sync += itd_in.eq(itd_out)
					with m.Else(): # m.If(chunk_start <= 0):
						m.d.sync \
						+= [
							bus.quot.eq(Mux(loc.quot_will_be_lez,
								lez_bus_szd_temp_q,
								bus_szd_temp_q)),
							bus.rema.eq(Mux(loc.rema_will_be_lez,
								lez_bus_szd_temp_r,
								bus_szd_temp_r)),
							bus.valid.eq(0b1),

							loc.state.eq(State.IDLE),
						]
					m.d.sync \
					+= [
						chunk_start.eq(chunk_start - 1),
					]
					#--------
			if constants.FORMAL():
				with m.If(past_valid):
					m.d.comb \
					+= [
						Assume(Stable(loc.numer_abs)),
						Assume(Stable(loc.denom_abs)),
					]
				with m.Switch(loc.state):
					with m.Case(State.IDLE):
						m.d.sync \
						+= [
							itd_in.formal.formal_numer.eq(loc.numer_abs),
							itd_in.formal.formal_denom.eq(loc.denom_abs),

							itd_in.formal.oracle_quot
								.eq(loc.numer_abs // loc.denom_abs),
							itd_in.formal.oracle_rema
								.eq(loc.numer_abs % loc.denom_abs),
						]
						m.d.sync \
						+= [
							itd_in.formal_dml_elem(i).eq(loc.denom_abs * i)
								for i in range(constants.DML_SIZE())
						]
						with m.If(past_valid & (~Stable(loc.state))):
							m.d.comb \
							+= [
								#--------
								Assert(skip_cond
									| (bus.quot 
										== (Mux(quot_was_lez,
											Past(lez_bus_szd_temp_q),
											Past(bus_szd_temp_q))))),
								Assert(skip_cond
									| (bus.rema
										== (Mux(rema_was_lez,
											Past(lez_bus_szd_temp_r),
											Past(bus_szd_temp_r))))),
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
									== (constants.NUM_CHUNKS() - 1)),
								#--------
								Assert(itd_in.temp_numer
									== Past(loc.numer_abs)),
								Assert(itd_in.temp_quot == 0x0),
								Assert(itd_in.temp_rema == 0x0),
								#--------
								Assert(itd_in.formal.formal_numer
									== Past(loc.numer_abs)),
								Assert(itd_in.formal.formal_denom
									== Past(loc.denom_abs)),

								Assert(itd_in.formal.oracle_quot
									== (Past(loc.numer_abs)
										// Past(loc.denom_abs))),
								Assert(itd_in.formal.oracle_rema
									== (Past(loc.numer_abs)
										% Past(loc.denom_abs))),
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
									for i in range(constants.DML_SIZE())
							]
							m.d.comb \
							+= [
								Assert(itd_in.formal_dml_elem(i)
									== (itd_in.formal.formal_denom * i))
									for i in range(constants.DML_SIZE())
							]
		#--------
		return m
		#--------
	#--------
#--------
class LongDivPipelined(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False,
		*, shape_func=unsigned):
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
		self.__bus = LongDivBus(self.__constants, shape_func=shape_func)
	#--------
	def bus(self):
		return self.__bus
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		constants = self.__constants
		bus = self.bus()

		#NUM_PSTAGES = constants.NUM_CHUNKS() + 1
		NUM_PSTAGES = constants.NUM_CHUNKS()

		loc = Blank()

		# Submodules go here
		loc.m \
			= [
				LongUdivIterSync
				(
					constants=constants,
					chunk_start_val=(NUM_PSTAGES - 1) - i
				)
					for i in range(NUM_PSTAGES)
			]
		m.submodules += loc.m
		#--------
		if constants.FORMAL():
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
		if constants.FORMAL():
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
				for i in range(constants.DML_SIZE())
		]
		m.d.comb \
		+= [
			bus.quot.eq(itd_out[-1].temp_quot),
			bus.rema.eq(itd_out[-1].temp_rema),

			bus.tag_out.eq(itd_out[-1].tag)
		]
		if constants.FORMAL():
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
					for i in range(constants.DML_SIZE())
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
