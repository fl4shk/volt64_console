#!/usr/bin/env python

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from vga_ext_types import *
from fifo_mod import *
from bram_mod import *


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
		loc.fifo = m.submodules.fifo \
			= Fifo \
			(
				shape_t=rec_to_shape(VgaColors()),
				SIZE=self.FIFO_SIZE()
			)
		#--------

		#--------
		loc.col = VgaColors()
		loc.visib = Signal()
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
		loc.PIXEL_EN = (loc.clk_cnt == 0x0)
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
		with m.If(loc.PIXEL_EN): 
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
		m.d.comb += loc.visib.eq((loc.hsc["s"] == loc.Tstate.VISIB)
			& (loc.vsc["s"] == loc.Tstate.VISIB))

		with m.If(loc.PIXEL_EN):
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
						#bus.col.r.eq(0xf),
						#bus.col.g.eq(0x0),
						#bus.col.b.eq(0x0),
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

		#--------
		# Implement VgaDriver bus to Fifo bus transaction
		m.d.comb \
		+= [
			bus.buf.can_prep.eq(~loc.fifo.bus().full),
			loc.fifo.bus().wr_en.eq(bus.buf.prep),
			loc.fifo.bus().wr_data.eq(bus.buf.col),
		]
		#--------

		#--------
		# Implement grabbing pixels from the FIFO.
		# This is done with an assumption that the VgaDriver's clock rate
		# is four times as great as the pixel clock.
		loc.FIFO_NOT_EMPTY = ~loc.fifo.bus().empty
		loc.START_GRAB_FROM_FIFO = loc.FIFO_NOT_EMPTY \
			& (loc.clk_cnt == (self.CLK_CNT_WIDTH() - 3))
		loc.END_GRAB_FROM_FIFO = loc.FIFO_NOT_EMPTY \
			& (loc.clk_cnt == (self.CLK_CNT_WIDTH() - 1))

		with m.If(loc.START_GRAB_FROM_FIFO):
			m.d.sync += loc.fifo.bus().rd_en.eq(0b1)
		with m.Elif(loc.END_GRAB_FROM_FIFO):
			m.d.sync += loc.col.eq(loc.fifo.bus().rd_data)
		with m.Else():
			m.d.sync \
			+= [
				loc.fifo.bus().rd_en.eq(0b0),
				loc.col.r.eq(0xf),
				loc.col.g.eq(0xf),
				loc.col.b.eq(0x0),
			]
		#--------

		#--------
		return m
		#--------
