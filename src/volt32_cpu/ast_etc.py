#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto
import math

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

		Int = auto()
		Float = auto()
		Log2 = auto()

	def __init__(self, op, left, right):
		self.__op, self.__left, self.__right = op, left, right

	Int = lambda left: Ast(op=Ast.Op.Int, left=left, right=None)
	Float = lambda left: Ast(op=Ast.Op.Float, left=left, right=None)
	Log2 = lambda left: Ast(op=Ast.Op.Log2, left=left, right=None)

	def op(self):
		return self.__op
	def left(self):
		return self.__left
	def right(self):
		return self.__right

	def elab(self):
		Op = Ast.Op

		left, right = self.left(), self.right()

		left_sym = False
		if type(left) == Symbol:
			left = left.val()
			left_sym = True
		elif type(left) == Ast:
			left = left.elab()

		if (type(left) != int) and (type(left) != float):
			if not left_sym:
				printerr("Error:  Ast.elab():  ",
					"Invalid type `{}`".format(type(left)),
					" for `left`!\n")
			else: # if left_sym
				printerr("Error:  Ast.elab():  ",
					"Invalid type `{}`".format(type(left)),
					" for `left` symbol called `{}`!\n" \
					.format(self.left().name()))
			exit(1)

		right_sym = False
		if type(right) == Symbol:
			right = right.val()
			right_sym = True
		elif type(right) == Ast:
			right = right.elab()

		if (type(right) != int) and (type(right) != float):
			if not right_sym:
				printerr("Error:  Ast.elab():  ",
					"Invalid type `{}`".format(type(right)),
					" for `right`!\n")
			else: # if right_sym
				printerr("Error:  Ast.elab():  ",
					"Invalid type `{}`".format(type(right)),
					" for `right` symbol called `{}`!\n" \
					.format(self.right().name()))
			exit(1)

		ret = None

		if self.op() == Op.Plus:
			ret = left + right
		elif self.op() == Op.Minus:
			ret = left - right

		elif self.op() == Op.Mul:
			ret = left * right
		elif self.op() == Op.Div:
			ret = left // right
		elif self.op() == Op.Mod:
			ret = left % right

		elif self.op() == Op.Pow:
			ret = left ** right

		elif self.op() == Op.Lshift:
			if (type(left) == int) and (type(right) == int):
				ret = left << right
			else:
				printerr("Error:  Ast.elab():  left shift of type `{}` " \
					.format(type(left)),
					"by type `{}`!\n".format(type(right)))
				exit(1)
		elif self.op() == Op.Rshift:
			if (type(left) == int) and (type(right) == int):
				ret = left >> right
			else:
				printerr("Error:  Ast.elab():  right shift of type `{}` " \
					.format(type(left)),
					"by type `{}`!\n".format(type(right)))
				exit(1)

		elif self.op() == Op.Bitand:
			if (type(left) == int) and (type(right) == int):
				ret = left & right
			else:
				printerr("Error:  Ast.elab():  bitwise AND of type `{}` " \
					.format(type(left)),
					"by type `{}`!\n".format(type(right)))
				exit(1)
		elif self.op() == Op.Bitor:
			if (type(left) == int) and (type(right) == int):
				ret = left | right
			else:
				printerr("Error:  Ast.elab():  bitwise OR of type `{}` " \
					.format(type(left)),
					"by type `{}`!\n".format(type(right)))
				exit(1)
		elif self.op() == Op.Bitxor:
			if (type(left) == int) and (type(right) == int):
				ret = left ^ right
			else:
				printerr("Error:  Ast.elab():  bitwise XOR of type `{}` " \
					.format(type(left)),
					"by type `{}`!\n".format(type(right)))
				exit(1)
		elif self.op() == Op.Bitnot:
			if type(left) == int:
				ret = ~left
			else:
				printerr("Error:  Ast.elab():  bitwise NOT of type `{}`" \
					.format(type(left)),
					"!\n")
				exit(1)

		elif self.op() == Op.Cmpeq:
			ret = 1 if left == right else 0
		elif self.op() == Op.Cmpne:
			ret = 1 if left != right else 0
		elif self.op() == Op.Cmplt:
			ret = 1 if left < right else 0
		elif self.op() == Op.Cmpgt:
			ret = 1 if left > right else 0
		elif self.op() == Op.Cmple:
			ret = 1 if left <= right else 0
		elif self.op() == Op.Cmpge:
			ret = 1 if left >= right else 0

		elif self.op() == Op.Int:
			ret = int(left)
		elif self.op() == Op.Float:
			ret = float(left)
		elif self.op == Op.Log2:
			ret = math.log2(left)

		else:
			printerr("Error:  Ast.elab():  Invalid opcode `{}`!\n" \
				.format(self.op()))
			exit(1)

		return ret
