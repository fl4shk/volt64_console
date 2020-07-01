#!/usr/bin/env python

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from vga_ext_types import *
#from fifo_mods import *
#from bram_mod import *


VGA_TIMING_INFO_DICT \
= {
	# 640 x 480 @ 60 Hz, taken from http://www.tinyvga.com
	"640x480@60":
		VgaTimingInfo \
		(
			PIXEL_CLK=25,
			HTIMING \
				=VgaTiming
				(
					visib=640,
					front=16,
					sync=96,
					back=48
				),
			VTIMING \
				=VgaTiming
				(
					visib=480,
					front=10,
					sync=2,
					back=33
				),
		)
}

class VgaDriverBusLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			# Global VGA driving enable (white screen when off)
			("en", unsigned(1)),

			# VGA physical pins
			("col", VgaColorsLayout()),
			("hsync", unsigned(1)),
			("vsync", unsigned(1)),

			# Pixel buffer
			("buf", VgaDriverBufLayout()),

			#("dbg_fifo_empty", unsigned(1)),
			#("dbg_fifo_full", unsigned(1)),
			("pixel_en", unsigned(1)),
			("visib", unsigned(1)),
			("past_visib", unsigned(1)),
			("draw_pos", Vec2Layout(unsigned(16))),
			("past_draw_pos", Vec2Layout(unsigned(16))),
			("size", Vec2Layout(unsigned(16))),
			#("start_draw", unsigned(1)),
		])

class VgaDriverBus(Record):
	def __init__(self):
		super().__init__(VgaDriverBusLayout())

