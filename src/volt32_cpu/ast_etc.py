#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto

from volt32_cpu.asm_misc import *

class Ast:
	class Op(Enum):
		Plus = auto()
		Minus = auto()

		Mul = auto()
		Div = auto()
		Mod = auto()

		Pow = auto()

		Lshift = auto()
		Rshift = auto()

		Bitand = auto()
		Bitor = auto()
		Bitxor = auto()
		Bitnot = auto()

		Cmpeq = auto()
		Cmpne = auto()
		Cmplt = auto()
		Cmpgt = auto()
		Cmple = auto()
		Cmpge = auto()

		Unsigned = auto()
		Signed = auto()

	def __init__(self, op, left, right):
		self.__op, self.__left, self.__right = op, left, right

	def op(self):
		return self.__op
	def left(self):
		return self.__left
	def right(self):
		return self.__right

	def elab(self):

	Unsigned = lambda left: Ast(op=Ast.Op.Unsigned, left=left, right=None)
	Signed = lambda left: Ast(op=Ast.Op.Signed, left=left, right=None)

class UseAst:
	#--------
	def __init__(self):
		pass
	#--------

	#--------
	def __add__(self, other):
		return Ast(Ast.Op.Plus, self, other)
	def __radd__(self, other):
		return Ast(Ast.Op.Plus, other, self)

	def __sub__(self, other):
		return Ast(Ast.Op.Minus, self, other)
	def __rsub__(self, other):
		return Ast(Ast.Op.Minus, other, self)
	#--------

	#--------
	def __mul__(self, other):
		return Ast(Ast.Op.Mul, self, other)
	def __rmul__(self, other):
		return Ast(Ast.Op.Mul, other, self)

	def __floordiv__(self, other):
		return Ast(Ast.Op.Div, self, other)
	def __rfloordiv__(self, other):
		return Ast(Ast.Op.Div, other, self)

	def __mod__(self, other):
		return Ast(Ast.Op.Mod, self, other)
	def __rmod__(self, other):
		return Ast(Ast.Op.Mod, other, self)

	def __pow__(self, other):
		return Ast(Ast.Op.Pow, self, other)
	def __rpow__(self, other):
		return Ast(Ast.Op.Pow, other, self)
	#--------

	#--------
	def __lshift__(self, other):
		return Ast(Ast.Op.Lshift, self, other)
	def __rlshift__(self, other):
		return Ast(Ast.Op.Lshift, other, self)

	def __rshift__(self, other):
		return Ast(Ast.Op.Rshift, self, other)
	def __rrshift__(self, other):
		return Ast(Ast.Op.Rshift, other, self)
	#--------

	#--------
	def __and__(self, other):
		return Ast(Ast.Op.Bitand, self, other)
	def __rand__(self, other):
		return Ast(Ast.Op.Bitand, other, self)

	def __or__(self, other):
		return Ast(Ast.Op.Bitor, self, other)
	def __ror__(self, other):
		return Ast(Ast.Op.Bitor, other, self)

	def __xor__(self, other):
		return Ast(Ast.Op.Bitxor, self, other)
	def __rxor__(self, other):
		return Ast(Ast.Op.Bitxor, other, self)

	def __invert__(self, other):
		return Ast(Ast.Op.Bitnot, self, other)
	def __rinvert__(self, other):
		return Ast(Ast.Op.Bitnot, other, self)
	#--------

	#--------
	def __eq__(self, other):
		return Ast(Ast.Op.Cmpeq, self, other)
	def __req__(self, other):
		return Ast(Ast.Op.Cmpeq, other, self)

	def __ne__(self, other):
		return Ast(Ast.Op.Cmpne, self, other)
	def __rne__(self, other):
		return Ast(Ast.Op.Cmpne, other, self)

	def __lt__(self, other):
		return Ast(Ast.Op.Cmplt, self, other)
	def __rlt__(self, other):
		return Ast(Ast.Op.Cmplt, other, self)

	def __gt__(self, other):
		return Ast(Ast.Op.Cmpgt, self, other)
	def __rgt__(self, other):
		return Ast(Ast.Op.Cmpgt, other, self)

	def __le__(self, other):
		return Ast(Ast.Op.Cmple, self, other)
	def __rle__(self, other):
		return Ast(Ast.Op.Cmple, other, self)

	def __ge__(self, other):
		return Ast(Ast.Op.Cmpge, self, other)
	def __rge__(self, other):
		return Ast(Ast.Op.Cmpge, other, self)
	#--------

class Symbol(UseAst):
	def __init__(self, parent, name, val, found):
		self.__parent = parent
		self.__name = name
		self.__val = val
		self.__found = found

	def parent(self):
		return self.__parent
	def name(self):
		return self.__name

	def val(self):
		return self.__val
	def set_val(self, val):
		self.__val = val

	def found(self):
		return self.__found
	def set_found(self, found):
		self.__found = found


class SymbolTable:
	def __init__(self, parent=None):
		self.__parent = parent
		self.__table = dict()
		self.__children = []

	def parent(self):
		return self.__parent
	def children(self):
		return self.__children

	def find(self, name):
		if name in self.__table:
			return self.__table[name]
		elif self.parent() != None:
			return self.parent().find(name)
		else:
			return None

	def shadows(self, name):
		ret = self.parent().find(name) \
			if self.parent() != None \
			else None
		if (name in self.__table) and ret != None:
			return \
			{
				"parent": ret,
				"current": self.__table,
			}
		else:
			return None

	def insert(self, name, val, found=False):
		if name not in self.__table:
			return None
		else: # if not self.contains(name)
			ret = Symbol \
				(
					parent=self,
					name=name,
					val=val,
					found=found
				)
			self.__table[name] = ret
			return ret


	#def mk_child(self):
	#	self.__children.append(SymbolTable(parent=self))

