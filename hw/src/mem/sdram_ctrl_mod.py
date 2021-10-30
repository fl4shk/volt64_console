#!/usr/bin/env python3

from enum import Enum, auto

from nmigen import *

from libcheesevoyage import *

from interconn.interconn_bus_types import IntrcnNodeBus
#--------
class SdramCtrlParams:
	def __init__(self):
		pass

	def ADDR_WIDTH(self):
		return 13
	def AUTOPRECHARGE_INDEX(self):
		return 10

	def REFRESH_A1_MS(self):
		return 64 
	def REFRESH_A2_MS(self):
		return 16

	def COL_WIDTH(self):
		return 10
	def COL_ADDR_RANGE(self):
		return (0, self.COL_WIDTH())
	def COL_ADDR_SLICE(self):
		addr_range = self.COL_ADDR_RANGE()
		return slice(addr_range[0], addr_range[1])

	def ROW_WIDTH(self):
		return 13
	def ROW_ADDR_RANGE(self):
		low = self.COL_WIDTH()
		return (low, low + ROW_WIDTH())
	def ROW_ADDR_SLICE(self):
		addr_range = self.ROW_ADDR_RANGE()
		return slice(addr_range[0], addr_range[1])

	def BANK_WIDTH(self):
		return 2
	def BANK_ADDR_RANGE(self):
		low = self.ROW_WIDTH() + self.COL_WIDTH()
		return (low, low + self.BANK_WIDTH())
	def BANK_ADDR_SLICE(self):
		addr_range = self.BANK_ADDR_RANGE()
		return slice(addr_range[0], addr_range[1])

	def DQM_WIDTH(self):
		return 2
	def WORD_WIDTH(self):
		return 16

	def FULL_ADDR_WIDTH(self):
		return self.COL_WIDTH() + self.ROW_WIDTH() + self.BANK_WIDTH()
#--------
# "Phys" is short for "Physical"
class SdramCtrlPhysBus:
	def __init__(self):
		self.__PARAMS = SdramCtrlParams()

		self.clk = Signal()
		self.cke = Signal()

		self.cs_n = Signal()

		self.ras_n = Signal()
		self.cas_n = Signal()
		self.we_n = Signal()

		self.ba = Signal(self.PARAMS().BANK_WIDTH())
		self.a = Signal(self.PARAMS().ADDR_WIDTH())
		self.dq = Signal(self.PARAMS().WORD_WIDTH())
		self.dqm = Signal(self.PARAMS().DQM_WIDTH())

	def PARAMS(self):
		return self.__PARAMS

	def phys_cmd(self):
		return Cat(self.ras_n, self.cas_n, self.we_n)

# "Pub" is short for "Public"
class SdramCtrlPubBus(IntrcnNodeBus):
	def __init__(self):
		#--------
		self.__PARAMS = SdramCtrlParams()
		#--------
		self.wr_addr = Signal(self.PARAMS().FULL_ADDR_WIDTH())
		self.wr_data = Signal(self.PARAMS().WORD_WIDTH())

		# Burst up to a full page (one full row)
		self.wr_burst_len = Signal(self.PARAMS().ROW_WIDTH())

		# Handshaking.
		# This is intended to be the same as AXI handshaking, so `valid`
		# is driven by the master of the `SdramCtrl` module, and `ready` is
		# driven by the `SdramCtrl` module.
		self.wr_valid = Signal()
		self.wr_ready = Signal()
		#--------
		#self.rd_addr = Signal(self.PARAMS().FULL_ADDR_WIDTH())
		self.rd_data = Signal(self.PARAMS().WORD_WIDTH())
		self.rd_burst_len = Signal(self.PARAMS().ROW_WIDTH())

		# Handshaking
		self.rd_valid = Signal()
		self.rd_ready = Signal()
		#--------
	def PARAMS(self):
		return self.__PARAMS

	def build_addr(self, bank, row, col):
		return Cat(bank, row, col)
	def build_full_page_addr(self, bank, row):
		return self.build_addr(bank, row, 0x0)

class SdramCtrlBus:
	def __init__(self):
		self.phys = SdramCtrlPhysBus(self.PARAMS())
		self.pub = SdramCtrlPubBus(self.PARAMS())

	def PARAMS(self):
		return self.phys.PARAMS()

	def build_addr(self, bank, row, col):
		return self.pub.build_addr(bank, row, col)
	def build_full_page_addr(self, bank, row):
		return self.pub.build_full_page_addr(bank, row)
#--------
class SdramPhysCmd(Enum):
	READ = auto()
	BST = auto()
	NOP = auto()

class SdramPhysBurstLen(Enum):
	BL_1 = 0b000
	BL_2 = 0b001
	BL_4 = 0b010
	BL_8 = 0b011
	BL_FULL_PAGE = 0b111
#--------
