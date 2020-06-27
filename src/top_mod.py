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


		#vga.HTIMING = vga.TIMING_INFO.HTIMING()
		#vga.VTIMING = vga.TIMING_INFO.VTIMING()

		#vga.Tstate = VgaTiming.State
		#vga.hsc \
		#= {
		#	"s": Signal(width_from_len(vga.Tstate),
		#		reset=vga.Tstate.FRONT),
		#	"c": Signal(vga.HTIMING.COUNTER_WIDTH()),
		#}
		#vga.vsc \
		#= {
		#	"s": Signal(width_from_len(vga.Tstate),
		#		reset=vga.Tstate.FRONT),
		#	"c": Signal(vga.VTIMING.COUNTER_WIDTH()),
		#}

		## Clocks Per Pixel
		#vga.CPP = self.__MAIN_CLK_RATE // vga.TIMING_INFO.PIXEL_CLK()

		## Clock counter, used to figure out when we can update the VGA pins
		#vga.CLK_CNT_WIDTH = width_from_arg(vga.CPP)
		#vga.clk_cnt = Signal(vga.CLK_CNT_WIDTH)

		#vga.clk_cnt_p_1 = Signal(vga.CLK_CNT_WIDTH)
		#m.d.comb += vga.clk_cnt_p_1.eq(vga.clk_cnt + 0b1)

		#with m.If(vga.clk_cnt_p_1 < vga.CPP):
		#	m.d.dom += vga.clk_cnt.eq(vga.clk_cnt_p_1)
		#with m.Else():
		#	m.d.dom += vga.clk_cnt.eq(0x0)

		#vga.PIXEL_EN = (vga.clk_cnt == 0x0)


		#with m.If(vga.PIXEL_EN):
		#	vga.HTIMING.update_state_cnt(m, vga.hsc)

		#	# Black border
		#	with m.If((vga.hsc["s"] != vga.Tstate.VISIB)
		#		| (vga.vsc["s"] != vga.Tstate.VISIB)):
		#		m.d.dom \
		#		+= [
		#			self.vga().r.eq(0b0000),
		#			self.vga().g.eq(0b0000),
		#			self.vga().b.eq(0b0000),
		#		]

		#	with m.Else():
		#		# Display image here
		#		m.d.dom \
		#		+= [
		#			self.vga().r.eq(0b1111),
		#			self.vga().g.eq(0b0000),
		#			self.vga().b.eq(0b1111),
		#		]

		#	with m.Switch(vga.hsc["s"]):
		#		with m.Case(vga.Tstate.FRONT):
		#			m.d.dom += self.vga().hs.eq(0b1)
		#		with m.Case(vga.Tstate.SYNC):
		#			m.d.dom += self.vga().hs.eq(0b0)
		#		with m.Case(vga.Tstate.BACK):
		#			m.d.dom += self.vga().hs.eq(0b1)
		#		with m.Case(vga.Tstate.VISIB):
		#			m.d.dom += self.vga().hs.eq(0b1),
		#			with m.If((vga.hsc["c"] + 0x1) >= vga.HTIMING.visib()):
		#				vga.VTIMING.update_state_cnt(m, vga.vsc)

		#	with m.Switch(vga.vsc["s"]):
		#		with m.Case(vga.Tstate.FRONT):
		#			m.d.dom += self.vga().vs.eq(0b1)
		#		with m.Case(vga.Tstate.SYNC):
		#			m.d.dom += self.vga().vs.eq(0b0)
		#		with m.Case(vga.Tstate.BACK):
		#			m.d.dom += self.vga().vs.eq(0b1)
		#		with m.Case(vga.Tstate.VISIB):
		#			m.d.dom += self.vga().vs.eq(0b1)
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
