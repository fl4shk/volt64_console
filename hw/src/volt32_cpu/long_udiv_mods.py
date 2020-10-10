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
		loc = Blank()

		loc.rst = ResetSignal()

		# numerator as a `temp_t`
		loc.temp_numer = Signal(self.TEMP_T_WIDTH())

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

		return loc
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
		#--------

		#--------
		with m.If(loc.rst):
			m.d.sync \
			+= [
				bus.valid.eq(0b0),
				bus.busy.eq(0b0),
				bus.quot.eq(0x0),
				bus.rema.eq(0x0),
			]
		with m.Else(): # If(~loc.rst):
			# If we're starting a divide
			with m.If((~bus.busy) & bus.start):
				m.d.sync \
				+= [
					bus.valid.eq(0b0),
					bus.busy.eq(0b1),
					bus.quot.eq(0x0),
					bus.rema.eq(0x0),
					loc.temp_numer.eq(bus.numer),
					loc.chunk_range.high.eq(self.TEMP_T_WIDTH()),
					loc.chunk_range.low.eq((self.TEMP_T_WIDTH() - 1) 
						- (self.CHUNK_WIDTH() - 1)),
				]
				for i in range(len(loc.denom_mult_lut)):
					m.d.sync += loc.denom_mult_lut[i].eq(bus.denom * i)

			# If we're performing a divide
			with m.Elif(bus.busy):
				# Create a priority encoder to find both the current
				# quotient digit, which is then also used to find the next
				# value of the remainder.
				with m.Switch(loc.gt_vec):
					for i in range(len(loc.gt_vec)):
						with m.Case("1" + ("-" * i)):
							m.d.sync \
							+= [
								bus.quot[loc.chunk_range.low
									: loc.chunk_range.high].eq(i),
								bus.rema.eq(loc.shift_in_rema
									- loc.denom_mult_lut[i]),
							]
				# Decrement the `chunk_range` counter
				m.d.sync \
				+= [
					loc.chunk_range.high.eq(loc.chunk_range.high
						- self.CHUNK_WIDTH()),
					loc.chunk_range.low.eq(loc.chunk_range.low
						- self.CHUNK_WIDTH()),
				]
		#--------

		#--------
		return m
		#--------
	#--------
#--------
