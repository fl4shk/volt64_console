#!/usr/bin/env python3

import sys
import math

from nmigen import *
from nmigen.hdl.rec import *

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
def to_shape(RecOrArrayT):
	return Value.cast(RecOrArrayT).shape()
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
class Vec2Layout(Layout):
	def __init__(self, ShapeT):
		self.__ShapeT = ShapeT
		super().__init__ \
		([
			("x", self.ShapeT()),
			("y", self.ShapeT()),
		])
	def ShapeT(self):
		return self.__ShapeT
class Vec2(Record):
	def __init__(self, ShapeT):
		super().__init__(Vec2Layout(ShapeT=ShapeT))
	def ShapeT(self):
		return self.layout.ShapeT()

class PrevCurrPair:
	def __init__(self, curr=None):
		self.__prev, self.__curr = None, curr

	def prev(self):
		return self.__prev
	def curr(self):
		return self.__curr

	def update(self, curr):
		self.__prev = self.curr()
		self.__curr = curr
#--------
##class PackedArray(ValueCastable):
#class PackedArray:
#	#--------
#	def __init__(self, ShapeT, SIZE):
#		self.__ShapeT, self.__SIZE = ShapeT, SIZE
#
#		self.__data = Signal(self.ShapeT().width * self.SIZE())
#	#--------
#	def ShapeT(self):
#		return self.__ShapeT
#	def SIZE(self):
#		return self.__SIZE
#
#	def data(self):
#		return self.__data
#	#--------
#	def __getitem__(self, key):
#		return self.data().word_select(key, self.ShapeT().width)
#	#--------
#--------

#--------
def sig_keep():
	return {"keep": 1}
#--------
