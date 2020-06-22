#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from vga_driver_mod import *

class Top(Elaboratable):
	def __init__(self, platform):
		self._platform = platform

	def platform(self):
		return self._platform
	def clk50(self):
		return self.platform().request("clk50", 0)

	def vga(self):
		return self.platform().request("vga", 0)

	def ps2_kb(self):
		return self.platform().request("ps2_host", 0)
	def ps2_mouse(self):
		return self.platform().request("ps2_host", 1)

	#--------
	def __elab_build_pll100(self, m):
		return inst_pll("pll_50_to_100_mod.v", "dom", "pll_50_to_100",
			100, self.platform(), m)
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
		#ALU_WIDTH = 3

		#m.submodules.alu = Alu(ALU_WIDTH)

		# 640 x 480 @ 60 Hz, taken from http://www.tinyvga.com
		#vga_driver = m.submodules.vga_driver \
		#	= VgaDriver \
		#	(
		#		cpp=100 // 25,
		#		htiming \
		#			= VgaTiming \
		#			(
		#				visib=640,
		#				front=16,
		#				sync=96,
		#				back=48
		#			),
		#		vtiming \
		#			= VgaTiming \
		#			(
		#				visib=480,
		#				front=10,
		#				sync=2,
		#				back=33
		#			)
		#	)
		#--------

		#--------
		pll100 = self.__elab_build_pll100(m)
		io = self.__elab_build_io_vecs(m)
		#--------

		#--------
		CNTR_32_WIDTH = 32
		cntr_32 = Blank()
		cntr_32.slow = Signal(unsigned(CNTR_32_WIDTH), reset=0)
		cntr_32.fast = Signal(unsigned(CNTR_32_WIDTH), reset=0)

		m.d.sync += cntr_32.slow.eq(cntr_32.slow - 0b1)
		m.d.dom += cntr_32.fast.eq(cntr_32.fast - 0b1)

		m.d.comb += io.led[0:5].eq(~cntr_32.slow[27:32])
		m.d.comb += io.led[5:10].eq(~cntr_32.fast[27:32])
		#--------

		#--------
		#--------

		#--------
		return m
		#--------
