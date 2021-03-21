#!/usr/bin/env python3

import math
from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto


#--------
class LongUdivPstageBus:
	#--------
	class PsData:
		#--------
		def __init__(self, bus, io_dir: str):
			#--------
			self.__DML_ENTRY_WIDTH = bus.DML_ENTRY_WIDTH()
			self.__FORMAL = bus.FORMAL()
			#--------

			#--------
			self.temp_numer = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep(),
				name=f"temp_numer_{io_dir}")

			self.temp_quot = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep(),
				name=f"temp_quot_{io_dir}")
			self.temp_rema = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep(),
				name=f"temp_rema_{io_dir}")
			#--------

			#--------
			#self.denom_mult_lut = Array([Signal
			#	(bus.DML_ENTRY_WIDTH())
			#	for _ in range(bus.RADIX())])
			self.denom_mult_lut = Signal \
				((bus.DML_ENTRY_WIDTH() * self.__DML_LEN),
				attrs=sig_keep(), name=f"denom_mult_lut_{io_dir}")
			#--------

			#--------
			self.tag = Signal(bus.TAG_WIDTH(), attrs=sig_keep(),
				name=f"tag_{io_dir}")
			#--------

			#--------
			if self.__FORMAL:
				#--------
				self.formal = Blank()
				#--------

				#--------
				self.formal.formal_numer = Signal(bus.TEMP_T_WIDTH(),
					attrs=sig_keep(), name=f"formal_numer_{io_dir}")
				self.formal.formal_denom = Signal(bus.DENOM_WIDTH(),
					attrs=sig_keep(), name=f"formal_denom_{io_dir}")

				self.formal.oracle_quot = Signal(bus.TEMP_T_WIDTH(),
					attrs=sig_keep(), name=f"oracle_quot_{io_dir}")
				self.formal.oracle_rema = Signal(bus.TEMP_T_WIDTH(),
					attrs=sig_keep(), name=f"oracle_rema_{io_dir}")
				#--------

				#--------
				self.formal.formal_denom_mult_lut = Signal \
					((bus.DML_ENTRY_WIDTH() * self.__DML_LEN),
					attrs=sig_keep(),
					name=f"formal_denom_mult_lut_{io_dir}")
				#--------
			#--------
		#--------

		#--------
		def dml_elem(self, index):
			return self.denom_mult_lut.word_select(index,
				self.__DML_ENTRY_WIDTH)
		def formal_dml_elem(self, index):
			assert self.__FORMAL
			return self.formal.formal_denom_mult_lut.word_select(index,
				self.__DML_ENTRY_WIDTH)
		#--------
	#--------

	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, TAG_WIDTH,
		PIPELINED, FORMAL):
		#--------
		self.__MAIN_WIDTH = MAIN_WIDTH
		self.__DENOM_WIDTH = DENOM_WIDTH
		self.__CHUNK_WIDTH = CHUNK_WIDTH
		self.__TAG_WIDTH = TAG_WIDTH
		self.__PIPELINED = PIPELINED
		self.__FORMAL = FORMAL
		#--------

		#--------
		# Inputs

		self.psd_in = LongUdivPstageBus.PsData(bus=self, io_dir="in")
		self.chunk_start = Signal(self.CHUNK_WIDTH(), attrs=sig_keep())
		#--------

		#--------
		# Outputs

		self.psd_out = LongUdivPstageBus.PsData(bus=self, io_dir="out")
		#--------
	#--------

	#--------
	def MAIN_WIDTH(self):
		return self.__MAIN_WIDTH
	def DENOM_WIDTH(self):
		return self.__DENOM_WIDTH
	def CHUNK_WIDTH(self):
		return self.__CHUNK_WIDTH
	def TAG_WIDTH(self):
		return self.__TAG_WIDTH
	def PIPELINED(self):
		return self.__PIPELINED
	def FORMAL(self):
		return self.__FORMAL

	def TEMP_T_WIDTH(self):
		return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
			// self.CHUNK_WIDTH()) + 1))
		#add_amount = 1 if not self.PIPELINED() else 2
		#return (self.CHUNK_WIDTH() * ((self.MAIN_WIDTH()
		#	// self.CHUNK_WIDTH()) + add_amount))

	#def NUM_CHUNKS(self):
	#	return (self.TEMP_T_WIDTH() // self.CHUNK_WIDTH())

	def RADIX(self):
		return (1 << self.CHUNK_WIDTH())

	def DML_ENTRY_WIDTH(self):
		return (self.DENOM_WIDTH() + self.CHUNK_WIDTH())
	#def DML_LEN(self):
	#	return self.RADIX()
	#--------
