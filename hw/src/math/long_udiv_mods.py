#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from enum import Enum, auto

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
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, FORMAL=False):
		self.__bus = LongUdivBus \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH
			)
		self.__CHUNK_WIDTH, self.__FORMAL = CHUNK_WIDTH, FORMAL
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
	#--------

	#--------
	def TEMP_T_WIDTH(self):
		#return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
		#	// self.CHUNK_WIDTH) + 2))
		return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
			// self.CHUNK_WIDTH) + 1))

	#def NUM_CHUNKS(self):
	#	return (self.TEMP_T_WIDTH() // self.CHUNK_WIDTH())

	def NUM_DIGITS_PER_CHUNK(self):
		return (2 ** self.CHUNK_WIDTH())
	def DENOM_MULT_LUT_ENTRY_WIDTH(self):
		return (self.DENOM_WIDTH() + self.CHUNK_WIDTH())
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
		loc.quot_digit = Signal(self.CHUNK_WIDTH)

		# Quotient as a `temp_t`
		loc.temp_quot = Signal(self.TEMP_T_WIDTH())

		# Remainder as a `temp_t`
		loc.temp_rema = Signal(self.TEMP_T_WIDTH())

		# The array of (denominator * possible_digit) values
		loc.denom_mult_lut = Array \
			([Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
			for i in range(self.NUM_DIGITS_PER_CHUNK())])

		# Remainder with the current chunk of `temp_numer` shifted in
		loc.shift_in_rema = Signal(self.MAIN_WIDTH())

		# The range of bits of the current chunk of `temp_numer`
		loc.chunk_range = Blank()
		loc.chunk_range.high = Signal(self.CHUNK_WIDTH())
		loc.chunk_range.low = Signal(self.CHUNK_WIDTH())

		# The vector of greater than comparison values
		loc.gt_vec = Signal(self.NUM_DIGITS_PER_CHUNK())
		#--------

		#--------
		if self.FORMAL():
			#--------
			loc.formal = Blank()
			#--------

			#--------
			loc.formal.past_valid = Signal(reset=0b0)
			#--------

			#--------
			loc.formal.numer = Signal(self.TEMP_T_WIDTH())
			#loc.formal.denom = Signal(self.DENOM_WIDTH())

			loc.formal.oracle = Blank()
			loc.formal.oracle.quot = Signal(self.TEMP_T_WIDTH())
			loc.formal.oracle.rema = Signal(self.TEMP_T_WIDTH())
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
		#--------

		#--------
		# Shift in the current chunk of `loc.temp_numer`
		m.d.comb \
		+= [
			loc.shift_in_rema.eq(Cat(loc.temp_numer
				[loc.chunk_range.low : loc.chunk_range.high],
				bus.rema[:self.TEMP_T_WIDTH() - self.CHUNK_WIDTH()])),
		]

		# Compare every element of the computed `denom * digit` array to
		# `shift_in_rema`, computing `gt_vec`.
		# This creates around a single LUT delay for the comparisons given
		# the existence of hard carry chains in FPGAs.
		for i in range(self.NUM_DIGITS_PER_CHUNK()):
			m.d.comb += loc.gt_vec[i].eq(loc.denom_mult_lut[i] 
				> loc.shift_in_rema)

		# Create a priority encoder to find both the current
		# quotient digit, which is then also used to find the next
		# value of the remainder.
		with m.Switch(loc.gt_vec):
			for i in range(len(loc.gt_vec)):
				with m.Case("1" + ("-" * i)):
					m.d.comb \
					+= [
						loc.quot_digit.eq(i),
						#bus.quot.eq(loc.temp_quot[:len(bus.quot)]
					]
					#m.d.sync \
					#+= [
					#	loc.temp_quot[loc.chunk_range.low
					#		: loc.chunk_range.high].eq(i),
					#]
					#m.d.comb \
					#+= [
					#	loc.temp_rema.eq(loc.shift_in_rema
					#		- loc.denom_mult_lut[i]),
					#]

		m.d.comb \
		+= [
			bus.quot.eq(loc.temp_quot[:len(bus.quot)]),
			bus.rema.eq(loc.temp_rema[:len(bus.rema)]),
		]
		#--------

		#--------
		if self.FORMAL():
			m.d.sync += loc.formal.past_valid.eq(0b1)
		#--------

		#--------
		# We do these things every cycle so as to not introduce extra LUT
		# delays from the reset logic.
		m.d.sync \
		+= [
			loc.temp_quot[loc.chunk_range.low : loc.chunk_range.high]
				.eq(loc.quot_digit)
			loc.temp_rema.eq(loc.shift_in_rema
				- loc.denom_mult_lut[loc.quot_digit]),
		]
		#--------

		#--------
		#with m.If(loc.rst):
		#	#--------
		#	m.d.sync \
		#	+= [
		#		bus.valid.eq(0b0),
		#		bus.busy.eq(0b0),
		#	]
		#	#--------
		with m.If(~loc.rst):
			#--------
			if self.FORMAL():
				with m.If(loc.formal.past_valid):
					with m.If(Past(loc.rst)):
						m.d.sync \
						+= [
							#--------
							Assert(~bus.valid),
							Assert(~bus.busy),
							Assert(bus.quot == 0x0),
							Assert(bus.rema == 0x0),

							#Assert(loc.temp_numer == Past(bus.numer)),
							Assert(loc.temp_quot == 0x0),
							Assert(loc.temp_rema == 0x0),
							#--------
						]
			#--------

			#--------
			# If we're starting a divide
			with m.If((~bus.busy) & bus.start):
				#--------
				if self.FORMAL():
					with m.If(loc.formal.past_valid):
						m.d.sync \
						+= [
							#loc.formal.numer.eq(bus.numer),
							#loc.formal.denom.eq(bus.denom),

							loc.formal.oracle.quot.eq(bus.numer 
								/ bus.denom),
							loc.formal.oracle.rema.eq(bus.numer
								% bus.denom),
						]
				#--------

				#--------
				m.d.sync \
				+= [
					bus.valid.eq(0b0),
					bus.busy.eq(0b1),

					loc.temp_numer.eq(bus.numer),

					loc.chunk_range.high.eq(self.TEMP_T_WIDTH()),
					loc.chunk_range.low.eq((self.TEMP_T_WIDTH() - 1) 
						- (self.CHUNK_WIDTH() - 1)),
				]

				# Compute the array of `(denom * digit)`
				for i in range(len(loc.denom_mult_lut)):
					m.d.sync += loc.denom_mult_lut[i].eq(bus.denom * i)
				#--------

			# If we're performing a divide
			with m.Elif(bus.busy):
				#--------
				if self.FORMAL():
					with m.If(loc.formal.past_valid):
						with m.If(~Past(bus.busy)):
							m.d.sync \
							+= [
								Assert(Past(bus.start)),

								Assert(loc.temp_numer == Past(bus.numer)),

								Assert(loc.chunk_range.high
									== self.TEMP_T_WIDTH()),
							]

							for i in range(len(loc.denom_mult_lut)):
								m.d.sync \
								+= [
									Assert(loc.denom_mult_lut[i]
										== (Past(bus.denom) * i)),
								]
						with m.Else(): # If(Past(bus.busy)):
							m.d.sync \
							+= [
								Assert(Stable(loc.temp_numer)),
							]
							for i in range(len(loc.denom_mult_lut)):
								m.d.sync \
								+= [
									Assert(Stable(loc.denom_mult_lut[i])),
								]

						m.d.sync \
						+= [
							Assert(~bus.valid),
							Assert(loc.chunk_range.low
								== ((loc.chunk_range.high - 1)
								- (self.CHUNK_WIDTH() - 1))),
						]
				#--------

				#--------
				# Decrement the `chunk_range` counters
				m.d.sync \
				+= [
					loc.chunk_range.high.eq(loc.chunk_range.high
						- self.CHUNK_WIDTH()),
					loc.chunk_range.low.eq(loc.chunk_range.low
						- self.CHUNK_WIDTH()),
				]

				# We are on the last cycle if `chunk_range.low` is 0. 
				with m.If(loc.chunk_range.low == 0x0):
					m.d.sync \
					+= [
						bus.valid.eq(0b1),
						bus.busy.eq(0b0),
					]
				#--------
			#--------
		#--------


		#--------
		return m
		#--------
	#--------
#--------
