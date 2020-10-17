#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto

#--------
class LongUdivBus:
	#--------
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
	#--------

	#--------
	def MAIN_WIDTH(self):
		return self.__MAIN_WIDTH
	def MAIN_MAX_VAL(self):
		return (1 << self.MAIN_WIDTH())

	def DENOM_WIDTH(self):
		return self.__DENOM_WIDTH
	def DENOM_MAX_VAL(self):
		return (1 << self.DENOM_WIDTH())
	#--------
#--------

#--------
class LongUdiv(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False,
		DBG=False):
		self.__bus = LongUdivBus \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH
			)
		self.__CHUNK_WIDTH, self.__FORMAL, self.__DBG \
			= CHUNK_WIDTH, FORMAL, DBG
	#--------

	#--------
	def bus(self):
		return self.__bus
	#--------

	#--------
	def MAIN_WIDTH(self):
		return self.bus().MAIN_WIDTH()
	def DENOM_WIDTH(self):
		return self.bus().DENOM_WIDTH()
	#--------

	#--------
	def CHUNK_WIDTH(self):
		return self.__CHUNK_WIDTH

	def FORMAL(self):
		return self.__FORMAL
	def DBG(self):
		return self.__DBG
	#--------

	#--------
	def TEMP_T_WIDTH(self):
		#return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
		#	// self.CHUNK_WIDTH()) + 2))
		return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
			// self.CHUNK_WIDTH()) + 1))

	#def NUM_CHUNKS(self):
	#	return (self.TEMP_T_WIDTH() // self.CHUNK_WIDTH())

	def NUM_DIGITS_PER_CHUNK(self):
		return (1 << self.CHUNK_WIDTH())
	def DENOM_MULT_LUT_ENTRY_WIDTH(self):
		return (self.DENOM_WIDTH() + self.CHUNK_WIDTH())
	#--------

	#--------
	def verify_process(self):
		bus = self.bus()
		for numer in range(bus.MAIN_MAX_VAL()):
		#for numer in range(4, bus.MAIN_MAX_VAL()):
			for denom in range(1, bus.DENOM_MAX_VAL()):
				yield bus.start.eq(0b1)
				yield bus.numer.eq(numer)
				yield bus.denom.eq(denom)
				yield Tick("sync")


				yield bus.start.eq(0b0)
				yield Tick("sync")

				# Parentheses are there to make `yield whatever` an
				# expression.
				while (yield bus.busy):
					yield Tick("sync")

				bus_quot = (yield bus.quot)
				bus_rema = (yield bus.rema)
				oracle_quot = (numer // denom)
				oracle_rema = (numer % denom)

				print("{} op {}; {} {}; {} {}; {} {}".format
					(hex(numer), hex(denom),
					hex(bus_quot), hex(bus_rema),
					hex(oracle_quot), hex(oracle_rema),
					(bus_quot == oracle_quot), (bus_rema == oracle_rema)))
			print()
	#--------

	#--------
	def _build_loc(self):
		#--------
		loc = Blank()
		#--------

		#--------
		loc.rst = ResetSignal()

		# Numerator as a `temp_t`
		loc.temp_numer = Signal(self.TEMP_T_WIDTH())

		# Current quotient digit
		loc.quot_digit = Signal(self.CHUNK_WIDTH())

		# Quotient as a `temp_t`
		loc.temp_quot = Signal(self.TEMP_T_WIDTH())

		# Remainder as a `temp_t`
		loc.temp_rema = Signal(self.TEMP_T_WIDTH())

		# The array of (denominator * possible_digit) values
		loc.denom_mult_lut = Array \
			([Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH(), attrs={"keep": 1})
			for _ in range(self.NUM_DIGITS_PER_CHUNK())])

		# Remainder with the current chunk of `temp_numer` shifted in
		loc.shift_in_rema = Signal(self.TEMP_T_WIDTH())

		# The start of the range of bits of the current chunk of
		# `temp_numer`
		loc.chunk_start = Signal(self.CHUNK_WIDTH())

		# The vector of greater than comparison values
		loc.gt_vec = Signal(self.NUM_DIGITS_PER_CHUNK(), attrs={"keep": 1})
		#--------


		#--------
		if self.FORMAL():
			#--------
			loc.formal = Blank()
			#--------

			#--------
			loc.formal.past_valid = Signal(reset=0b0, attrs={"keep": 1})
			#--------

			#--------
			loc.formal.formal_numer = Signal(self.TEMP_T_WIDTH(),
				attrs={"keep": 1})
			loc.formal.formal_denom = Signal(self.DENOM_WIDTH(),
				attrs={"keep": 1})

			loc.formal.oracle_quot = Signal(self.TEMP_T_WIDTH(),
				attrs={"keep": 1})
			loc.formal.oracle_rema = Signal(self.TEMP_T_WIDTH(),
				attrs={"keep": 1})
			#--------

			#--------
			loc.formal.denom_mult_lut_lst = []
			for i in range(self.NUM_DIGITS_PER_CHUNK()):
				loc.formal.denom_mult_lut_lst.append \
					(Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH(),
						name=f"denom_mult_lut_{i}", attrs={"keep": 1}))
			#--------
		#--------

		#--------
		if self.DBG():
			#--------
			loc.dbg = Blank()
			#--------

			#--------
			loc.dbg.dbg_quot = Signal(self.TEMP_T_WIDTH())
			loc.dbg.dbg_rema = Signal(self.TEMP_T_WIDTH())
			#--------

			#--------
			loc.dbg.denom_mult_lut_lst = []
			for i in range(self.NUM_DIGITS_PER_CHUNK()):
				loc.dbg.denom_mult_lut_lst.append \
					(Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH(),
						name=f"dbg_denom_mult_lut_{i}"))
			#--------
		#--------

		#--------
		return loc
		#--------
	#--------

	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		#--------
		# Local variables
		bus = self.bus()

		loc = self._build_loc()

		TEMP_T_WIDTH = self.TEMP_T_WIDTH()
		CHUNK_WIDTH = self.CHUNK_WIDTH()
		#--------

		#--------
		# Shift in the current chunk of `loc.temp_numer`
		m.d.comb \
		+= [
			loc.shift_in_rema.eq(Cat(loc.temp_numer.word_select
				(loc.chunk_start, CHUNK_WIDTH),
				loc.temp_rema[:TEMP_T_WIDTH - CHUNK_WIDTH])),
		]

		# Compare every element of the computed `denom * digit` array to
		# `shift_in_rema`, computing `gt_vec`.
		# This creates around a single LUT delay for the comparisons given
		# the existence of hard carry chains in FPGAs.
		for i in range(self.NUM_DIGITS_PER_CHUNK()):
			m.d.comb += loc.gt_vec[i].eq(loc.denom_mult_lut[i] 
				> loc.shift_in_rema)

		# Find the current quotient digit with something resembling a
		# priority encoder.
		with m.Switch(loc.gt_vec):
			for i in range(len(loc.gt_vec)):
				with m.Case(("1" * (len(loc.gt_vec) - (i + 1)))
					+ ("0" * (i + 1))):
					m.d.comb += loc.quot_digit.eq(i)
			with m.Default():
				m.d.comb += loc.quot_digit.eq(0)

			#with m.Case("1110"):
			#	m.d.comb += loc.quot_digit.eq(0)
			#with m.Case("1100"):
			#	m.d.comb += loc.quot_digit.eq(1)
			#with m.Case("1000"):
			#	m.d.comb += loc.quot_digit.eq(2)
			#with m.Case("0000"):
			#	m.d.comb += loc.quot_digit.eq(3)
			#with m.Default():
			#	m.d.comb += loc.quot_digit.eq(0)


		m.d.comb \
		+= [
			bus.quot.eq(loc.temp_quot[:len(bus.quot)]),
			bus.rema.eq(loc.temp_rema[:len(bus.rema)]),
		]
		#--------

		#--------
		if self.DBG():
			for i in range(len(loc.dbg.denom_mult_lut_lst)):
				m.d.comb \
				+= [
					loc.dbg.denom_mult_lut_lst[i]
						.eq(loc.denom_mult_lut[i])
				]
		#--------

		#--------
		with m.If(~loc.rst):
			#--------
			# If we're starting a divide
			with m.If(~bus.busy):
				#--------
				with m.If(bus.start):
					#--------
					m.d.sync \
					+= [
						bus.valid.eq(0b0),
						bus.busy.eq(0b1),

						loc.temp_numer.eq(bus.numer),

						loc.temp_quot.eq(0x0),
						loc.temp_rema.eq(0x0),

						loc.chunk_start.eq(CHUNK_WIDTH - 1)
					]

					# Compute the array of `(denom * digit)`
					for i in range(len(loc.denom_mult_lut)):
						m.d.sync += loc.denom_mult_lut[i].eq(bus.denom * i)
					#--------

					#--------
					if self.DBG():
						m.d.sync \
						+= [
							loc.dbg.dbg_quot.eq(bus.numer // bus.denom),
							loc.dbg.dbg_rema.eq(bus.numer % bus.denom),
						]
					#--------

			# If we're performing a divide
			with m.Else(): # If(bus.busy):
				#--------
				m.d.sync \
				+= [
					loc.temp_quot.word_select(loc.chunk_start, CHUNK_WIDTH)
						.eq(loc.quot_digit),

					loc.temp_rema.eq(loc.shift_in_rema
						- loc.denom_mult_lut[loc.quot_digit]),

					loc.chunk_start.eq(loc.chunk_start - 0x1),
				]

				## We do these things every cycle so as to not introduce
				## extra LUT delays from the reset logic.
				#m.d.sync \
				#+= [
				#	loc.temp_quot.word_select(loc.chunk_start, CHUNK_WIDTH)
				#		.eq(loc.quot_digit),
				#	loc.temp_rema.eq(loc.shift_in_rema
				#		- loc.denom_mult_lut[loc.quot_digit]),
				#]

				# We are on the last cycle if `chunk_start` is 0. 
				with m.If(loc.chunk_start == 0x0):
					m.d.sync \
					+= [
						bus.valid.eq(0b1),
						bus.busy.eq(0b0),
					]
				#--------
			#--------
		#--------

		#--------
		if self.FORMAL():
			#--------
			past_valid = loc.formal.past_valid

			formal_numer = loc.formal.formal_numer
			formal_denom = loc.formal.formal_denom

			oracle_quot = loc.formal.oracle_quot
			oracle_rema = loc.formal.oracle_rema

			denom_mult_lut_lst = loc.formal.denom_mult_lut_lst
			#--------

			#--------
			m.d.comb \
			+= [
				#--------
				Assume(bus.denom != 0x0),
				#--------
			]

			m.d.comb += [denom_mult_lut_lst[i].eq(loc.denom_mult_lut[i])
				for i in range(len(denom_mult_lut_lst))]

			m.d.sync \
			+= [
				past_valid.eq(0b1)
			]
			#--------

			#--------
			with m.If(~loc.rst):
				with m.If(~bus.busy):
					#--------
					with m.If(bus.start):
						m.d.sync \
						+= [
							#--------
							formal_numer.eq(bus.numer),
							formal_denom.eq(bus.denom),

							oracle_quot.eq(bus.numer // bus.denom),
							oracle_rema.eq(bus.numer % bus.denom)
							#--------
						] 
					with m.Else(): # If(~bus.start):
						pass
					#--------

					#--------
					with m.If(past_valid):
						#--------
						with m.If(Past(bus.busy)):
							m.d.comb \
							+= [
								#--------
								Assert(~Stable(bus.valid)),
								Assert(bus.valid),

								Assert(bus.quot == (formal_numer
									// formal_denom)),
								Assert(bus.rema == (formal_numer
									% formal_denom)),
								#--------

							]
						with m.Else(): # If(~Past(bus.busy)):
							m.d.comb \
							+= [
								#--------
								#Assert(Stable(bus.start)),
								#Assert(~bus.start),

								Assert(Stable(bus.valid)),
								#--------

								#--------
								Assert(Stable(loc.temp_numer)),
								Assert(Stable(loc.quot_digit)),

								Assert(Stable(loc.temp_quot)),
								Assert(Stable(loc.temp_rema)),
								#--------
							]
						#--------

						#--------
						#with m.If(~bus.start):
						m.d.comb \
						+= [
							#--------
							Assert(Stable(formal_numer)),
							Assert(Stable(formal_denom)),

							Assert(Stable(oracle_quot)),
							Assert(Stable(oracle_rema)),
							#--------
						] \
						+ [Assert(Stable(denom_mult_lut_lst[i]))
							for i in range(len(denom_mult_lut_lst))]
						#--------
					#--------
				with m.Else(): # If(bus.busy):
					#--------
					m.d.comb \
					+= [
						#--------
						Assert(~bus.valid),
						#--------

						#--------
						Assert(loc.quot_digit == oracle_quot
							.word_select(loc.chunk_start, CHUNK_WIDTH)),
						#--------
					]
					#--------

					#--------
					with m.If(past_valid):
						#--------
						with m.If(~Past(bus.busy)):
							#--------
							m.d.comb \
							+= [
								#--------
								Assert(formal_numer == Past(bus.numer)),
								Assert(formal_denom == Past(bus.denom)),

								Assert(oracle_quot == (Past(bus.numer)
									// Past(bus.denom))),
								Assert(oracle_rema == (Past(bus.numer)
									% Past(bus.denom))),
								#--------
							] \
							+ [Assert(denom_mult_lut_lst[i]
								== (Past(bus.denom) * i))
								for i in range(len(denom_mult_lut_lst))]
								
							#--------
						with m.Else(): # If(Past(bus.busy)):
							#--------
							m.d.comb \
							+= [
								#--------
								Assert(Stable(formal_numer)),
								Assert(Stable(formal_denom)),

								Assert(Stable(oracle_quot)),
								Assert(Stable(oracle_rema)),
								#--------
							] \
							+ [Assert(Stable(denom_mult_lut_lst[i]))
								for i in range(len(denom_mult_lut_lst))]
							#--------
						#--------

					#--------
			#--------
		#--------


		#--------
		return m
		#--------
	#--------
#--------