#--------



#--------
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
#--------

#--------
class Instr:
	def __init__(self, op=None, ra=None, rb=None, rc=None, rd=None,
		simm=None):
		self.__op = op
		self.__ra = ra
		self.__rb = rb
		self.__rc = rc
		self.__rd = rd
		self.__simm = simm

		#assert (self.__op != Op.Pre)

	#--------
	def op(self):
		return self.__op
	def ra(self):
		return self.__ra
	def rb(self):
		return self.__rb
	def rc(self):
		return self.__rc
	def rd(self):
		return self.__rd
	def simm(self):
		return self.__simm
	#--------

	#--------
	def HAS(self):
		return \
		{
			Op.Add: {"regs": {"rA", "rB", "rC"}},
			Op.Sub: {"regs": {"rA", "rB", "rC"}},
			Op.Addsi: {"regs": {"rA", "rB"}, "simm": 16},
			Op.Sltu: {"regs": {"rA", "rB", "rC"}},

			Op.Slts: {"regs": {"rA", "rB", "rC"}},
			Op.Mulu: {"regs": {"rA", "rB", "rC", "rD"}},
			Op.Muls: {"regs": {"rA", "rB", "rC", "rD"}},
			Op.Divu: {"regs": {"rA", "rB", "rC", "rD"}},

			Op.Divs: {"regs": {"rA", "rB", "rC", "rD"}},
			Op.And: {"regs", {"rA", "rB", "rC"}},
			Op.Or: {"regs", {"rA", "rB", "rC"}},
			Op.Xor: {"regs", {"rA", "rB", "rC"}},

			Op.Lsl: {"regs", {"rA", "rB", "rC"}},
			Op.Lsr: {"regs", {"rA", "rB", "rC"}},
			Op.Asr: {"regs", {"rA", "rB", "rC"}},
			Op.Pre: {"simm": 24},

			Op.AddsiPc: {"regs": {"rA"}, "simm": 20},
			Op.Jl: {"regs": {"rA"}, "simm": 20},
			Op.Jmp: {"regs": {"rA"}, "simm": 20},
			Op.Bz: {"regs": {"rA"}, "simm": 20}

			Op.Bnz: {"regs": {"rA"}, "simm": 20}
			Op.Ld: {"regs": {"rA", "rB"}, "simm": 16}
			Op.St: {"regs": {"rA", "rB"}, "simm": 16}
			Op.Ldh: {"regs": {"rA", "rB"}, "simm": 16}

			Op.Ldsh: {"regs": {"rA", "rB"}, "simm": 16}
			Op.Sth: {"regs": {"rA", "rB"}, "simm": 16}
			Op.Ldb: {"regs": {"rA", "rB"}, "simm": 16}
			Op.Ldsb: {"regs": {"rA", "rB"}, "simm": 16}

			Op.Stb: {"regs": {"rA", "rB"}, "simm": 16}
			Op.Zeh: {"regs": {"rA", "rB"}}
			Op.Zeb: {"regs": {"rA", "rB"}}
			Op.Seh: {"regs": {"rA", "rB"}}

			Op.Seb: {"regs": {"rA", "rB"}}
			Op.Ei: {},
			Op.Di: {},
			Op.Reti: {},
		}
	#--------

	#--------
	def expand(self, sym_tbl) -> list:
		#--------
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
		#--------

		#--------
		ret \
		= {
			"warn": "",
			"lst": []
		}
		#--------

		#--------
		HAS = self.HAS()
		op = self.op()
		ra = self.ra()
		rb = self.rb()
		rc = self.rc()
		rd = self.rd()
		simm = self.simm()

		if op in HAS:
			if "regs" in HAS[op]:
				if "rA" in HAS[op]["regs"]:
					assert type(ra) == int
				if "rB" in HAS[op]["regs"]:
					assert type(rb) == int
				if "rC" in HAS[op]["regs"]:
					assert type(rc) == int
				if "rD" in HAS[op]["regs"]:
					assert type(rd) == int
			if "simm" in HAS[op]:
				assert (type(simm) == Ast) or (type(simm) == Symbol) \
					or (type(simm) == str) or (type(simm) == int) \
					or (type(simm) == float)

		else: # if op not in HAS:
			printerr("Error:  Volt32CpuAssembler.Instr.enc():  ",
				"Invalid instruction with opcode {}.\n"
				.format(hex(int(op))))
			exit(1)
		#--------

		#--------
		return ret
		#--------
	#--------
#--------