#--------

#--------
class LongUdivPstage(Elaboratable):
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH, TAG_WIDTH,
		PIPELINED=False, FORMAL=False):
		self.__bus \
			= LongUdivPstageBus \
			(
				MAIN_WIDTH=MAIN_WIDTH,
				DENOM_WIDTH=DENOM_WIDTH,
				CHUNK_WIDTH=CHUNK_WIDTH,
				TAG_WIDTH=TAG_WIDTH,
				PIPELINED=PIPELINED,
				FORMAL=FORMAL,
			)
	#--------

	#--------
	def bus(self):
		return self.__bus
	#--------

	#--------
	# Local signals
	def __build_loc(self):
		#--------
		bus = self.bus()

		loc = Blank()
		#--------

		#--------
		# Current quotient digit
		loc.quot_digit = Signal(bus.CHUNK_WIDTH(), attrs=sig_keep())

		# Remainder with the current chunk of `bus.ps_data_in.temp_numer`
		# shifted in
		loc.shift_in_rema = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep())

		# The vector of greater than comparison values
		loc.gt_vec = Signal(bus.RADIX(), attrs=sig_keep())

		# Next value of `temp_quot`
		loc.temp_quot = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep())

		loc.temp_rema = Signal(bus.TEMP_T_WIDTH(), attrs=sig_keep())
		#--------

		#--------
		if bus.FORMAL():
			#--------
			loc.formal = Blank()
			#--------

			#--------
			loc.formal.past_valid = Signal(reset=0b0, attrs=sig_keep())
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
		bus = self.bus()

		loc = self.__build_loc()

		psd_in = bus.psd_in
		psd_out = bus.psd_out

		TEMP_T_WIDTH = bus.TEMP_T_WIDTH()
		CHUNK_WIDTH = bus.CHUNK_WIDTH()
		#--------

		#--------
		# Shift in the current chunk of `psd_in.temp_numer`
		m.d.comb += loc.shift_in_rema.eq(Cat(psd_in.temp_numer.word_select
			(bus.chunk_start, CHUNK_WIDTH),
			psd_in.temp_rema[:TEMP_T_WIDTH - CHUNK_WIDTH])),

		# Compare every element of the computed `denom * digit` array to
		# `shift_in_rema`, computing `gt_vec`.
		# This creates around a single LUT delay for the comparisons given
		# the existence of hard carry chains in FPGAs.
		for i in range(bus.RADIX()):
			m.d.comb += loc.gt_vec[i].eq(psd_in.dml_elem(i) 
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


		#m.d.comb \
		#+= [
		#	bus.quot.eq(loc.temp_quot[:len(bus.quot)]),
		#	bus.rema.eq(loc.temp_rema[:len(bus.rema)]),
		#]

		for i in range(bus.TEMP_T_WIDTH() // bus.CHUNK_WIDTH()):
			with m.If(bus.chunk_start == i):
				m.d.comb \
				+= [
					loc.temp_quot_next.word_select(i, CHUNK_WIDTH)
						.eq(loc.quot_digit),
				]
			with m.Else(): # If(bus.chunk_start != i):
				m.d.comb \
				+= [
					loc.temp_quot_next.word_select(i, CHUNK_WIDTH)
						.eq(psd_in.temp_quot.word_select(i, CHUNK_WIDTH)),
				]

		m.d.comb += loc.temp_rema_next.eq(loc.shift_in_rema
			- psd_in.dml_elem(loc.quot_digit)),
		#--------

		#--------
		with m.If(~ResetSignal()):
			#for i in range(bus.TEMP_T_WIDTH() // bus.CHUNK_WIDTH()):
			#	with m.If(bus.chunk_start == i):
			#		m.d.sync += psd_out.temp_quot.word_select
			#			(i, CHUNK_WIDTH).eq(loc.quot_digit)
			#	with m.Else(): # If(bus.chunk_start != i):
			#		m.d.sync += psd_out.temp_quot.word_select
			#			(i, CHUNK_WIDTH).eq(psd_in.temp_quot.word_select
			#				(i, CHUNK_WIDTH))
			m.d.sync \
			+= [
				#--------
				psd_out.temp_numer.eq(psd_in.temp_numer),

				#loc.temp_quot.word_select(bus.chunk_start, CHUNK_WIDTH)
				#	.eq(loc.quot_digit),

				#psd_out.temp_rema.eq(loc.shift_in_rema
				#	- psd_in.dml_elem(loc.quot_digit)),

				psd_out.temp_quot.eq(loc.temp_quot_next),
				psd_out.temp_rema.eq(loc.temp_rema_next),
				#--------

				#--------
				psd_out.denom_mult_lut.eq(psd_in.denom_mult_lut),
				#--------

				#--------
				psd_out.tag.eq(psd_in.tag),
				#--------

				#--------
				#bus.chunk_start.eq(bus.chunk_start - 0x1),
				#--------
			]
		#--------

		#--------
		if bus.FORMAL():
			#--------
			past_valid = loc.formal.past_valid

			formal_numer_in = psd_in.formal.formal_numer
			formal_denom_in = psd_in.formal.formal_denom

			oracle_quot_in = psd_in.formal.oracle_quot
			oracle_rema_in = psd_in.formal.oracle_rema

			formal_denom_mult_lut_in = psd_in.formal.formal_denom_mult_lut
			#--------

			#--------
			m.d.comb \
			+= [
				#--------
				Assume(formal_denom != 0),
				#--------
			]

			m.d.sync \
			+= [
				#--------
				past_valid.eq(0b1),
				#--------
			]
			#--------

			#--------
			with m.If(~ResetSignal()):
				#--------
				# Send the formal verification pipeline signals to the next
				# stage of the pipeline.
				m.d.sync \
				+= [
					#--------
					psd_out.formal.formal_numer.eq(formal_numer_in),
					psd_out.formal.formal_denom.eq(formal_denom_in),

					psd_out.formal.oracle_quot.eq(oracle_quot_in),
					psd_out.formal.oracle_rema.eq(oracle_rema_in),
					#--------

					#--------
					psd_out.formal.formal_denom_mult_lut
						.eq(formal_denom_mult_lut_in),
					#--------
				]
				#--------

				#--------
				m.d.comb \
				+= [
					#--------
					Assert(loc.quot_digit == oracle_quot_in
						.word_select(bus.chunk_start, bus.CHUNK_WIDTH())),
					#--------
				]

				# If we are the last pipeline stage (or if we are
				# multi-cycle and computing the last chunk of quotient and
				# final remainder), check to see if our answer is correct  
				with m.If(bus.chunk_start == 0x0):
					m.d.comb \
					+= [
						#--------
						Assert(loc.next_temp_quot == (formal_numer_in
							// formal_denom_in)),
						Assert(loc.next_temp_rema == (formal_numer_in
							% formal_denom_in)),
						#--------
					]
				#--------

				#--------
				with m.If(past_valid):
					#--------
					m.d.comb \
					+= [
						#--------
						Assert(psd_out.formal.formal_numer
							== Past(formal_numer_in)),
						Assert(psd_out.formal.formal_denom
							== Past(formal_denom_in)),

						Assert(psd_out.formal.oracle_quot
							== Past(oracle_quot_in)),
						Assert(psd_out.formal.oracle_rema
							== Past(oracle_rema_in)),
						#--------

						#--------
						Assert(psd_out.formal.formal_denom_mult_lut
							== Past(formal_denom_mult_lut_in)),
						#--------
					]
					#--------
				#--------
			#--------
		#--------

		#--------
		return m
		#--------
	#--------
#--------

#--------
class LongUdivBus:
	#--------
	def __init__(self, MAIN_WIDTH, DENOM_WIDTH, CHUNK_WIDTH,
		PIPELINED=False, FORMAL=False):
		#--------
		self.__MAIN_WIDTH = MAIN_WIDTH
		self.__DENOM_WIDTH = DENOM_WIDTH
		self.__CHUNK_WIDTH = CHUNK_WIDTH
		self.__PIPELINED = PIPELINED
		self.__FORMAL = FORMAL
		#--------

		#--------
		# Inputs

		if not self.PIPELINED():
			self.start = Signal()

		self.numer = Signal(self.MAIN_WIDTH())
		self.denom = Signal(self.DENOM_WIDTH())

		if self.PIPELINED():
			self.tag_in = Signal(self.TAG_WIDTH())
		#--------

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

	#--------
	def MAIN_WIDTH(self):
		return self.__MAIN_WIDTH
	def MAIN_MAX_VAL(self):
		return (1 << self.MAIN_WIDTH())

	def DENOM_WIDTH(self):
		return self.__DENOM_WIDTH
	def DENOM_MAX_VAL(self):
		return (1 << self.DENOM_WIDTH())

	def CHUNK_WIDTH(self):
		return self.__CHUNK_WIDTH
	def TAG_WIDTH(self):
		return (math.log2(self.MAIN_WIDTH() // self.CHUNK_WIDTH()) + 2)

	def PIPELINED(self):
		return self.__PIPELINED

	def FORMAL(self):
		return self.__FORMAL
	#--------
#--------