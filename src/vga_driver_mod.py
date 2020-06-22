#!/usr/bin/env python

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

#class VgaDriverBusLayout(Layout):
#	def __init__(self):
#		super().__init__\
#		([
#			("clk", unsigned(1)),
#
#			("r", self.__unsgn_color()),
#			("g", self.__unsgn_color()),
#			("b", self.__unsgn_color()),
#			("hsync", self.__unsgn_sync()),
#			("vsync", self.__unsgn_sync()),
#		])
#
#	def __unsgn_color(self):
#		return unsigned(4)
#	def __unsgn_sync(self):
#		return unsigned(1)


class VgaTiming:
	def __init__(self, visib, front, sync, back):
		self.__visib, self.__front, self.__sync, self.__back \
			= visib, front, sync, back

	def visib(self):
		return self.__visib
	def front(self):
		return self.__front
	def sync(self):
		return self.__sync
	def back(self):
		return self.__back

	# This is specifically the minimum width instead of like, 32-bit or
	# something
	def COUNTER_WIDTH(self):
		return width_from_arg(self.visib() + self.front() + self.sync()
			+ self.back())

class VgaColorsLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			("r", self.__unsgn_color()),
			("g", self.__unsgn_color()),
			("b", self.__unsgn_color()),
		])

	def COLOR_WIDTH(self):
		return 4
	def __unsgn_color(self):
		return unsigned(self.COLOR_WIDTH())

	def drive(self, other):
		return Cat(self.r, self.g, self.b) \
			.eq(Cat(other.r, other.g, other.b))

def VgaColors(Record):
	def __init__(self):
		super().__init__(VgaColorsLayout())

class VgaDriverBufLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			("can_prep", unsigned(1), "o"),
			("prep", unsigned(1), "i"),
			("col", VgaColorsLayout(), "i"),
		])

class VgaDriverBusLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			("clk", unsigned(1), "i"),

			("col", VgaColorsLayout(), "o"),
			("hsync", self.__unsgn_sync(), "o"),
			("vsync", self.__unsgn_sync(), "o"),

			("buf", VgaDriverBufLayout()),
		])

	def __unsgn_sync(self):
		return unsigned(1)

	def drive_hsync(self, inv_hsync):
		return self.hsync.eq(~inv_hsync)
	def drive_vsync(self, inv_vsync):
		return self.vsync.eq(~inv_vsync)
class VgaDriverBus(Record):
	def __init__(self):
		super().__init__(VgaDriverBusLayout())

class VgaDriver(Elaboratable):
	def __init__(self, cpp, htiming, vtiming):
		self.bus = VgaDriverBus()

		# clocks per pixel
		self.__cpp = cpp
		self.__htiming = htiming
		self.__vtiming = vtiming


	def elaborate(self, platform: str):
		#--------
		m = Module()
		#--------

		#--------
		add_clk_domain(m, "dom", self.bus.clk)
		#--------

		#--------
		clk_counter = Signal(unsigned(width_from_arg(self.__cpp)),
			reset=self.__cpp - 1)

		# Implement wrap-around for the clock counter
		clk_counter_p_1 = clk_counter + 0x1
		with m.If(clk_counter_p_1 < self.__cpp):
			m.d.dom += clk_counter.eq(clk_counter_p_1)
		with m.Else():
			m.d.dom += clk_counter.eq(0x0)
		#--------

		#--------
		#--------

		#--------
		return m
		#--------
