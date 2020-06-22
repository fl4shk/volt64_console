#!/usr/bin/env python3

from misc_util import *
from top_mod import *


from nmigen import *
from nmigen.cli import main
from nmigen_boards.de0_cv import *


if __name__ == "__main__":
	#alu = Alu(8)
	#main(alu, 
	#	ports
	#	=[
	#		alu.bus.a, alu.bus.b, alu.bus.carry_in, alu.bus.op,
	#		alu.bus.result, alu.bus.carry_out
	#	])

	#blinky = Blinky()

	top = Top(DE0CVPlatform())

	top.platform().build(top, do_program=True)
