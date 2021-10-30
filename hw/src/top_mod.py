#!/usr/bin/env python3

from nmigen import *
from nmigen_boards import *
from nmigen.build.dsl import *

from libcheesevoyage import *
#from bram_mod import *

class Top(Elaboratable):
	#--------
	def __init__(self, platform):
		self.__platform = platform
		self.__MAIN_CLK_RATE = 100

		self.__pins = Blank()
		#self.pins().clk50 = self.platform().request("clk50", 0)
		self.pins().vga = self.platform().request("vga", 0)
		self.pins().ps2_kb = self.platform().request("ps2", 0)
		self.pins().ps2_mouse = self.platform().request("ps2", 1)
		self.pins().sd_card = self.platform().request("sd_card_spi", 0)
		self.pins().sdram = self.platform().request("sdram", 0)

		#self.platform().add_resources \
		#([
		#	Resource("vga_rgb6", 0,
		#		Subsignal("r", Pins("1 2 3 4 5 6", dir="o",
		#			conn=("j", 1))))
		#])
		#self.pins().vga_rgb6 = self.platform().request("vga_rgb6", 0)
	#--------
	def platform(self):
		return self.__platform
	def MAIN_CLK_RATE(self):
		return self.__MAIN_CLK_RATE
	#--------
	def pins(self):
		return self.__pins
	#def clk50(self):
	#	return self.__clk50
	#def vga(self):
	#	return self.__vga
	#def ps2_kb(self):
	#	return self.__ps2_kb
	#def ps2_mouse(self):
	#	return self.__ps2_mouse
	#def sd_card(self):
	#	return self.__sd_card
	#def sdram(self):
	#	return self.__sdram
	#--------
	def __elab_build_pll100(self, m: Module):
		return inst_pll("pll_50_to_100_mod.v", "dom", "pll_50_to_100",
			self.MAIN_CLK_RATE(), self.platform(), m)
	#--------
	def __elab_build_io(self, m: Module) -> Blank:
		ret = Blank()
		ret.led, ret.button, ret.switch = Signal(10), Signal(4), Signal(10)

		for i in range(len(ret.led)):
			led = self.platform().request("led", i)
			m.d.comb += led.eq(ret.led[i])

		for i in range(len(ret.button)):
			button = self.platform().request("button", i)
			m.d.comb += ret.button[i].eq(button)

		for i in range(len(ret.switch)):
			switch = self.platform().request("switch", i)
			m.d.comb += ret.switch[i].eq(switch)

		#ret.led, ret.button, ret.switch = [], [], []

		#for i in range(10):
		#	ret.led.append(self.platform().request("led", i))
		#for i in range(4):
		#	ret.button.append(self.platform().request("button", i))
		#for i in range(10):
		#	ret.switch.append(self.platform().request("switch", i))

		return ret
	#--------
	def elaborate(self, platform: str) -> Module:
		#--------
		m = Module()
		#--------
		pll100 = self.__elab_build_pll100(m)
		io = self.__elab_build_io(m)

		loc = Blank()
		loc.dom_rst = ResetSignal("dom")
		loc.past_dom_rst = Signal()
		m.d.dom += loc.past_dom_rst.eq(loc.dom_rst)
		#--------
		# VGA
		vga = Blank()
		vga.m = Blank()

		vga.TIMING_INFO = VGA_TIMING_INFO_DICT["640x480@60"]
		#vga.TIMING_INFO = VGA_TIMING_INFO_DICT["800x600@60"]
		#vga.TIMING_INFO = VGA_TIMING_INFO_DICT["1024x768@60"]
		#vga.TIMING_INFO = VGA_TIMING_INFO_DICT["1280x800@60"]
		vga.FIFO_SIZE = 16

		# Use the 100 MHz clock rate by setting the "sync" domain to "dom"
		# instead
		vga.m.driver = m.submodules.vga_driver \
			= DomainRenamer({"sync": "dom"}) \
			(
				VgaDriver \
				(
					CLK_RATE=self.MAIN_CLK_RATE(),
					TIMING_INFO=vga.TIMING_INFO,
					FIFO_SIZE=vga.FIFO_SIZE,
				)
			)
		vga.drbus = vga.m.driver.bus()
		#vga.col = RgbColor()

		# Use the 100 MHz clock rate by setting the "sync" domain to "dom"
		# instead
		vga.m.ditherer = m.submodules.video_ditherer \
			= DomainRenamer({"sync": "dom"}) \
			(
				VideoDitherer \
				(
					FB_SIZE=vga.m.driver.FB_SIZE(),
				)
			)
		vga.dibus = vga.m.ditherer.bus()

		# Use the 100 MHz clock rate by setting the "sync" domain to "dom"
		# instead
		vga.m.gradient = m.submodules.vga_gradient \
			= DomainRenamer({"sync": "dom"}) \
			(
				VgaGradient \
				(
					vga_drbus=vga.drbus,
					vga_dibus=vga.dibus,
				)
			)

		m.d.comb \
		+= [
			vga.drbus.inp.en.eq(io.switch[0]),
			vga.drbus.inp.buf.col.eq(vga.dibus.outp.col),

			#vga.dibus.en.eq(0b1),

			self.pins().vga.r.eq(vga.drbus.outp.col.r),
			self.pins().vga.g.eq(vga.drbus.outp.col.g),
			self.pins().vga.b.eq(vga.drbus.outp.col.b),
			self.pins().vga.hs.eq(vga.drbus.outp.hsync),
			self.pins().vga.vs.eq(vga.drbus.outp.vsync),
		]
		#--------
		return m
		#--------