class VgaDriver(Elaboratable):
	def __init__(self, CLK_RATE, TIMING_INFO, NUM_BUF_SCANLINES):
		self.__bus = VgaDriverBus()

		self.__CLK_RATE = CLK_RATE
		self.__TIMING_INFO = TIMING_INFO
		self.__NUM_BUF_SCANLINES = NUM_BUF_SCANLINES

	def bus(self):
		return self.__bus
	def CLK_RATE(self):
		return self.__CLK_RATE
	def TIMING_INFO(self):
		return self.__TIMING_INFO
	def CPP(self):
		return self.CLK_RATE() // self.TIMING_INFO().PIXEL_CLK()
	def HTIMING(self):
		return self.TIMING_INFO().HTIMING()
	def VTIMING(self):
		return self.TIMING_INFO().VTIMING()
	def NUM_BUF_SCANLINES(self):
		return self.__NUM_BUF_SCANLINES
	def FIFO_SIZE(self):
		return (self.FB_SIZE().x * self.NUM_BUF_SCANLINES())
	def FB_SIZE(self):
		ret = Blank()
		ret.x, ret.y = self.HTIMING().visib(), self.VTIMING().visib()
		return ret
	def CLK_CNT_WIDTH(self):
		return width_from_arg(self.CPP())

	def elaborate(self, platform: str):
		#--------
		m = Module()
		#--------

		#--------
		# Local variables
		loc = Blank()
		bus = self.bus()
		#--------

		#--------
		#loc.fifo = m.submodules.fifo \
		#	= Fifo \
		#	(
		#		shape_t=rec_to_shape(VgaColors()),
		#		SIZE=self.FIFO_SIZE()
		#	)

		##loc.fifo_rst = Signal(reset=0b1)

		##with m.If(loc.fifo_rst):
		##	m.d.sync += loc.fifo_rst.eq(~loc.fifo_rst)
		##m.d.comb += loc.fifo.bus().rst.eq(loc.fifo_rst)
		#m.d.comb += loc.fifo.bus().rst.eq(ResetSignal())
		#--------

		#--------
		loc.col = VgaColors()
		#--------

		#--------
		# Implement the clock enable
		loc.CLK_CNT_WIDTH = self.CLK_CNT_WIDTH()
		loc.clk_cnt = Signal(loc.CLK_CNT_WIDTH)

		# Force this addition to be of width `CLK_CNT_WIDTH + 1` to
		# prevent wrap-around
		loc.clk_cnt_p_1 = Signal(loc.CLK_CNT_WIDTH + 1)
		m.d.comb += loc.clk_cnt_p_1.eq(loc.clk_cnt + 0b1)

		# Implement wrap-around for the clock counter
		with m.If(loc.clk_cnt_p_1 < self.CPP()):
			m.d.sync += loc.clk_cnt.eq(loc.clk_cnt_p_1)
		with m.Else():
			m.d.sync += loc.clk_cnt.eq(0x0)

		# Since this is an alias, use ALL_CAPS for its name.
		#bus.pixel_en = (loc.clk_cnt == 0x0)
		m.d.comb += bus.pixel_en.eq(loc.clk_cnt == 0x0)
		loc.PIXEL_EN_NEXT_CYCLE = (loc.clk_cnt_p_1 == self.CPP())
		#--------

		#--------
		# Implement the State/Counter stuff
		loc.Tstate = VgaTiming.State
		loc.hsc \
		= {
			"s": Signal(width_from_len(loc.Tstate)),
			"c": Signal(self.HTIMING().COUNTER_WIDTH()),
		}
		loc.vsc \
		= {
			"s": Signal(width_from_len(loc.Tstate)),
			"c": Signal(self.VTIMING().COUNTER_WIDTH()),
		}
		#--------

		#--------
		## Implement HSYNC and VSYNC logic
		with m.If(bus.pixel_en): 
			self.HTIMING().update_state_cnt(m, loc.hsc)

			with m.Switch(loc.hsc["s"]):
				with m.Case(loc.Tstate.FRONT):
					m.d.sync += bus.hsync.eq(0b1)
				with m.Case(loc.Tstate.SYNC):
					m.d.sync += bus.hsync.eq(0b0)
				with m.Case(loc.Tstate.BACK):
					m.d.sync += bus.hsync.eq(0b1)
				with m.Case(loc.Tstate.VISIB):
					m.d.sync += bus.hsync.eq(0b1),
					with m.If((loc.hsc["c"] + 0x1) >= self.FB_SIZE().x):
						self.VTIMING().update_state_cnt(m, loc.vsc)

			with m.Switch(loc.vsc["s"]):
				with m.Case(loc.Tstate.FRONT):
					m.d.sync += bus.vsync.eq(0b1)
				with m.Case(loc.Tstate.SYNC):
					m.d.sync += bus.vsync.eq(0b0)
				with m.Case(loc.Tstate.BACK):
					m.d.sync += bus.vsync.eq(0b1)
				with m.Case(loc.Tstate.VISIB):
					m.d.sync += bus.vsync.eq(0b1)
		#--------

		#--------
		# Implement drawing the picture

		with m.If(bus.pixel_en):
			# Visible area
			with m.If(loc.visib):
				with m.If(~bus.en):
					m.d.sync \
					+= [
						bus.col.r.eq(0xf),
						bus.col.g.eq(0xf),
						bus.col.b.eq(0xf),
					]
				with m.Else(): # If(bus.en):
					m.d.sync \
					+= [
						bus.col.eq(loc.col)
					]
			# Black border
			with m.Else(): # If (~loc.visib)
				m.d.sync \
				+= [
					bus.col.r.eq(0x0),
					bus.col.g.eq(0x0),
					bus.col.b.eq(0x0),
				]
		#--------

		##--------
		## Implement VgaDriver bus to Fifo bus transaction
		#m.d.comb \
		#+= [
		#	bus.buf.can_prep.eq(~loc.fifo.bus().full),
		#	loc.fifo.bus().wr_en.eq(bus.buf.prep),
		#	loc.fifo.bus().wr_data.eq(bus.buf.col),
		#]
		##--------

		#--------
		# Implement grabbing pixels from the FIFO.

		#loc.FIFO_NOT_EMPTY = ~loc.fifo.bus().empty
		#loc.START_GRAB_FROM_FIFO = loc.FIFO_NOT_EMPTY \
		#	& (loc.clk_cnt == (self.CLK_CNT_WIDTH() - 3))
		#loc.END_GRAB_FROM_FIFO = loc.FIFO_NOT_EMPTY \
		#	& (loc.clk_cnt == (self.CLK_CNT_WIDTH() - 1))

		#with m.If(loc.START_GRAB_FROM_FIFO):
		#	m.d.sync += loc.fifo.bus().rd_en.eq(0b1)
		#with m.Elif(loc.END_GRAB_FROM_FIFO):
		#	m.d.sync += loc.col.eq(loc.fifo.bus().rd_data)
		#with m.Else():
		#	m.d.sync \
		#	+= [
		#		loc.fifo.bus().rd_en.eq(0b0),
		#		loc.col.r.eq(0xf),
		#		loc.col.g.eq(0xf),
		#		loc.col.b.eq(0x0),
		#	]


		#m.d.comb \
		#+= [
		#	bus.dbg_fifo_empty.eq(loc.fifo.bus().empty),
		#	bus.dbg_fifo_full.eq(loc.fifo.bus().full),
		#]

		#with m.If(bus.buf.prep):
		#	m.d.sync \
		#	+= [
		#		loc.col.eq(bus.buf.col),
		#	]
		#with m.Else():
		#	m.d.sync \
		#	+= [
		#		loc.col.r.eq(0xf),
		#		loc.col.g.eq(0xf),
		#		loc.col.b.eq(0x0),
		#	]


		loc.fifo = Blank()
		loc.fifo.PTR_WIDTH = width_from_len(self.FIFO_SIZE())

		loc.fifo.arr = Array([VgaColors()
			for _ in range(self.FIFO_SIZE())])

		loc.fifo.head = Signal(loc.fifo.PTR_WIDTH)
		loc.fifo.tail = Signal(loc.fifo.PTR_WIDTH)
		loc.fifo.next_head = Signal(loc.fifo.PTR_WIDTH)
		loc.fifo.next_tail = Signal(loc.fifo.PTR_WIDTH)
		loc.fifo.incr_next_head = Signal(loc.fifo.PTR_WIDTH)

		loc.fifo.empty = Signal()
		loc.fifo.full = Signal()
		loc.fifo.next_empty = Signal()
		loc.fifo.next_full = Signal()

		m.d.comb \
		+= [
			bus.buf.can_prep.eq(~loc.fifo.full),
		]
		m.d.sync \
		+= [
			loc.fifo.head.eq(loc.fifo.next_head),
			loc.fifo.tail.eq(loc.fifo.next_tail),
			loc.fifo.empty.eq(loc.fifo.next_empty),
			loc.fifo.full.eq(loc.fifo.next_full)
		]

		with m.If(~loc.fifo.empty):
			m.d.comb += loc.col.eq(loc.fifo.arr[loc.fifo.tail])
		with m.Else(): # If(loc.fifo.empty)
			m.d.comb \
			+= [
				loc.col.r.eq(0xf),
				loc.col.g.eq(0xf),
				loc.col.f.eq(0x0),
			]

		# Compute `loc.fifo.next_head` and write into the FIFO if it's not
		# full
		with m.If((~loc.fifo.full) & bus.buf.prep):
			m.d.sync += loc.fifo.arr[loc.fifo.head].eq(bus.buf.col)
			with m.If((loc.fifo.head + 1) >= self.FIFO_SIZE()):
				m.d.comb += loc.fifo.next_head.eq(0)
			with m.Else():
				m.d.comb += loc.fifo.next_head.eq(loc.fifo.head + 1)
		with m.Else():
			m.d.comb += loc.fifo.next_head.eq(loc.fifo.head)

		# Compute `loc.fifo.next_tail`
		with m.If((~loc.fifo.empty) & loc.visib & bus.pixel_en):
			with m.If((loc.fifo.tail + 1) >= self.FIFO_SIZE()):
				m.d.comb += loc.fifo.next_tail.eq(0)
			with m.Else():
				m.d.comb += loc.fifo.next_tail.eq(loc.fifo.tail + 1)
		with m.Else():
			m.d.comb += loc.fifo.next_tail.eq(loc.fifo.tail)

		# Compute `loc.fifo.next_empty` and `loc.fifo.next_full`
		with m.If((loc.fifo.next_head + 1) >= self.FIFO_SIZE()):
			m.d.comb += loc.fifo.incr_next_head.eq(0)
		with m.Else():
			m.d.comb + loc.fifo.incr_next_head.eq(loc.fifo.next_head + 1)

		with m.If(loc.fifo.incr_next_head == loc.fifo.next_tail):
			m.d.comb \
			+= [
				loc.fifo.next_empty.eq(0b0),
				loc.fifo.next_full.eq(0b1),
			]
		with m.Elif(loc.fifo.next_head == loc.fifo.next_tail):
			m.d.comb \
			+= [
				loc.fifo.next_empty.eq(0b1),
				loc.fifo.next_full.eq(0b0),
			]
		with m.Else():
			m.d.comb \
			+= [
				loc.fifo.next_empty.eq(0b0),
				loc.fifo.next_full.eq(0b0),
			]
		#--------

		#--------
		m.d.comb \
			+= [
				bus.visib.eq((loc.hsc["s"] == loc.Tstate.VISIB)
					& (loc.vsc["s"] == loc.Tstate.VISIB)),
				bus.draw_pos.x.eq(loc.hsc["c"]),
				bus.draw_pos.y.eq(loc.vsc["c"]),
				bus.size.x.eq(self.FB_SIZE().x),
				bus.size.y.eq(self.FB_SIZE().y),
			]
		m.d.sync \
			+= [
				bus.past_visib.eq(bus.visib),
				bus.past_draw_pos.eq(bus.draw_pos)
			]
		#--------

		#--------
		return m
		#--------
