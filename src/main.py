#!/usr/bin/env python3

import sys

from misc_util import *
#from top_mod import *
from fifo_mods import *


from nmigen import *
from nmigen.cli import main, main_parser, main_runner
from nmigen_boards.de0_cv import *

from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

def to_verilog(dut_mod, **kw_args):
	#alu = Alu(8)
	#main(alu, 
	#	ports
	#	=[
	#		alu.bus.a, alu.bus.b, alu.bus.carry_in, alu.bus.op,
	#		alu.bus.result, alu.bus.carry_out
	#	])
	dut = dut_mod(**kw_args)
	main(dut, ports=dut.bus().ports())

def formal(dut_mod, **kw_args):
	parser = main_parser()
	args = parser.parse_args()
	m = Module()
	m.submodules.dut = dut = dut_mod(**kw_args, FORMAL=True)

	main_runner(parser, args, m, ports=dut.bus().ports())

def program(mod_name, **kw_args):
	#top = Top(DE0CVPlatform())

	#top.platform().build(top, do_program=True)

	mod = mod_name(platform=DE0CVPlatform(), **kw_args)
	mod.platform().build(mod, do_program=True)

if __name__ == "__main__":
	#formal(Fifo, ShapeT=unsigned(8), SIZE=4)
	#formal(FwftFifo, ShapeT=unsigned(8), SIZE=4)
	program(Top)
