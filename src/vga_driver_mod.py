#!/usr/bin/env python

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from vga_ext_types import *
from bram_mod import *



class VgaDriverBusLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			# Clock and global VGA driving enable
			("clk", unsigned(1), "i"),
			("en", unsigned(1), "i"),

			# VGA physical pins
			("col", VgaColorsLayout(), "o"),
			("hsync", self.__unsgn_sync(), "o"),
			("vsync", self.__unsgn_sync(), "o"),

			# Pixel buffer
			("buf", VgaDriverBufLayout()),
		])

	def __unsgn_sync(self):
		return unsigned(1)

	def drive_hsync(hsync_sig, inv_hsync):
		return hsync_sig.eq(~inv_hsync)
	def drive_vsync(vsync_sig, inv_vsync):
		return vsync_sig.eq(~inv_vsync)

class VgaDriverBus(Record):
	def __init__(self):
		super().__init__(VgaDriverBusLayout())

class VgaDriver(Elaboratable):
	def __init__(self, CPP, HTIMING, VTIMING, NUM_BUF_SCANLINES):
		self.bus = VgaDriverBus()

		# clocks per pixel
		self.__CPP = CPP
		self.__HTIMING = HTIMING
		self.__VTIMING = VTIMING
		self.__NUM_BUF_SCANLINES = NUM_BUF_SCANLINES

	def CPP(self):
		return self.__CPP
	def HTIMING(self):
		return self.__HTIMING
	def VTIMING(self):
		return self.__VTIMING
	def NUM_BUF_SCANLINES(self):
		return self.__NUM_BUF_SCANLINES
	def FB_SIZE(self):
		ret = Blank()
		ret.x, ret.y = self.HTIMING().visib(), self.VTIMING().visib()
		return ret
	def CLK_COUNTER_WIDTH(self):
		return width_from_arg(self.CPP())

	def elaborate(self, platform: str):
		#--------
		m = Module()
		#--------

		#--------
		add_clk_domain(m, self.bus.clk)
		#--------

		#--------
		#--------

		#--------
		# Implement the clock enable
		CLK_COUNTER_WIDTH = self.CLK_COUNTER_WIDTH()
		clk_counter = Signal(CLK_COUNTER_WIDTH)

		# Force this addition to be of width `CLK_COUNTER_WIDTH + 1` to
		# prevent wrap-around
		clk_counter_p_1 = Signal(CLK_COUNTER_WIDTH + 1)
		m.d.comb += clk_counter_p_1.eq(clk_counter + 0b1)

		# Implement wrap-around for the clock counter
		with m.If(self.bus.en == 0b1):
			with m.If(clk_counter_p_1 < self.CPP()):
				m.d.dom += clk_counter.eq(clk_counter_p_1)
			with m.Else():
				m.d.dom += clk_counter.eq(0x0)
		with m.Else();
			m.d.dom += clk_counter.eq(0x0)

		# Since this is an alias, use ALL_CAPS for its name.
		PIXEL_EN = ((self.bus.en == 0b1) & (clk_counter == 0x0))
		#--------

		#--------
		#h_counter = Signal(self.__HTIMING.COUNTER_WIDTH())
		#h_state = VgaTiming.State.FRONT
		#--------

		#--------
		return m
		#--------