class Instr:
	def __init__(self, op=Op.Add, ra=0, rb=0, rc=0, rd=0, simm=0):
		self.__op = op
		self.__ra = ra
		self.__rb = rb
		self.__rc = rc
		self.__rd = rd
		self.__simm = simm

		#assert (self.__op != Op.Pre)

	def enc(self) -> list:
		def enc_simm(simm: int, SIMM_WIDTH: int) -> Blank:
			ret = Blank()

			def itol(x: int, MIN_WIDTH: int) -> list:
				bit_str = bin(abs(x))[2:][::-1]
				if x < 0:
					XOR_VAL = (1 << max(len(bit_str), MIN_WIDTH)) - 1
					bit_str = bin((abs(x) ^ XOR_VAL) + 1)[2:][::-1]
				else: # if x >= 0:
					while len(bit_str) < MIN_WIDTH:
						bit_str += "0"
				return [int(bit) for bit in bit_str]

			def ltoui(x: list) -> int:
				bit_str = "0b" + "".join([str(bit) for bit in x[::-1]])
				return int(bit_str, 2)
			def ltoi(x: list) -> list:
				ret = ltoui(x)

				# if x is negative
				if x[-1] == 1:
					XOR_VAL = (1 << len(x)) - 1
					ret = -((ret ^ XOR_VAL) + 1)
				return ret

			TOP_WIDTH = 3
			SIMM_MAX_WIDTH = 8

			simm_list = itol(simm, SIMM_MAX_WIDTH)
			ret.wont_fit = len(simm_list) > (SIMM_MAX_WIDTH - 1)

			ret.bot_list = simm_list[:SIMM_WIDTH]
			ret.top_list = simm_list[SIMM_WIDTH:]

			ret.bot = ltoui(ret.bot_list)
			ret.top = ltoui(ret.top_list)

			ret.dbg = ltoi(ret.bot_list + ret.top_list)

			return ret

		ret = []

		HAS \
		= {
			Op.Add: {"regs": {"rA", "rB", "rC"}, "simm": 12},
			Op.Sub: {"regs": {"rA", "rB", "rC"}, "simm": 12},
			Op.Sltu: {"regs": {"rA", "rB", "rC"}},
			Op.Mulu: {"regs": {"rA", "rB", "rC", "rD"}},

			Op.Divu: {"regs": {"rA", "rB", "rC", "rD"}},
			Op.And: {"regs", {"rA", "rB", "rC"}},
			Op.Or: {"regs", {"rA", "rB", "rC"}},
			Op.Xor: {"regs", {"rA", "rB", "rC"}},

			Op.Lsl: {"regs", {"rA", "rB", "rC"}},
			Op.Lsr: {"regs", {"rA", "rB", "rC"}},
			Op.Asr: {"regs", {"rA", "rB", "rC"}},
			Op.Pre: {"simm": 24},

			Op.AddPc: {"regs": {"rA"}, "simm": 20},
			Op.Bl: {"regs": {"rA"}, "simm": 20},
			Op.Jmp: {"regs": {"rA", "rB"}, "simm": 16},
			Op.Bz: {"regs": {"rA"}, "simm": 20}

			Op.Bnz: {"regs": {"rA"}, "simm": 20}
			Op.Ldr: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Str: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Ldh: {"regs": {"rA", "rB", "rC"}, "simm": 12}

			Op.Ldsh: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Sth: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Ldb: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Ldsb: {"regs": {"rA", "rB", "rC"}, "simm": 12}

			Op.Stb: {"regs": {"rA", "rB", "rC"}, "simm": 12}
			Op.Zeh: {"regs": {"rA", "rB"}}
			Op.Zeb: {"regs": {"rA", "rB"}}
			Op.Seh: {"regs": {"rA", "rB"}}

			Op.Seb: {"regs": {"rA", "rB"}}
			Op.Ei: set(),
			Op.Di: set(),
			Op.Reti: set(),
		}

		if op not in HAS:
			printerr("Error:  Volt32CpuAssembler.Instr.enc():  ",
				"Invalid instruction with opcode {}.\n"
				.format(hex(int(op))))
			exit(1)

		return ret

class Begin:
	pass
class End:
	pass
class L:
	def __init__(self, name):
		self.__name = name
	def name(self):
		return self.__name

class ScopeGen:
	def __init__(self, lst: SymbolTable):
		self.__lst = lst

	class ScopeCtxMgr:
		def __init__(self, parent: ScopeGen):
			self.__parent = parent

		def __enter__(self):
			#self.__parent.tbl = SymbolTable(parent=self.tbl())
			#self.tbl().children().append(self.tbl())
			self.__parent.lst().append(Begin())

		def __exit__(self, exc_type, exc_val, exc_tb):
			#self.__parent.tbl = self.tbl().parent()
			self.__parent.lst().append(End())

	def lst(self):
		return self.__lst
	def scope(self):
		return ScopeCtxMgr(parent=self)


class ProgData:
	def __init__(self):
		self.__sym_tbl = SymbolTable()
		self.__lst = []
		self.__scope_gen = ScopeGen(lst=self.lst())
	def sym_tbl(self):
		return self.__sym_tbl
	def lst(self):
		return self.__lst
	def scope_gen(self):
		return self.__scope_gen

prog_data = ProgData()

def scope():
	return prog_data.scope_gen().scope()

