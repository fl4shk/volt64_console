#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto

class Volt32EncGrp(Enum):
	#--------
	# 0 .. 3

	# Encoding:  0000 aaaa aabb bbbb  cccc ccii iiij jjjj
	# * a:  `dA`
	# * b:  `iB`
	# * c:  `iC`
	# * i:  `imm5b`.  5-bit immediate indicating which instruction in `iB`
	# to jump to
	# * j:  `imm5c`.  5-bit immediate indicating which instruction in `iC`
	# to jump to

	# Instruction:  jmp.s dA, iB, iC, imm5b, imm5c
	# * This instruction jumps to iB (index given by imm5b) if `dA`'s
	# scalar data is non-zero, else to iC (index given by imm5c)
	Grp0 = 0

	# Encoding:  0001 aaaa aabb bbbb  cccc ccii iiij jjjj
	# * a:  `dA`
	# * b:  `iB`
	# * c:  `iC`
	# * i:  `imm5b`.  5-bit immediate indicating which instruction in `iB`
	# to jump to
	# * j:  `imm5c`.  5-bit immediate indicating which instruction in `iC`
	# to jump to

	# Instruction:  jmp.v dA, iB, iC, imm5b, imm5c
	# * This instruction jumps to iB (index given by imm5b) if `dA`'s
	# entire vector data is non-zero, else to iC (index given by imm5c)
	Grp1 = auto()

	# Encoding:  0010 aaaa aabb bbbb  cccc ccoo oov0 0000
	# * a:  `dA`
	# * b:  `dB`
	# * c:  `dC`
	# * o:  opcode
	# * v:  1 if vector op, 0 if scalar op
	Grp2 = auto()

	# Encoding:  0011 aaaa aajj jbbb  cccc ccii iiii iiii
	# * a:  `iA`.  The first destination ILAR
	# * j:  `imm3`.  The number of consecutive destination ILARs to `fetch`
	# into.
	# * b:  `dB`.  Only allows for the low 8 DLARs to be selected.
	# `dB.scalar_data` is used by this instruction. 
	# * c:  `iC`.  `iC.address` is used by this instruction.
	# * i:  `simm10`.  Signed, 13-bit immediate

	# Instruction:  fetch iA, imm3, dB, iC, simm10
	Grp3 = auto()
	#--------

	#--------
	# 4 .. 7

	# Encoding:  0100 aaaa aabb bbbb  oooo iiii iiii iiii
	# * a:  `dA`
	# * b:  `dB`, used as `dB.scalar_data`
	# * o:  `opcode`
	# * i:  `simm12`
	Grp4 = auto()

	# Encoding:  0101 aaaa aabb bbbb  oooo iiii ii00 0000
	# * a:  `dA`.  Supervisor-mode base DLAR.
	# * b:  `dB` or `iB`.  User-mode base DLAR or ILAR.
	# * o:  opcode
	# * i:  `imm6`.  Unsigned 6-bit immediate indicating the number of
	# consecutive user-mode LARs after the base.
	Grp5 = auto()

	# Encoding:  0110 aaaa aabb bbbb  cccc ccoo oov00 0000
	# * a:  `dA`
	# * b:  `dB`
	# * c:  `dC`
	# * o:  opcode
	# * v:  1 if vector op, 0 if scalar op
	Grp6 = auto()
	#--------

