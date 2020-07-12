#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

from gfx.vga_ext_types import *
from gfx.vga_driver_mod import *
from gfx.video_ditherer_mod import *
from general.sdram_ctrl_mod import *
#from bram_mod import *

class Top(Elaboratable):
	#--------
	def __init__(self, platform):
		self.__platform = platform
		self.__MAIN_CLK_RATE = 100

		#self.__clk50 = self.platform().request("clk50", 0)
		self.__vga = self.platform().request("vga", 0)
		self.__ps2_kb = self.platform().request("ps2_host", 0)
		self.__ps2_mouse = self.platform().request("ps2_host", 1)
		self.__sd_card = self.platform().request("sd_card_spi", 0)
		self.__sdram = self.platform().request("sdram", 0)
	#--------

	#--------
	def platform(self):
		return self.__platform
	def MAIN_CLK_RATE(self):
		return self.__MAIN_CLK_RATE
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
	def sd_card(self):
		return self.__sd_card
	def sdram(self):
		return self.__sdram
	#--------

	#--------
	def __elab_build_pll100(self, m):
		return inst_pll("pll_50_to_100_mod.v", "dom", "pll_50_to_100",
			self.MAIN_CLK_RATE(), self.platform(), m)
	#--------

	#--------
	def __elab_build_io(self, m):
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

	def elaborate(self, platform: str):
		#--------
		m = Module()
		#--------

		#--------
		pll100 = self.__elab_build_pll100(m)
		io = self.__elab_build_io(m)

		loc = Blank()
		loc.dom_rst = ResetSignal("dom")
		loc.past_dom_rst = Signal()
		m.d.dom += loc.past_dom_rst.eq(loc.dom_rst)
		#--------

		#--------
		# VGA
		vga = Blank()
		vga.m = Blank()

		vga.TIMING_INFO = VGA_TIMING_INFO_DICT["640x480@60"]
		vga.FIFO_SIZE = 16

		vga.m.driver = m.submodules.vga_driver \
			= DomainRenamer({"sync": "dom"}) \
			(
				VgaDriver \
				(
					CLK_RATE=self.MAIN_CLK_RATE(),
					TIMING_INFO=vga.TIMING_INFO,
					#NUM_BUF_SCANLINES=vga.NUM_BUF_SCANLINES,
					FIFO_SIZE=vga.FIFO_SIZE,
				)
			)
		vga.drbus = vga.m.driver.bus()
		#vga.col = RgbColor()

		vga.m.ditherer = m.submodules.video_ditherer \
			= DomainRenamer({"sync": "dom"}) \
			(
				VideoDitherer \
				(
					FB_SIZE=vga.m.driver.FB_SIZE(),
					#drbus=vga.drbus,
					#col=vga.col,
				)
			)
		vga.dibus = vga.m.ditherer.bus()

		vga.col = vga.dibus.col_in

		m.d.comb \
		+= [
			vga.drbus.en.eq(io.switch[0]),
			vga.drbus.buf.col.eq(vga.dibus.col_out),

			#vga.dibus.en.eq(0b1),

			self.vga().r.eq(vga.drbus.col.r),
			self.vga().g.eq(vga.drbus.col.g),
			self.vga().b.eq(vga.drbus.col.b),
			self.vga().hs.eq(vga.drbus.hsync),
			self.vga().vs.eq(vga.drbus.vsync),
		]

		#m.d.comb \
		#+= [
		#]

		with m.If(vga.drbus.buf.can_prep):
			m.d.dom \
			+= [
				vga.drbus.buf.prep.eq(0b1),
				vga.dibus.en.eq(0b1),
			]

			with m.If(vga.dibus.next_pos.x == 0x0):
				m.d.dom += vga.col.r.eq(0x0)
			with m.Else(): # If(vga.dibus.next_pos.x > 0x0)
				m.d.dom += vga.col.r.eq(vga.col.r + 0x1)
			#m.d.dom += vga.col.r.eq(vga.col.r + 0x1)

			m.d.dom += vga.col.g.eq(0x0)
			m.d.dom += vga.col.b.eq(0x0)
		with m.Else(): # If(~vga.drbus.buf.can_prep):
			m.d.dom \
			+= [
				#vga.drbus.buf.prep.eq(0b0),
				vga.dibus.en.eq(0b0),
			]

		#with m.If(vga.drbus.pixel_en & vga.drbus.visib
		#	& vga.drbus.buf.can_prep):

		#	#m.d.dom += vga.past_col.eq(vga.col)

		#	m.d.dom += vga.drbus.buf.prep.eq(0b1)

		#	with m.If(vga.drbus.draw_pos.x >= 0x10):
		#		m.d.dom += vga.col.r.eq(vga.col.r + 0x1)

		#	with m.If(vga.drbus.draw_pos.y >= 0x10):
		#		m.d.dom += vga.col.g.eq(vga.col.g + 0x1)

		#	m.d.dom += vga.col.b.eq(0x0)
		#with m.Else():
		#	m.d.dom \
		#	+= [
		#		vga.drbus.buf.prep.eq(0b0)
		#	]

		#--------

		#--------
		return m
		#--------
