#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

#--------
class FifoBusLayout(Layout):
	def __init__(self, shape_t, SIZE):
		self.__shape_t, self.__SIZE = shape_t, SIZE

		super().__init__ \
		([
			#--------
			("clk", 1),
			("rst", 1),
			#--------

			#--------
			("wr_en", 1),
			("wr_data", self.shape_t()),

			("rd_en", 1),
			("rd_data", self.shape_t()),
			#--------

			#--------
			("empty", 1),
			("full", 1),
			#--------
		])

	def shape_t(self):
		return self.__shape_t
	def SIZE(self):
		return self.__SIZE

class FifoBus(Record):
	def __init__(self, shape_t, SIZE):
		super().__init__(FifoBusLayout(shape_t, SIZE))

	def shape_t(self):
		return self.layout.shape_t()
	def SIZE(self):
		return self.layout.SIZE()

	def ports(self):
		return [self.clk, self.rst, self.wr_en, self.wr_data, self.rd_en,
			self.rd_data, self.empty, self.full]
#--------

#--------
class Fifo(Elaboratable):
	def __init__(self, shape_t, SIZE, FORMAL=False):
		self.__bus = FifoBus(shape_t, SIZE)
		self.__FORMAL = FORMAL

	def bus(self):
		return self.__bus
	def FORMAL(self):
		return self.__FORMAL

	def elaborate(self, platform: str):
		#--------
		m = Module()

		#add_clk_domain(m, self.bus().clk)
		#add_clk_from_domain(m, self.bus.clk())
		#--------

		#--------
		# Local variables
		bus = self.bus()

		loc = Blank()

		loc.arr = Array([Signal(bus.shape_t()) for _ in range(bus.SIZE())])

		loc.PTR_WIDTH = width_from_arg(bus.SIZE())

		loc.rd = Signal(loc.PTR_WIDTH)
		loc.wr = Signal(loc.PTR_WIDTH)

		loc.RD_PLUS_1 = loc.rd + 0x1
		loc.WR_PLUS_1 = loc.wr + 0x1

		loc.incr_rd = Signal(loc.PTR_WIDTH)
		loc.incr_wr = Signal(loc.PTR_WIDTH)

		loc.next_empty = Signal()
		loc.next_full = Signal()

		loc.next_rd = Signal(loc.PTR_WIDTH)
		loc.next_wr = Signal(loc.PTR_WIDTH)

		#loc.curr_en_cat = Signal(2)

		if self.FORMAL():
			loc.formal = Blank()

			loc.formal.last_rd_val = Signal(bus.shape_t())
			loc.formal.test_wr = Signal(loc.PTR_WIDTH)
			#loc.formal.empty = Signal()
			#loc.formal.full = Signal()
			loc.formal.wd_cnt = Signal(bus.shape_t(), reset=0xa0)
		#--------

		#--------
		if self.FORMAL():
			m.d.dom \
			+= [
				loc.formal.last_rd_val.eq(loc.arr[loc.rd]),
				loc.formal.wd_cnt.eq(loc.formal.wd_cnt - 0x10)
			]
			m.d.comb \
			+= [
				loc.formal.test_wr.eq((loc.wr + 0x1) % bus.SIZE()),
			]
		#--------

		#--------
		# Combinational logic

		m.d.comb \
		+= [
			loc.incr_rd.eq(Mux(loc.RD_PLUS_1 < bus.SIZE(),
				(loc.rd + 0x1), 0x0)),
			loc.incr_wr.eq(Mux(loc.WR_PLUS_1 < bus.SIZE(),
				(loc.wr + 0x1), 0x0)),

			loc.next_empty.eq(loc.next_wr == loc.next_rd),
			#loc.next_full.eq((loc.next_wr + 0x1) == loc.next_rd),

			#loc.curr_en_cat.eq(Cat(bus.rd_en, bus.wr_en)),
		]

		with m.If(bus.rd_en & (~bus.empty)):
			m.d.comb += loc.next_rd.eq(loc.incr_rd)
		with m.Else():
			m.d.comb += loc.next_rd.eq(loc.rd)

		with m.If(bus.wr_en & (~bus.full)):
			m.d.comb \
			+= [
				loc.next_wr.eq(loc.incr_wr),
				loc.next_full.eq((loc.incr_wr + 0x1) == loc.next_rd),
			]
		with m.Else():
			m.d.comb \
			+= [
				loc.next_wr.eq(loc.wr),
				loc.next_full.eq(loc.incr_wr == loc.next_rd), 
			]
		#--------

		#--------
		# Clocked behavioral code
		with m.If(bus.rst):
			#for elem in loc.arr:
			#	m.d.dom += elem.eq(bus.shape_t()())

			m.d.dom \
			+= [
				loc.rd.eq(0x0),
				loc.wr.eq(0x0),

				#bus.rd_data.eq(bus.shape_t()()),

				bus.empty.eq(0b1),
				bus.full.eq(0b0),
			]
		with m.Else(): # If(~bus.rst):
			#--------
			m.d.dom \
			+= [
				bus.empty.eq(loc.next_empty),
				bus.full.eq(loc.next_full),
				loc.rd.eq(loc.next_rd),
				loc.wr.eq(loc.next_wr),
			]

			with m.If(bus.rd_en & (~bus.empty)):
				m.d.dom += bus.rd_data.eq(loc.arr[loc.rd])
			with m.If(bus.wr_en & (~bus.full)):
				m.d.dom += loc.arr[loc.wr].eq(bus.wr_data)
			#--------

			#--------
			if self.FORMAL():
				with m.If(Fell(bus.rst)):
					m.d.dom \
					+= [
						Assert(loc.rd == 0x0),
						Assert(loc.wr == 0x0),

						Assert(bus.empty == 0b1),
						Assert(bus.full == 0b0),
					]
				with m.Else(): # If(~Fell(bus.rst)):
					m.d.dom \
					+= [
						Assert(bus.empty == Past(loc.next_empty)),
						Assert(bus.full == Past(loc.next_full)),
						Assert(loc.rd == Past(loc.next_rd)),
						Assert(loc.wr == Past(loc.next_wr)),
					]
					with m.If(Past(bus.rd_en)):
						with m.If(Past(bus.empty)):
							m.d.dom \
							+= [
								#Assert(Stable(bus.empty)),
								Assert(Stable(loc.rd)),
							]
						with m.Else(): # If(~Past(bus.empty)):
							#with m.If(~Past(bus.wr_en)):
							m.d.dom \
							+= [
								Assert(bus.rd_data
									== loc.arr[Past(loc.rd)])
							]
					with m.If(Past(bus.wr_en)):
						with m.If(Past(bus.full)):
							m.d.dom \
							+= [
								Assert(Stable(loc.wr)),
							]
						#with m.Else(): # If(~Past(bus.full)):
						#	m.d.dom \
						#	+= [
						#		Assert(Past(bus.wr_data))
						#	]
					with m.Switch(Cat(bus.empty, bus.full)):
						with m.Case(0b00):
							m.d.dom \
							+= [
								Assume(loc.wr != loc.rd),
								Assume(loc.formal.test_wr != loc.rd),
							]
						with m.Case(0b01):
							m.d.dom \
							+= [
								Assert(loc.wr == loc.rd)
							]
						with m.Case(0b10):
							m.d.dom \
							+= [
								Assert(loc.formal.test_wr == loc.rd),
							]
					m.d.dom \
					+= [
						Assert(~(bus.empty & bus.full)),
						#Assume(~Stable(bus.wr_data)),
						#Assume(bus.wr_data == loc.formal.wd_cnt),
					]
			#--------
		#--------

		#--------
		return m
		#--------

#--------