# Group 2 Instructions
class Volt32Eg2Op(Enum):
	#--------
	# 0 .. 3

	# add dA, dB, dC
	Add = 0

	# sub dA, dB, dC
	Sub = auto()

	# slt dA, dB, dC
	Slt = auto()

	# mul dA, dB, dC
	Mul = auto()
	#--------

	#--------
	# 4 .. 7

	# umull dA, dB, dC
	# Unsigned full product
	# This instruction forcibly treats `dA` as 64-bit, `dB` as 32-bit, and
	# `dC` as 32-bit.
	Umull = auto()

	# smull dA, dB, dC
	# Signed full product
	# This instruction forcibly treats `dA` as 64-bit, `dB` as 32-bit, and
	# `dC` as 32-bit.
	Smull = auto()

	# udiv dA, dB, dC
	Udiv = auto()

	# sdiv dA, dB, dC
	Sdiv = auto()
	#--------

	#--------
	# 8 .. 11

	# udivl dA, dB, dC
	# This instruction forcibly treats `dA` as 64-bit, `dB` as 64-bit, and
	# `dC` as 32-bit
	Udivl = auto()

	# sdivl dA, dB, dC
	# This instruction forcibly treats `dA` as 64-bit, `dB` as 64-bit, and
	# `dC` as 32-bit
	Sdivl = auto()

	# and dA, dB, dC
	And = auto()

	# or dA, dB, dC
	Or = auto()
	#--------

	#--------
	# 12 .. 15
	# xor dA, dB, dC
	Xor = auto()

	# nand dA, dB, dC
	Nand = auto()

	# shl dA, dB, dC
	# Left shift
	Shl = auto()

	# shr dA, dB, dC
	# Right shift
	# Logical right shift when `dA` is unsigned
	# Arithmetic right shift when `dA` is signed
	Shr = auto()
	#--------

# Group 4 Instructions
class Volt32Eg4Op(Enum):
	#--------
	# 0 .. 3

	# ldu8 dA, dB, simm12 
	Ldu8 = 0

	# lds8 dA, dB, simm12
	Lds8 = auto()

	# ldu16 dA, dB, simm12
	Ldu16 = auto()

	# lds16 dA, dB, simm12
	Lds16 = auto()
	#--------

	#--------
	# 4 .. 7

	# ldu32 dA, dB, simm12 
	Ldu32 = auto()

	# lds32 dA, dB, simm12
	Lds32 = auto()

	# stu8 dA, dB, simm12 
	Stu8 = auto()

	# sts8 dA, dB, simm12
	Sts8 = auto()
	#--------

	#--------
	# 8 .. 11

	# stu16 dA, dB, simm12
	Stu16 = auto()

	# sts16 dA, dB, simm12
	Sts16 = auto()

	# stu32 dA, dB, simm12 
	Stu32 = auto()

	# sts32 dA, dB, simm12
	Sts32 = auto()
	#--------

# Group 5 Instructions
class Volt32Eg5Op(Enum):
	#--------
	# 0 .. 3

	# guda dA, dB, imm6
	# Get user-mode DLAR addresses.  Stores user-mode DLAR addresses
	# (starting with user-mode DLAR `dB`) in each vector data element of
	# supervisor-mode DLAR `dA` and the necessary amount of `dA`-following
	# consecutive supervisor-mode DLARs.  Useful for implementing task
	# switching.
	# This instruction is a NOP if performed in user-mode. 
	Guda = 0

	# suda dA, dB, imm6
	# Set user-mode DLAR addresses.  Acts similarly to the `guda`
	# instruction in terms of which supervisor-mode DLAR vector elements
	# are used and which user-mode DLARs are written to.
	# This instruction is a NOP if performed in user-mode. 
	Suda = auto()

	# gudt dA, dB, imm6
	# Get user-mode DLAR type tags.  Acts similarly to the `guda`
	# instruction in terms of which supervisor-mode DLAR vector elements
	# are used and which user-mode DLARs are written to.
	# This instruction is a NOP if performed in user-mode. 
	Gudt = auto()

	# sudt dA, dB, imm6
	# Set user-mode DLAR type tags.  Acts similarly to the `guda`
	# instruction in terms of which supervisor-mode DLAR vector elements
	# are used and which user-mode DLARs are written to.
	# This instruction is a NOP if performed in user-mode. 
	Sudt = auto()
	#--------

	#--------
	# 4 .. 7
	# guia dA, iB, imm6
	# Get user-mode ILAR addresses.  Acts similarly to the `guda`
	# instruction in terms of which supervisor-mode DLAR vector elements
	# are used.  User-mode ILARs that are used by this instruction are
	# selected via an identical process to how user-mode DLARs are selected
	# by the `guda` instruction.
	# This instruction is a NOP if performed in user-mode. 
	Guia = auto()

	# suia dA, iB, imm6
	# Set user-mode ILAR addresses.  Acts similarly to the `guda`
	# instruction in terms of which supervisor-mode DLAR vector elements
	# are used.  User-mode ILARs that are used by this instruction are
	# selected via an identical process to how user-mode DLARs are selected
	# by the `guda` instruction.
	# This instruction is a NOP if performed in user-mode. 
	Suia = auto()

	# gupc dA
	# Get user-mode PC.  Grabs the user-mode program counter in the form of
	# concat(pc.ilar_num, pc.scalar_offset) and stores it in
	# supervisor-mode DLAR `dA`'s scalar data.
	Gupc = auto()

	# supc dA
	# Set user-mode PC.  Restores the user-mode program counter from the
	# supervisor-mode DLAR `dA`'s scalar data.
	Supc = auto()
	#--------

	#--------
	# 8 .. 11

	# ei
	# Enable interrupts.
	Ei = auto()

	# di
	# Disable interrupts.
	Di = auto()

	# reti
	# Return from an interrupt, switching from supervisor-mode to user-mode
	# and enabling interrupts in the process.
	Reti = auto()
	#--------

