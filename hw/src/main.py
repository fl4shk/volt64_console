#!/usr/bin/env python3

import sys

#from libcheesevoyage.misc_util import *
from misc_util import *
from misc_util_running import *
from top_mod import *
from general.fifo_mods import *
#from libcheesevoyage.general.container_types import *
#from libcheesevoyage.general.tests.container_types_mods import VectorAdd
from general.container_types import *
from general.tests.container_types_mods import *
from volt32_cpu.long_udiv_mods import *

from nmigen import *
from nmigen.sim import *

from nmigen.cli import main, main_parser, main_runner
from nmigen_boards.de0_cv import *

from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.back import verilog


def program(mod_name, **kw_args):
	#top = Top(DE0CVPlatform())

	#top.platform().build(top, do_program=True)

	mod = mod_name(platform=DE0CVPlatform(), **kw_args)
	mod.platform().build(mod, do_program=True)

if __name__ == "__main__":
	#to_verilog(VectorAdd, ElemKindT=4, SIZE=2)
	#to_verilog(AddChosenScalars, ElemKindT=4, SIZE=2)
	#e = Packrec \
	#	([
	#		("a", 6),
	#		("b", [("c", 3), ("d", 9)]),
	#		("f", Packarr.Shape(5, 7))
	#	])
	#printerr(e[0], "\n")
	#printerr(e.a.word_select(e.f[0], 3), "\n")
	#printerr(e.b.c.word_select(0, 3), "\n")
	#printerr(type(Value.cast(e.a)), "\n")

	#formal(Fifo, ShapeT=unsigned(8), SIZE=4)
	#formal(AsyncReadFifo, ShapeT=unsigned(8), SIZE=4)
	#program(Top)

	#formal(LongUdiv, MAIN_WIDTH=4, DENOM_WIDTH=4, CHUNK_WIDTH=3)
	#formal(LongUdiv, MAIN_WIDTH=7, DENOM_WIDTH=3, CHUNK_WIDTH=2)

	#formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8, CHUNK_WIDTH=3)
	#formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8, CHUNK_WIDTH=3)
	#formal(LongUdivIterSync,
	#	constants=LongUdivConstants
	#	(
	#		MAIN_WIDTH=3,
	#		DENOM_WIDTH=3,
	#		CHUNK_WIDTH=2,
	#	))

	#parser = main_parser()
	#args = parser.parse_args()

	#dut_constants \
	#	= LongUdivConstants \
	#	(
	#		MAIN_WIDTH=3,
	#		DENOM_WIDTH=3,
	#		CHUNK_WIDTH=2,
	#		FORMAL=True,
	#	)
	#m = Module()
	#m.submodules.dut = dut = LongUdivIterSync(constants=dut_constants)
	#main_runner(parser, args, m, ports=ports(dut.bus()))

	#dut \
	#	= LongUdivIterSync \
	#	(
	#		constants=LongUdivConstants
	#		(
	#			MAIN_WIDTH=3,
	#			DENOM_WIDTH=3,
	#			CHUNK_WIDTH=2
	#		)
	#	)
	#bus = dut.bus()
	##dut_ports = [ClockSignal(), ResetSignal()]
	##dut_ports += [bus.itd_out_sync]
	##main(dut, ports=(ports(bus.it_bus.itd_in)
	##	+ inner_ports(bus.it_bus.itd_out)
	##	+ inner_ports(bus.itd_out_sync)))
	##main(dut, ports=ports(bus))
	##dut_ports = inner_ports(bus)
	#main(dut, ports=ports(bus))

	#to_verilog(LongUdivMultiCycle,
	#	MAIN_WIDTH=3,
	#	DENOM_WIDTH=3,
	#	CHUNK_WIDTH=2)
	#formal(LongUdivMultiCycle,
	#	MAIN_WIDTH=8,
	#	DENOM_WIDTH=8,
	#	CHUNK_WIDTH=2)

	#formal(LongUdivMultiCycle,
	#	MAIN_WIDTH=4,
	#	DENOM_WIDTH=4,
	#	CHUNK_WIDTH=2)
	formal(LongUdivMultiCycle,
		MAIN_WIDTH=8,
		DENOM_WIDTH=8,
		CHUNK_WIDTH=4)

	#for CHUNK_WIDTH in range(1, 4 + 1):
	#	formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8,
	#		CHUNK_WIDTH=CHUNK_WIDTH)
	#formal(LongUdiv, MAIN_WIDTH=16, DENOM_WIDTH=12, CHUNK_WIDTH=3)
	#formal(LongUdiv, MAIN_WIDTH=16, DENOM_WIDTH=10, CHUNK_WIDTH=5)
	#for MAIN_WIDTH in range(1, 16 + 1):
	#	for DENOM_WIDTH in range(1, 16 + 1):
	#		for CHUNK_WIDTH in range(1, 8 + 1):
	#			formal(LongUdiv, MAIN_WIDTH=MAIN_WIDTH,
	#				DENOM_WIDTH=DENOM_WIDTH, CHUNK_WIDTH=CHUNK_WIDTH)
	#formal(LongUdiv, MAIN_WIDTH=7, DENOM_WIDTH=7, CHUNK_WIDTH=2)


#temp = [enc_simm(x, 5) for x in [-0xa, 0xa, 0x0, 0xff, -0x1f]]
#for t in temp:
#	#print("{}, {}, {}".format(t.top, t.bot, hex(t.dbg)))
#	#print(hex(t.dbg))
#	print(t.wont_fit,
#		t.bot_list[::-1], t.top_list[::-1], hex(t.bot), hex(t.top),
#		hex(t.dbg))

#print([(x, ltoi(itol(x, 8))) for x in list(range(-4, 5))])
#print(itol(-3, 8), ltoi(itol(-3, 8)))
#print(itol(3, 8), ltoi(itol(3, 8)))
