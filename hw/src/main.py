#!/usr/bin/env python3

import sys

from misc_util import *
from top_mod import *
from general.fifo_mods import *
from general.container_types import *
from general.tests.container_types_mods import VectorAdd
from volt32_cpu.long_udiv_mod import *

from nmigen import *
from nmigen.sim import *

from nmigen.cli import main, main_parser, main_runner
from nmigen_boards.de0_cv import *

from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.back import verilog

from tracemalloc import *

def ports(bus):
	def inner_ports(bus):
		ret = []
		for key in bus.__dict__:
			val = bus.__dict__[key]
			if key[0] != "_":
				if isinstance(val, Signal) or isinstance(val, Record):
					ret += [val]
				elif isinstance(val, Packrec):
					#ret += val.flattened()
					ret += [val.sig()]
				#elif isinstance(val, Packarr):
				#	ret += [val.sig()]
				elif isinstance(val, Splitrec):
					ret += val.flattened()
				else:
					ret += inner_ports(val)
		return ret
	return ([ClockSignal(), ResetSignal()] + inner_ports(bus))

def to_verilog(dut_mod, **kw_args):
	dut = dut_mod(**kw_args)
	# ./main.py generate -t verilog
	#main(dut, ports=ports(dut.bus()))
	with open("dut.v.ignore", "w") as f:
		f.write(verilog.convert(dut, ports=ports(dut.bus())))

def formal(dut_mod, **kw_args):
	parser = main_parser()
	args = parser.parse_args()

	m = Module()
	m.submodules.dut = dut = dut_mod(**kw_args, FORMAL=True)

	main_runner(parser, args, m, ports=ports(dut.bus()))

def verify(dut_mod, **kw_args):
	dut = dut_mod(**kw_args, DBG=True)

	sim = Simulator(dut)
	sim.add_clock(1e-6) # 1 MHz
	sim.add_process(dut.verify_process)
	with sim.write_vcd("test.vcd"):
		#sim.run_until(1e-3)
		sim.run()

def program(mod_name, **kw_args):
	#top = Top(DE0CVPlatform())

	#top.platform().build(top, do_program=True)

	mod = mod_name(platform=DE0CVPlatform(), **kw_args)
	mod.platform().build(mod, do_program=True)

if __name__ == "__main__":
	#to_verilog(VectorAdd, ElemKindT=4, SIZE=2)
	e = Packrec \
		([
			("b", 6),
			("a", [("c", 3), ("d", 9)]),
			("f", Packarr.Shape(5, 7))
		])
	printerr(e.a.c.word_select(0, 3), "\n")
	printerr(e.b.word_select(1, 3), "\n")
	#printerr(type(Value.cast(e.a)), "\n")

	##formal(Fifo, ShapeT=unsigned(8), SIZE=4)
	##formal(AsyncReadFifo, ShapeT=unsigned(8), SIZE=4)
	##program(Top)

	##formal(LongUdiv, MAIN_WIDTH=4, DENOM_WIDTH=4, CHUNK_WIDTH=3)
	##formal(LongUdiv, MAIN_WIDTH=7, DENOM_WIDTH=3, CHUNK_WIDTH=2)

	#formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8, CHUNK_WIDTH=3,
	#	PIPELINED=False)
	##formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8, CHUNK_WIDTH=3,
	##	PIPELINED=True)

	##for CHUNK_WIDTH in range(1, 4 + 1):
	##	formal(LongUdiv, MAIN_WIDTH=8, DENOM_WIDTH=8,
	##		CHUNK_WIDTH=CHUNK_WIDTH)
	##formal(LongUdiv, MAIN_WIDTH=16, DENOM_WIDTH=12, CHUNK_WIDTH=3)
	##formal(LongUdiv, MAIN_WIDTH=16, DENOM_WIDTH=10, CHUNK_WIDTH=5)
	##for MAIN_WIDTH in range(1, 16 + 1):
	##	for DENOM_WIDTH in range(1, 16 + 1):
	##		for CHUNK_WIDTH in range(1, 8 + 1):
	##			formal(LongUdiv, MAIN_WIDTH=MAIN_WIDTH,
	##				DENOM_WIDTH=DENOM_WIDTH, CHUNK_WIDTH=CHUNK_WIDTH)
	##formal(LongUdiv, MAIN_WIDTH=7, DENOM_WIDTH=7, CHUNK_WIDTH=2)


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
