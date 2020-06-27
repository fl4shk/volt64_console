#!/usr/bin/env python3

from enum import Enum, auto, unique

from misc_util import *
from nmigen import *
from nmigen.hdl.rec import *

class VgaTiming:
	def __init__(self, visib, front, sync, back):
		self.__visib, self.__front, self.__sync, self.__back \
			= visib, front, sync, back
		#self.__state = Signal(unsigned(width_from_len(State)),
		#	reset=State.FRONT)
		#self.__state_counter = Signal(unsigned(self.COUNTER_WIDTH()),
		#	reset=0x0)

	#--------
	class State(Enum):
		FRONT = 0
		SYNC = auto()
		BACK = auto()
		VISIB = auto()
	#--------

	#--------
	def visib(self):
		return self.__visib
	def front(self):
		return self.__front
	def sync(self):
		return self.__sync
	def back(self):
		return self.__back
	#--------

	#--------
	# This is specifically the minimum width instead of like, 32-bit or
	# something
	def COUNTER_WIDTH(self):
		return max \
			([
				width_from_arg(arg)
				for arg in [self.visib(), self.front(), self.sync(),
					self.back()]
			])
	#--------

	#--------
	def update_state_cnt(self, m, state_cnt):
		def mk_case(m, state_cnt, state_size, next_state):
			counter_p_1 = state_cnt["c"] + 0x1
			with m.If(counter_p_1 >= state_size):
				m.d.dom += state_cnt["s"].eq(next_state)
				m.d.dom += state_cnt["c"].eq(0x0)
			with m.Else():
				m.d.dom += state_cnt["c"].eq(counter_p_1)

		State = VgaTiming.State
		with m.Switch(state_cnt["s"]):
			with m.Case(State.FRONT):
				mk_case(m, state_cnt, self.front(), State.SYNC)
			with m.Case(State.SYNC):
				mk_case(m, state_cnt, self.sync(), State.BACK)
			with m.Case(State.BACK):
				mk_case(m, state_cnt, self.back(), State.VISIB)
			with m.Case(State.VISIB):
				mk_case(m, state_cnt, self.visib(), State.FRONT)
	#--------

class VgaTimingInfo:
	def __init__(self, PIXEL_CLK, HTIMING, VTIMING):
		self.__PIXEL_CLK, self.__HTIMING, self.__VTIMING \
			= PIXEL_CLK, HTIMING, VTIMING
	def PIXEL_CLK(self):
		return self.__PIXEL_CLK
	def HTIMING(self):
		return self.__HTIMING
	def VTIMING(self):
		return self.__VTIMING


class VgaColorsLayout(Layout):
	def __init__(self, COLOR_WIDTH=4):
		self.__COLOR_WIDTH = COLOR_WIDTH
		super().__init__ \
		([
			("r", self.__unsgn_color()),
			("g", self.__unsgn_color()),
			("b", self.__unsgn_color()),
		])

	def COLOR_WIDTH(self):
		return self.__COLOR_WIDTH
	def __unsgn_color(self):
		return unsigned(self.COLOR_WIDTH())

	def drive(self, other):
		return Cat(self.r, self.g, self.b) \
			.eq(Cat(other.r, other.g, other.b))

class VgaColors(Record):
	def __init__(self):
		super().__init__(VgaColorsLayout())

	def COLOR_WIDTH(self):
		return self.layout.COLOR_WIDTH()
	def drive(self, other):
		self.layout.drive(other)

class VgaDriverBufLayout(Layout):
	def __init__(self):
		super().__init__ \
		([
			("can_prep", unsigned(1)),
			("prep", unsigned(1)),
			("col", VgaColorsLayout()),
		])
