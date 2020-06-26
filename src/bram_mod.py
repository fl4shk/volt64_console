#!/usr/bin/env python3

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

#--------
class BramBusLayout(Layout):
	def __init__(self, DATA_WIDTH, SIZE):
		self.__DATA_WIDTH, self.__ADDR_WIDTH, self.__SIZE \
			= DATA_WIDTH, width_from_arg(SIZE), SIZE

		super().__init__ \
		([
			#--------
			("clk", 1, "i"),
			("rst", 1, "i"),
			#--------

			#--------
			("rd_data", self.DATA_WIDTH(), "o"),
			("rd_addr", self.ADDR_WIDTH(), "i"),
			#--------

			#--------
			("wr_en", 1, "i"),
			("wr_data", self.DATA_WIDTH(), "i"),
			("wr_addr", self.ADDR_WIDTH(), "i"),
			#--------
		])

	def DATA_WIDTH(self):
		return self.__DATA_WIDTH
	def ADDR_WIDTH(self):
		return self.__ADDR_WIDTH
	def SIZE(self):
		return self.__SIZE

	def prep_write(self, dom, wr_data, wr_addr):
		dom += self.wr_en.eq(0b1)
		dom += self.wr_data.eq(wr_data)
		dom += self.wr_addr.eq(wr_addr)
	def stop_write(self, dom):
		dom += self.wr_en.eq(0b0)

class BramBus(Record):
	def __init__(self, DATA_WIDTH, SIZE):
		super().__init__(BramBusLayout(DATA_WIDTH, SIZE))
#--------

#--------
class Bram(Elaboratable):
	def __init__(self, DATA_WIDTH, SIZE):
		self.bus = BramBus(DATA_WIDTH, SIZE)

	def elaborate(self, platform: str):
		#--------
		m = Module()

		add_clk_domain(m, self.bus.clk)
		#--------

		#--------
		# Local signals
		arr = Array([Signal(self.bus.DATA_WIDTH(), reset=0x0)
			for _ in self.bus.SIZE()])
		#--------

		#--------
		# Behavioral code
		with m.If(self.bus.rst):
			for i in range(len(arr)):
				m.d.dom += arr[i].eq(0x0)

			m.d.dom += self.bus.rd_data.eq(0x0)
		with m.Else():
			with m.If(self.bus.wr_en):
				m.d.dom += arr[self.bus.wr_addr].eq(self.bus.wr_data)

			# No error checking in the case of `wr_addr == rd_addr`.
			m.d.dom += self.bus.rd_data.eq(arr[self.bus.rd_addr])
		#--------

		#--------
		return m
		#--------
#--------
