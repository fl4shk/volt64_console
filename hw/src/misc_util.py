#!/usr/bin/env python3

import sys
import math

from general.container_types import *

from nmigen import *
from nmigen import *
from nmigen.sim import *

from nmigen.cli import main, main_parser, main_runner
from nmigen_boards.de0_cv import *

from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.back import verilog

#--------
class Blank:
	pass

def psconcat(*args):
	return str().join([str(arg) for arg in args])

def lsconcat(lst):
	return str().join([str(elem) for elem in lst])

def fprintout(file, *args, flush=False):
	print(psconcat(*args), sep="", end="", file=file, flush=flush)

def printout(*args):
	fprintout(sys.stdout, *args)

def printerr(*args):
	fprintout(sys.stderr, *args)

def convert_enum_to_str(to_conv):
	return str(to_conv)[str(to_conv).find(".") + 1:]
#--------
def width_from_arg(arg):
	return math.ceil(math.log2(arg))
def width_from_len(arg):
	return width_from_arg(len(arg))

#def add_unique_memb(self, name, val):
#	if name not in self.__dict__:
#		self.__dict__[name] = val
#	else: # if name in self.__dict__
#		printerr("add_unique_memb():  ")
#		printerr("non-unique member name \"{}\" for \"{}\"" \
#			.format(name, self))

#def add_clk_domain(m, clk, domain="dom"):
#	m.domains += ClockDomain(domain)
#	m.d.comb += ClockSignal(domain=domain).eq(clk)
def to_shape(arg):
	return Value.cast(arg).shape()
#--------
def inst_pll(pll_file_name, domain, pll_module_name, freq, platform, m):
	ret = Blank()
	ret.pll_clk = Signal()
	ret.locked = Signal()

	m.domains += ClockDomain(domain)
	m.d.comb += ClockSignal(domain=domain).eq(ret.pll_clk)

	with open(pll_file_name) as f:
		platform.add_file(pll_file_name, f)

	setattr(m.submodules, domain,
		Instance \
		(
			pll_module_name,

			i_refclk=ClockSignal(domain="sync"),
			i_rst=ResetSignal(domain="sync"),
			o_outclk_0=ret.pll_clk,
			o_locked=ret.locked,
		))

	platform.add_clock_constraint(ret.pll_clk, freq)

	return ret
#--------
class Vec2Layout(Packrec.Layout):
	def __init__(self, ElemKindT, signed=False):
		self.__ElemKindT = ElemKindT
		self.__signed = signed
		super().__init__ \
		(
			[
				("x", self.ElemKindT()),
				("y", self.ElemKindT()),
			],
			signed=signed
		)
	def ElemKindT(self):
		return self.__ElemKindT
	def signed(self):
		return self.__signed
class Vec2(Packrec):
	def __init__(self, ElemKindT, signed):
		super().__init__(Vec2Layout(ElemKindT=ElemKindT))
	def ElemKindT(self):
		return self.layout().ElemKindT()
	def signed(self):
		return self.layout().signed()

class PrevCurrPair:
	def __init__(self, curr=None):
		self.__prev, self.__curr = None, curr

	def prev(self):
		return self.__prev
	def curr(self):
		return self.__curr

	def back_up(self):
		self.__prev = self.curr()

	def back_up_and_update(self, curr):
		self.__prev = self.curr()
		self.__curr = curr
#--------
def sig_keep():
	return {"keep": 1}
#--------
def ports(bus):
	def inner_ports(bus):
		ret = []
		for key in bus.__dict__:
			val = bus.__dict__[key]
			if key[0] != "_":
				if isinstance(val, Signal) or isinstance(val, Record):
					ret += [val]
				elif isinstance(val, Packrec):
					ret += [val.sig()]
				elif isinstance(val, Packarr):
					ret += [val.sig()]
				elif isinstance(val, Splitrec):
					ret += val.flattened()
				else:
					ret += inner_ports(val)
		return ret
	return ([ClockSignal(), ResetSignal()] + inner_ports(bus))

def to_verilog(dut_mod, **kw_args):
	dut = dut_mod(**kw_args)
	# ./main.py generate -t v
	main(dut, ports=ports(dut.bus()))
	#with open("dut.v.ignore", "w") as f:
	#	f.write(verilog.convert(dut, ports=ports(dut.bus())))

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
