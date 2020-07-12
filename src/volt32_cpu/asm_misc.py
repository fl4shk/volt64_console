#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto

class Op(Enum):
	#--------
	# 0 .. 3

	# We already have provisions for doing two adds in one instruction
	# due to the loads and stores, so we might as well make it possible
	# to do so for `add` and `sub` instructions

	# add rA, rB, rC, simm12
	Add = 0

	# sub rA, rB, rC, simm12
	Sub = auto()

	# sltu rA, rB, rC
	Sltu = auto()

	# mulu rA, rB, rC, rD
	# multiply, unsigned full product, high in `rA`, low in `rB`
	Mulu = auto()
	#--------

	#--------
	# 4 .. 7

	# divu rA, rB, rC, rD
	# divmod unsigned, quotient in `rA`, remainder in `rB`
	Divu = auto()

	# and rA, rB, rC
	And = auto()

	# or rA, rB, rC
	Or = auto()

	# xor rA, rB, rC
	Xor = auto()
	#--------

	#--------
	# 8 .. 11

	# lsl rA, rB, rC
	Lsl = auto()

	# lsr rA, rB, rC
	Lsr = auto()

	# asr rA, rB, rC
	Asr = auto()

	# pre simm24
	Pre = auto()
	#--------

	#--------
	# 12 .. 15
	# add rA, pc, simm20
	AddPc = auto()

	# bl rA, simm20
	# Branch and link, jumping to location `rA + to_s32(simm20)`
	Bl = auto()

	# jmp rA, rB, simm16
	# Jump to location `rA + rB + to_s32(simm16)`
	Jmp = auto()

	# bz rA, simm20
	Bz = auto()
	#--------

	#--------
	# 16 .. 19

	# bnz rA, simm20
	Bnz = auto()

	# ldr rA, [rB, rC, simm12]
	Ldr = auto()

	# str rA, [rB, rC, simm12]
	Str = auto()

	# ldh rA, [rB, rC, simm12]
	Ldh = auto()
	#--------

	#--------
	# 20 .. 23

	# ldsh rA, [rB, rC, simm12]
	Ldsh = auto()

	# sth rA, [rB, rC, simm12]
	Sth = auto()

	# ldb rA, [rB, rC, simm12]
	Ldb = auto()

	# ldsb rA, [rB, rC, simm12]
	Ldsb = auto()
	#--------

	#--------
	# 24 .. 27

	# stb rA, [rB, rC, simm12]
	Stb = auto()

	# zeh rA, rB
	Zeh = auto()

	# zeb rA, rB
	Zeb = auto()

	# seh rA, rB
	Seh = auto()
	#--------

	#--------
	# 28 .. 31
	# seb rA, rB
	Seb = auto()

	# ei
	Ei = auto()

	# di
	Di = auto()

	# reti
	Reti = auto()
	#--------

#--------
Zero = 0
Ua = 1
Ub = 2
Uc = 3
#--------

#--------
Ud = 4
Ue = 5
Uf = 6
Ug = 7
#--------

#--------
Uh = 8
Ui = 9
Uj = 10
Uk = 11
#--------

#--------
Ira = 12
Lr = 13
Fp = 14
Sp = 15
#--------

