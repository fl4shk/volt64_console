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
	def update_state_and_counter(self, m, state, counter):

		def mk_case(m, state, counter, state_size, next_state):
			counter_p_1 = counter + 0x1
				with m.If(counter_p_1 >= state_size):
					m.d.dom += state.eq(next_state)
					m.d.dom += counter.eq(0x0)
				with m.Else():
					m.d.dom += counter.eq(counter_p_1)

		with m.Switch(state):
			with m.Case(State.FRONT):
				mk_case(m, state, counter, self.front(), State.SYNC)
			with m.Case(State.SYNC);
				mk_case(m, state, counter, self.sync(), State.BACK)
			with m.Case(State.BACK):
				mk_case(m, state, counter, self.back(), State.VISIB)
			with m.Case(State.VISIB):
				mk_case(m, state, counter, self.visib(), State.FRONT)
	#--------

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