#--------
def Add(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Add, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Sub(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Sub, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Addsi(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Addsi, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Sltu(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Sltu, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}

def Slts(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Slts, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Mulu(ra, rb, rc, rd):
	return \
	{
		"instr": [Instr(op=Op.Mulu, ra=ra, rb=rb, rc=rc, rd=rd)],
		"enc": [],
	}
def Muls(ra, rb, rc, rd):
	return \
	{
		"instr": [Instr(op=Op.Muls, ra=ra, rb=rb, rc=rc, rd=rd)],
		"enc": [],
	}
def Divu(ra, rb, rc, rd):
	return \
	{
		"instr": [Instr(op=Op.Divu, ra=ra, rb=rb, rc=rc, rd=rd)],
		"enc": [],
	}

def Divs(ra, rb, rc, rd):
	return \
	{
		"instr": [Instr(op=Op.Divs, ra=ra, rb=rb, rc=rc, rd=rd)],
		"enc": [],
	}
def And(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.And, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Or(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Or, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Xor(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Xor, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}

def Lsl(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Lsl, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Lsr(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Lsr, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}
def Asr(ra, rb, rc):
	return \
	{
		"instr": [Instr(op=Op.Asr, ra=ra, rb=rb, rc=rc)],
		"enc": [],
	}

def AddsiPc(ra, simm):
	return \
	{
		"instr": [Instr(op=Op.AddsiPc, ra=ra, simm=simm)],
		"enc": [],
	}
def Jl(ra, simm):
	return \
	{
		"instr": [Instr(op=Op.Jl, ra=ra, simm=simm)],
		"enc": [],
	}
def Jmp(ra, simm):
	return \
	{
		"instr": [Instr(op=Op.Jmp, ra=ra, simm=simm)],
		"enc": [],
	}
def Bz(ra, simm):
	return \
	{
		"instr": [Instr(op=Op.Bz, ra=ra, simm=simm)],
		"enc": [],
	}

def Bnz(ra, simm):
	return \
	{
		"instr": [Instr(op=Op.Bnz, ra=ra, simm=simm)],
		"enc": [],
	}
def Ld(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Ld, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def St(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.St, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Ldh(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Ldh, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}

def Ldsh(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Ldsh, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Sth(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Sth, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Ldb(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Ldb, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Ldsb(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Ldsb, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}

def Stb(ra, rb, simm):
	return \
	{
		"instr": [Instr(op=Op.Stb, ra=ra, rb=rb, simm=simm)],
		"enc": [],
	}
def Zeh(ra, rb):
	return \
	{
		"instr": [Instr(op=Op.Zeh, ra=ra, rb=rb)],
		"enc": [],
	}
def Zeb(ra, rb):
	return \
	{
		"instr": [Instr(op=Op.Zeb, ra=ra, rb=rb)],
		"enc": [],
	}
def Seh(ra, rb):
	return \
	{
		"instr": [Instr(op=Op.Seh, ra=ra, rb=rb)],
		"enc": [],
	}

def Seb(ra, rb):
	return \
	{
		"instr": [Instr(op=Op.Seb, ra=ra, rb=rb)],
		"enc": [],
	}
def Ei():
	return \
	{
		"instr": [Instr(op=Op.Ei)],
		"enc": [],
	}
def Di():
	return \
	{
		"instr": [Instr(op=Op.Di)],
		"enc": [],
	}
def Reti():
	return \
	{
		"instr": [Instr(op=Op.Reti)],
		"enc": [],
	}
#--------

#--------
# Scope begin
class ScopeBegin:
	pass

# Scope end
class ScopeEnd:
	pass

# Label
class L:
	def __init__(self, name: str):
		self.__name = name
	def name(self) -> str:
		return self.__name

# Set the current program counter
class Org:
	def __init__(self, addr: int):
		self.__addr = addr
	def addr(self):
		return self.__addr

# Align code/data
class Align:
	def __init__(self, amount: int):
		self.__amount = amount
	def amount(self):
		return self.__amount

# Literal byte
class Lbyte:
	def __init__(self, lst: list):
		self.__lst = lst
	def lst(self):
		return self.__lst
	def __len__(self):
		return len(self.lst())

# Literal half word
class Lhword(Lbyte):
	def __init__(self, lst: list):
		super().__init__(lst=lst)
	def __len__(self):
		return (len(self.lst()) * 2)

# Literal word
class Lword(Lbyte):
	def __init__(self, lst: list):
		super().__init__(lst=lst)
	def __len__(self):
		return (len(self.lst()) * 4)
#--------

#--------
# Stack frame info
class FrameInfo:
	#--------
	def __init__(self, reg_set=None, var_dict=None, REG_SIZE=4,
		NUM_REGS=NumRegs):
		# TODO:  Add in support for constructor and destructor calling
		self.__reg_set = reg_set
		self.__var_dict = var_dict,
		self.__REG_SIZE = REG_SIZE
		self.__NUM_REGS = NUM_REGS

		self.__REG_ALLOC_SIZE = 0
		self.__VAR_ALLOC_SIZE = 0

		reg_set = self.reg_set()
		var_dict = self.var_dict()

		self.__reg_save_list = []
		if reg_set != None:
			assert type(reg_set) == set

			NUM_SAVED_REGS = len(reg_set)
			assert NUM_SAVED_REGS < NUM_REGS
			regs_list = list(reg_set)

			self.__REG_ALLOC_SIZE = NUM_SAVED_REGS * self.REG_SIZE()

			for i in range(NUM_SAVED_REGS):
				reg = regs_list[i]
				assert reg < self.NUM_REGS()

				self.__reg_save_list \
					+= [{
						"reg": regs_list[i],
						"offset": -(self.REG_BASE()
							+ (i * self.REG_SIZE())),
					}]
				#reg_save = self.__reg_save_list[-1]
				#reg_save["ld"] = Ld(reg_save["reg"], Fp,
				#	-(self.REG_BASE() + reg_save["index"]))
				#reg_save["st"] = St(reg_save["reg"], Fp,
				#	-(self.REG_BASE() + reg_save["index"]))

		if var_dict != None:
			assert type(var_dict) == dict
			self.__VAR_ALLOC_SIZE = sum([var_dict[name]["size"]
				for name in var_dict])

			offset = 0
			for name in var_dict:
				var = self.var_dict()[name]
				assert "offset" not in var
				var["offset"] = offset
				offset += var["size"]

		self.__INITIAL_ALLOC_SIZE = self.REG_ALLOC_SIZE() \
			+ self.VAR_ALLOC_SIZE()

		#self.__stack_alloc_instr \
		#	= Addsi(Sp, Sp, -self.INITIAL_ALLOC_SIZE())
		#self.__stack_dealloc_instr \
		#	= Addsi(Sp, Sp, self.INITIAL_ALLOC_SIZE())
	#--------

	#--------
	# Saved parameters
	def reg_set(self):
		return self.__reg_set
	def var_dict(self):
		return self.__var_dict
	def REG_SIZE(self):
		return self.__REG_SIZE
	def NUM_REGS(self):
		return self.__NUM_REGS
	#--------

	#--------
	# Other Members
	def reg_save_list(self):
		return self.__reg_save_list
	#def stack_alloc_instr(self):
	#	return self.__stack_alloc_instr
	#def stack_dealloc_instr(self):
	#	return self.__stack_dealloc_instr
	#--------

	#--------
	# Sizes of storage
	def REG_ALLOC_SIZE(self):
		return self.__REG_ALLOC_SIZE
	def VAR_ALLOC_SIZE(self):
		return self.__VAR_ALLOC_SIZE
	def INITIAL_ALLOC_SIZE(self):
		return self.__INITIAL_ALLOC_SIZE
	#--------

	#--------
	# Offsets from frame pointer to specific things in the frame

	# The start of storage for saved registers
	def REG_BASE(self):
		return 0

	# The start of storage for local variables
	def VAR_BASE(self):
		return self.REG_BASE() + self.REG_ALLOC_SIZE()

	# The initial stack pointer of the scope
	def STACK_BASE(self):
		return self.VAR_BASE() + self.VAR_ALLOC_SIZE()
	#--------

class ScopeGen:
	def __init__(self, lst):
		self.__lst = lst

	class ScopeCtxMgr:
		def __init__(self, parent, frame_info=None):
			self.__parent = parent
			self.__frame_info = frame_info

			fi = self.__frame_info

			if fi != None:
				assert type(fi) == FrameInfo

		def __enter__(self):
			lst = self.__parent.lst()
			lst += [ScopeBegin()]

			fi = self.__frame_info

			if fi != None:
				if fi.INITIAL_ALLOC_SIZE() != 0:
					lst += [Addsi(Sp, Sp, -fi.INITIAL_ALLOC_SIZE())]
				for reg_save in fi.reg_save_list():
					lst += [St(reg_save["reg"], Fp, reg_save["offset"])]

		def __exit__(self, exc_type, exc_val, exc_tb):
			lst = self.__parent.lst()

			fi = self.__frame_info

			if fi != None:
				for reg_save in fi.reg_save_list():
					lst += [Ld(reg_save["reg"], Fp, reg_save["offset"])]
				if fi.INITIAL_ALLOC_SIZE() != 0:
					#lst += [fi.INITIAL_ALLOC_SIZE()]
					lst += [Add(Sp, Zero, Fp)]

			lst += [ScopeEnd()]

	def lst(self):
		return self.__lst
	def scope(self, frame_info=None):
		return ScopeCtxMgr(parent=self, frame_info=frame_info)
#--------

#--------
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

def scope(frame_info=None):
	return prog_data.scope_gen().scope(frame_info=frame_info)
#--------
