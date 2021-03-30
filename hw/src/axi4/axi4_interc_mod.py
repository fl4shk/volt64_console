#!/usr/bin/env python3

import math
from misc_util import *
from nmigen import *
from nmigen.hd.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto


#--------
class Axi4IntercInstInfo:
	#--------
	def __init__(self, ModT, InpT, OutpT, BASE_ADDR, AXI_ADDR_WIDTH,
		AXI_DATA_WIDTH):
		self.__ModT = ModT
		self.__InpT = InpT
		self.__OutpT = OutpT
		self.__BASE_ADDR = BASE_ADDR
		self.__AXI_ADDR_WIDTH = AXI_ADDR_WIDTH
		self.__AXI_DATA_WIDTH = AXI_DATA_WIDTH
	#--------
	def ModT(self):
		return self.__ModT
	def InpT(self):
		return self.__InpT
	def OutpT(self):
		return self.__OutpT
	def BASE_ADDR(self):
		return self.__BASE_ADDR
	def AXI_ADDR_WIDTH(self):
		return self.__AXI_ADDR_WIDTH
	def AXI_DATA_WIDTH(self):
		return self.__AXI_DATA_WIDTH
	#--------
#--------
class Axi4Interc(Elaboratable):
	#--------
	def __init__(self):
		pass
	#--------
