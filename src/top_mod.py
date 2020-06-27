#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from vga_ext_types import *
from vga_driver_mod import *
from bram_mod import *

class Top(Elaboratable):
	#--------
	def __init__(self, platform):
		self.__platform = platform
		self.__MAIN_CLK_RATE = 100

		#self.__clk50 = self.platform().request("clk50", 0)
		self.__vga = self.platform().request("vga", 0)
		self.__ps2_kb = self.platform().request("ps2_host", 0)
		self.__ps2_mouse = self.platform().request("ps2_host", 1)
	#--------

	#--------
	def platform(self):
		return self.__platform
	#--------

	#--------
	#def clk50(self):
	#	return self.__clk50
	def vga(self):
		return self.__vga
	def ps2_kb(self):
		return self.__ps2_kb
	def ps2_mouse(self):
		return self.__ps2_mouse
	#--------

	#--------
	def __elab_build_pll100(self, m):
		return inst_pll("pll_50_to_100_mod.v", "dom", "pll_50_to_100",
			self.__MAIN_CLK_RATE, self.platform(), m)
	#--------

	#--------
	def __elab_build_io_vecs(self, m):
		ret = Blank()
		ret.led = Signal(10)
		ret.button = Signal(4)
		ret.switch = Signal(10)

		for i in range(len(ret.led)):
			led = self.platform().request("led", i)
			m.d.comb += led.eq(ret.led[i])

		for i in range(len(ret.button)):
			button = self.platform().request("button", i)
			m.d.comb += ret.button[i].eq(button)

		for i in range(len(ret.switch)):
			switch = self.platform().request("switch", i)
			m.d.comb += ret.switch[i].eq(switch)
		return ret
	#--------

	def elaborate(self, platform: str):
		#--------
		m = Module()
		#--------

		#--------
		pll100 = self.__elab_build_pll100(m)
		io = self.__elab_build_io_vecs(m)
		#--------

		#--------
		# VGA
		vga = Blank()
		vga.TIMING_INFO = VGA_TIMING_INFO_DICT["640x480@60"]
		vga.NUM_BUF_SCANLINES = 2

		vga.driver = m.submodules.vga_driver \
			= VgaDriver \
			(
				CLK_RATE=self.__MAIN_CLK_RATE,
				#CLK_RATE=50,
				TIMING_INFO=vga.TIMING_INFO,
				NUM_BUF_SCANLINES=vga.NUM_BUF_SCANLINES,
			)
		vga.drbus = vga.driver.bus()
		m.d.comb \
		+= [
			vga.drbus.clk.eq(ClockSignal("dom")),
			vga.drbus.en.eq(io.switch[0]),

			self.vga().r.eq(vga.drbus.col.r),
			self.vga().g.eq(vga.drbus.col.g),
			self.vga().b.eq(vga.drbus.col.b),
			self.vga().hs.eq(vga.drbus.hsync),
			self.vga().vs.eq(vga.drbus.vsync),
		]
		##--------

		#--------
		#CNTR_32_WIDTH = 32
		#cntr_32 = Blank()
		#cntr_32.slow = Signal(unsigned(CNTR_32_WIDTH), reset=0)
		#cntr_32.fast = Signal(unsigned(CNTR_32_WIDTH), reset=0)

		#m.d.sync += cntr_32.slow.eq(cntr_32.slow - 0b1)
		#m.d.dom += cntr_32.fast.eq(cntr_32.fast - 0b1)

		#m.d.comb += io.led[0:5].eq(~cntr_32.slow[27:32])
		#m.d.comb += io.led[5:10].eq(~cntr_32.fast[27:32])
		#--------

		#--------
		return m
		#--------
