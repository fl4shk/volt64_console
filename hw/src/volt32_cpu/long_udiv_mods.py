#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.back.pysim import Simulator, Delay, Tick

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
	def ports(self):
		return [ClockSignal(), ResetSignal(), 
			self.start, self.numer, self.denom,
			self.valid, self.busy, self.quot, self.rema]
	#--------
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
	#def verify_process(self):
	#	bus = self.bus()
	#	for numer in range(bus.MAIN_MAX_VAL()):
	#		for denom in range(1, bus.DENOM_MAX_VAL()):
	#			#print("rst:  {}".format((yield ResetSignal())))
	#			#yield Tick("sync")

	#			yield bus.start.eq(0b1)
	#			yield bus.numer.eq(numer)
	#			yield bus.denom.eq(denom)
	#			yield Tick("sync")


	#			yield bus.start.eq(0b0)
	#			yield bus.numer.eq(numer + 1)
	#			yield bus.denom.eq(denom + 1)
	#			yield Tick("sync")

	#			# Parentheses are there to make `yield whatever` an
	#			# expression.
	#			#print("begin:  {} {}".format((yield bus.busy),
	#			#	(yield bus.start)))
	#			#print("begin")
	#			while (yield bus.busy):
	#				#print("{} {}".format(hex((yield bus.quot)),
	#				#	hex((yield bus.rema))))
	#				yield Tick("sync")

	#			bus_quot = (yield bus.quot)
	#			bus_rema = (yield bus.rema)
	#			oracle_quot = (numer // denom)
	#			oracle_rema = (numer % denom)

	#			#print("{} op {}; {} {}; {} {}; {} {}\n".format
	#			#	(hex(numer), hex(denom),
	#			#	hex(bus_quot), hex(bus_rema),
	#			#	hex(oracle_quot), hex(oracle_rema),
	#			#	(bus_quot == oracle_quot), (bus_rema == oracle_rema)))
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
			for i in range(self.NUM_DIGITS_PER_CHUNK())])

		# Remainder with the current chunk of `temp_numer` shifted in
		loc.shift_in_rema = Signal(self.MAIN_WIDTH())

		# The start of the range of bits of the current chunk of
		# `temp_numer`
		loc.chunk_start = Signal(self.NUM_DIGITS_PER_CHUNK())

		# The vector of greater than comparison values
		loc.gt_vec = Signal(self.NUM_DIGITS_PER_CHUNK(), attrs={"keep": 1})

		#loc.temp_gt_vec = Signal(self.NUM_DIGITS_PER_CHUNK())

		#loc.temp_denom_mult_lut_0 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_1 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_2 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_3 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_4 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_5 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_6 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#loc.temp_denom_mult_lut_7 \
		#	= Signal(self.DENOM_MULT_LUT_ENTRY_WIDTH())
		#--------

		##--------
		#loc.dbg = Blank()
		##--------

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
			loc.formal.denom = Signal(self.DENOM_WIDTH())

			loc.formal.oracle_quot = Signal(self.TEMP_T_WIDTH())
			loc.formal.oracle_rema = Signal(self.TEMP_T_WIDTH())
			#--------

			##--------
			#loc.formal.temp_denom_mult_lut_lst = []
			##--------
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

		##--------
		#m.d.sync += self.bus().busy.eq(0b1)
		#return m
		##--------

		#--------
		# Local variables
		bus = self.bus()

		loc = self._build_loc()

		TEMP_T_WIDTH = self.TEMP_T_WIDTH()
		CHUNK_WIDTH = self.CHUNK_WIDTH()

		## dbg
		#bus.loc = loc
		#--------

		#--------
		# Shift in the current chunk of `loc.temp_numer`
		m.d.comb \
		+= [
			loc.shift_in_rema.eq(Cat(loc.temp_numer.word_select
				(loc.chunk_start, CHUNK_WIDTH),
				loc.temp_rema[:TEMP_T_WIDTH - CHUNK_WIDTH])),
		]

		#m.d.sync \
		#+= [
		#	loc.temp_gt_vec.eq(loc.gt_vec),
		#]

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
			with m.Default():
				m.d.comb += loc.quot_digit.eq(0)
			for i in range(1, len(loc.gt_vec)):
				with m.Case(("1" * (len(loc.gt_vec) - (i + 1))) + "0"
					+ ("-" * i)):
					m.d.comb \
					+= [
						loc.quot_digit.eq(i)
					]
			##with m.Case("------10"):
			#with m.Default():
			#	m.d.comb += loc.quot_digit.eq(0)
			#with m.Case("11111100"):
			#	m.d.comb += loc.quot_digit.eq(1)
			#with m.Case("11111000"):
			#	m.d.comb += loc.quot_digit.eq(2)
			#with m.Case("11110000"):
			#	m.d.comb += loc.quot_digit.eq(3)
			#with m.Case("11100000"):
			#	m.d.comb += loc.quot_digit.eq(4)
			#with m.Case("11000000"):
			#	m.d.comb += loc.quot_digit.eq(5)
			#with m.Case("10000000"):
			#	m.d.comb += loc.quot_digit.eq(6)
			#with m.Case("00000000"):
			#	m.d.comb += loc.quot_digit.eq(7)

		m.d.comb \
		+= [
			bus.quot.eq(loc.temp_quot[:len(bus.quot)]),
			bus.rema.eq(loc.temp_rema[:len(bus.rema)]),
		]
		#--------

		#--------
		if self.FORMAL():
			m.d.comb \
			+= [
				#--------
				Assume(bus.denom != 0x0),
				#--------
			]

			m.d.sync \
			+= [
				loc.formal.past_valid.eq(0b1)
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
					with m.Elif(Past(bus.busy) & (~bus.busy)):
						m.d.sync \
						+= [
							#--------
							Assert(bus.quot 
								== loc.formal.oracle_quot[:len(bus.quot)]),
							Assert(bus.rema 
								== loc.formal.oracle_rema[:len(bus.rema)]),
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
							#--------
							loc.formal.numer.eq(bus.numer),
							loc.formal.denom.eq(bus.denom),

							loc.formal.oracle_quot.eq(bus.numer 
								// bus.denom),
							loc.formal.oracle_rema.eq(bus.numer
								% bus.denom),
							#--------
						]
				#--------

				#--------
				m.d.sync \
				+= [
					bus.valid.eq(0b0),
					bus.busy.eq(0b1),

					loc.temp_numer.eq(bus.numer),

					loc.temp_quot.eq(0x0),
					loc.temp_rema.eq(0x0),

					loc.chunk_start.eq(TEMP_T_WIDTH - CHUNK_WIDTH),
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

								Assert(loc.chunk_start == (TEMP_T_WIDTH
									- CHUNK_WIDTH)),
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
								Assert(loc.chunk_start
									== (Past(loc.chunk_start)
										- CHUNK_WIDTH)),
							]
							for i in range(len(loc.denom_mult_lut)):
								m.d.sync \
								+= [
									Assert(Stable(loc.denom_mult_lut[i])),
								]

						# If we're just busy
						m.d.sync \
						+= [
							Assert(~bus.valid),

							Assert(loc.chunk_start <= (TEMP_T_WIDTH
								- CHUNK_WIDTH)),

							Assert(loc.quot_digit == loc.formal.oracle_quot
								.word_select(loc.chunk_start,
									CHUNK_WIDTH)),

							## These lines make no sense?  They make the
							## base case pass!
							#Assume(loc.temp_denom_mult_lut_0
							#	== loc.denom_mult_lut[0]),
							#Assume(loc.temp_denom_mult_lut_1
							#	== loc.denom_mult_lut[1]),
							#Assume(loc.temp_denom_mult_lut_2
							#	== loc.denom_mult_lut[2]),
							#Assume(loc.temp_denom_mult_lut_3
							#	== loc.denom_mult_lut[3]),
							#Assume(loc.temp_denom_mult_lut_4
							#	== loc.denom_mult_lut[4]),
							#Assume(loc.temp_denom_mult_lut_5
							#	== loc.denom_mult_lut[5]),
							#Assume(loc.temp_denom_mult_lut_6
							#	== loc.denom_mult_lut[6]),
							#Assume(loc.temp_denom_mult_lut_7
							#	== loc.denom_mult_lut[7]),
						]
				#--------

				#--------
				m.d.sync \
				+= [
					loc.temp_quot.word_select(loc.chunk_start, CHUNK_WIDTH)
						.eq(loc.quot_digit),

					loc.temp_rema.eq(loc.shift_in_rema
						- loc.denom_mult_lut[loc.quot_digit]),

					loc.chunk_start.eq(loc.chunk_start - CHUNK_WIDTH),
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
		return m
		#--------
	#--------
#--------

