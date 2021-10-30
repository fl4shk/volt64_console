#!/usr/bin/env python3

from nmigen import *
from nmigen_boards import *

from libcheesevoyage import *

from intrcn.intrcn_bus_types import IntrcnNodeBus

#--------
class Volt32NanoCpuBus:
	#--------
	def __init__(self):
		#--------
		# Note: we're an interconnect host
		self.__intrcn \
			= IntrcnNodeBus \
			(
				ADDR_WIDTH=self.MAIN_WIDTH(),
				DATA_WIDTH=self.MAIN_WIDTH(),
			)
		self.ic_who = self.__intrcn.who
		self.ic_whi = self.__intrcn.whi
		#--------
		self.rem = Splitrec()
		#--------
	#--------
	def MAIN_WIDTH(self):
		return 32
	#--------
#--------
