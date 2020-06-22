#!/usr/bin/env python3

from misc_util import *
from enum import Enum, auto, unique
import math

from nmigen import *
from nmigen.hdl.rec import *


@unique
class AluOp(Enum):
	ADD = 0
	ADC = auto()
	SUB = auto()
	SBC = auto()

	def WIDTH():
		return width_from_len(AluOp)

class AluBusLayout(Layout):
	def __init__(self, WIDTH):
		super().__init__ \
		([
			("a", unsigned(WIDTH)),
			("b", unsigned(WIDTH)),
			("carry_in", unsigned(1)),
			("op", unsigned(AluOp.WIDTH())),

			("result", unsigned(WIDTH)),
			("carry_out", unsigned(1)),
		])
class AluBus(Record):
	def __init__(self, WIDTH):
		super().__init__(AluBusLayout(WIDTH))
		self._WIDTH = WIDTH
	def WIDTH(self):
		return self._WIDTH

	def add_with_carry(self, a, b, carry_in):
		return Cat(self.result, self.carry_out) \
			.eq(Cat(Const(0, 1), a) + Cat(Const(0, 1), b)
				+ Cat(Const(0, self.WIDTH()), carry_in))



class Alu(Elaboratable):
	def __init__(self, WIDTH):
		self.bus = AluBus(WIDTH)

	def WIDTH(self):
		return self.bus.WIDTH()

	def elaborate(self, platform: str):
		m = Module()

		with m.Switch(self.bus.op):
			with m.Case(AluOp.ADD):
				m.d.comb += self.bus.add_with_carry \
					(
						a=self.bus.a,
						b=self.bus.b,
						carry_in=0b0
					)
			with m.Case(AluOp.ADC):
				m.d.comb += self.bus.add_with_carry \
					(
						a=self.bus.a,
						b=self.bus.b,
						carry_in=self.bus.carry_in
					)
			with m.Case(AluOp.SUB):
				m.d.comb += self.bus.add_with_carry \
					(
						a=self.bus.a,
						b=~self.bus.b,
						carry_in=0b1
					)
			with m.Case(AluOp.SBC):
				m.d.comb += self.bus.add_with_carry \
					(
						a=self.bus.a,
						b=~self.bus.b,
						carry_in=self.bus.carry_in
					)
			with m.Default():
				m.d.comb += self.bus.add_with_carry \
					(
						a=Const(0, self.WIDTH()),
						b=Const(0, self.WIDTH()),
						carry_in=0b0
					)

		return m