# Group 6 Instructions
class Volt32Eg6Op(Enum):
	#--------
	# 0 .. 3

	# inu8.s dA, dB
	# inu8.v dA, dB
	# Read 8-bit data from IO port indicated by the scalar data of `dB`
	# into the scalar data or vector data of `dA`
	# This instruction sets the type tag of `dA` to u8.
	Inu8 = 0

	# ins8.s dA, dB
	# ins8.v dA, dB
	Ins8 = auto()

	# inu16.s dA, dB
	# inu16.v dA, dB
	Inu16 = auto()

	# ins16.s dA, dB
	# ins16.v dA, dB
	Ins16 = auto()
	#--------

	#--------
	# 4 .. 7

	# inu32.s dA, dB
	# inu32.v dA, dB
	Inu32 = auto()

	# ins32.s dA, dB
	# ins32.v dA, dB
	Ins32 = auto()

	# outu8.s dA, dB
	# outu8.v dA, dB
	# Write 8-bit scalar data or vector data that's stored in `dA` to the IO
	# port indicated by the scalar data of `dB` 
	# This instruction does not affect the type tag of `dA`.
	Outu8 = auto()

	# outs8.s dA, dB
	# outs8.v dA, dB
	Outs8 = auto()
	#--------

	#--------
	# 8 .. 11

	# outu16.s dA, dB
	# outu16.v dA, dB
	Outu16 = auto()

	# outs16.s dA, dB
	# outs16.v dA, dB
	Outs16 = auto()

	# outu32.s dA, dB
	# outu32.v dA, dB
	Outu32 = auto()

	# outs32.s dA, dB
	# outs32.v dA, dB
	Outs32 = auto()
	#--------

	#--------
	# 12 .. 15
	# syscall dA
	# System call with call number indicated by the scalar data of `dA`
	Syscall = auto()
	#--------

# DLARs
# `dzero`, the always-zero DLAR, is DLAR 0
# `dcp`, the constant-pool pointer, is DLAR 1
# `dfp`, the frame pointer, is DLAR 2
# `dsp`, the stack pointer, is DLAR 3
# 60 more DLARs, which are general-purpose, are `dg0` to `dg60`

# DLARs are 128 bytes long

# ILARs
# `izero`, the always-zero ILAR, is ILAR #0
# 63 more ILARs, usable for anything, are `ig0` to `ig62`

# ILARS are 128 bytes long
