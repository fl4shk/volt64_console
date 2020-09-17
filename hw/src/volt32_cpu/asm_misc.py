#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto

class Volt32EncGrp(Enum):
	#--------
	# 0 .. 3

	# Encoding:  0000 aaaa aabb bbbb  cccc ccoo iiii jjjj
	# * a:  `dA`
	# * b:  `iB`
	# * c:  `iC`
	# * o:  opcode
	# * i:  `imm4b`.  4-bit immediate indicating which instruction in `iB`
	# to jump to
	# * j:  `imm4c`.  4-bit immediate indicating which instruction in `iC`
	# to jump to
	Grp0 = 0

	# Encoding:  0001 aaaa aabb bbbb  cccc ccoo ooov 0000
	# * a:  `dA`
	# * b:  `dB`
	# * c:  `dC`
	# * o:  opcode
	# * v:  1 if vector op, 0 if scalar op
	Grp1 = auto()

	# Encoding:  0010 aaaa aajj bbbb  cccc ccji iiii iiii
	# * a:  `iA`.  The first destination ILAR
	# * j:  `imm4`.  The number of consecutive destination ILARs to `fetch`
	# into.
	# * b:  `dB`.  Only allows for the low 16 DLARs to be selected.
	# `dB.scalar_data` is used by this instruction. 
	# * c:  `iC`.  `iC.addr` is used by this instruction.
	# * i:  `simm9`.  Signed, 9-bit immediate

	# Instruction:  fetch iA, imm4, dB, iC, simm9
	Grp2 = auto()

	# Encoding:  0011 aaaa aabb bbbb  oooo iiii iiii iiii
	# * a:  `dA`
	# * b:  `dB`, used as `dB.scalar_data`
	# * o:  `opcode`
	# * i:  `simm12`
	Grp3 = auto()
	#--------

	#--------
	# 4 .. 7

	# Encoding:  0100 aaaa aabb bbbb  oooo iiii ii00 0000
	# * a:  `dA`.  For some instructions, supervisor-mode base DLAR.
	# * b:  `dB` or `iB`.  For some instructions, user-mode base DLAR or
	# ILAR.
	# * o:  opcode
	# * i:  `imm6`.  Unsigned 6-bit immediate indicating the number of
	# consecutive user-mode LARs after the base.
	Grp4 = auto()

	# Encoding:  0101 aaaa aabb bbbb  cccc ccoo oov00 0000
	# * a:  `dA`
	# * b:  `dB`
	# * c:  `dC`
	# * o:  opcode
	# * v:  1 if vector op, 0 if scalar op
	Grp5 = auto()

	# Encoding:  0110 aaaa aabb bbbb  oooo oiii iii0 0000
	# * a:  `dA`
	# * b:  `dB`
	# * o:  opcode
	# * i:  imm6, unsigned 6-bit immediate
	Grp6 = auto()
	#--------

# Group 0 Instructions
class Volt32Grp0Op(Enum):
	#--------
	# 0 .. 3

	# jmp.s dA, iB, iC, imm4b, imm4c
	# * This instruction jumps to iB (index given by imm4b) if `dA`'s
	# scalar data is non-zero, else to iC (index given by imm4c)
	JmpS = 0
	
	# jmp.v dA, iB, iC, imm4b, imm4c
	# This instruction jumps to iB (index given by imm4b) if `dA`'s
	# entire vector data is non-zero, else to iC (index given by imm4c)
	JmpV = auto()

	# jtbl dA
	# Jump table jump instruction, with destination ILAR and offset into
	# that ILAR obtained from the scalar data of `dA`.
	Jtbl = auto()

	# jr dA, iB
	# Indirect jump helper instruction that jumps to `iB`, using the low 4
	# bits of the scalar data of `dA` to encode which instruction in `iB`
	# to jump to.
	Jr = auto()
	#--------

# Group 1 Instructions
class Volt32Grp1Op(Enum):
	#--------
	# 0 .. 3

	# add dA, dB, dC
	Add = 0

	# sub dA, dB, dC
	Sub = auto()

	# slt dA, dB, dC
	Slt = auto()

	# mul dA, dB, dC
	# This instruction forcibly treats all three DLARs as vectors of 32-bit
	Mul = auto()
	#--------

	#--------
	# 4 .. 7

	# udiv dA, dB, dC
	# This instruction forcibly treats all three DLAR arguments as vectors
	# of `u32`
	Udiv = auto()

	# sdiv dA, dB, dC
	# This instruction forcibly treats all three DLAR arguments as vectors
	# of `s32`
	Sdiv = auto()

	# umull.hi dA, dB, dC
	# Unsigned full product
	# This instruction forcibly treats `dA` as a vector of `u64`, `dB` as a
	# vector of `u32`, and `dC` as a vector of `u32`.
	# The high-numbered 32-bit vector elements of `dB` and `dC` are used
	# when this is a vector instruction.
	UmullHi = auto()

	# smull.hi dA, dB, dC
	# Signed full product
	# This instruction forcibly treats `dA` as a vector of `s64`, `dB` as a
	# vector of `s32`, and `dC` as a vector of `s32`.
	# The high-numbered 32-bit vector elements of `dB` and `dC` are used
	# when this is a vector instruction.
	SmullHi = auto()
	#--------

	#--------
	# 8 .. 11

	# umull.lo dA, dB, dC
	# Unsigned full product
	# This instruction forcibly treats `dA` as a vector of `u64`, `dB` as a
	# vector of `u32`, and `dC` as a vector of `u32`.
	# The low-numbered 32-bit vector elements of `dB` and `dC` are used
	# when this is a vector instruction.
	UmullLo = auto()

	# smull.lo dA, dB, dC
	# Signed full product
	# This instruction forcibly treats `dA` as a vector of `s64`, `dB` as a
	# vector of `s32`, and `dC` as a vector of `s32`.
	# The low-numbered 32-bit vector elements of `dB` and `dC` are used
	# when this is a vector instruction.
	SmullLo = auto()

	# udivl.hi dA, dB, dC
	# This instruction forcibly treats `dA` as a vector of `u64`, `dB` as a
	# vector of `u64`, and `dC` as a vector of `u32`.
	# The high-numbered 32-bit vector elements of `dC` are used when this
	# is a vector instruction.
	UdivlHi = auto()

	# sdivl.hi dA, dB, dC
	# This instruction forcibly treats `dA` as a vector of `s64`, `dB` as a
	# vector of `s64`, and `dC` as a vector of `s32`.
	# The high-numbered 32-bit vector elements of `dC` are used when this
	# is a vector instruction.
	SdivlHi = auto()
	#--------

	#--------
	# 12 .. 15

	# udivl.lo dA, dB, dC
	# This instruction forcibly treats `dA` as a vector of `u64`, `dB` as a
	# vector of `u64`, and `dC` as a vector of `u32`.
	# The low-numbered 32-bit vector elements of `dC` are used when this
	# is a vector instruction.
	UdivlLo = auto()

	# sdivl.lo dA, dB, dC
	# This instruction forcibly treats `dA` as a vector of `s64`, `dB` as a
	# vector of `s64`, and `dC` as a vector of `s32`.
	# The low-numbered 32-bit vector elements of `dC` are used when this
	# is a vector instruction.
	SdivlLo = auto()

	# and dA, dB, dC
	And = auto()

	# or dA, dB, dC
	Or = auto()
	#--------

	#--------
	# 16 .. 19

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

# Group 3 Instructions
class Volt32Grp3Op(Enum):
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

# Group 4 Instructions
class Volt32Grp4Op(Enum):
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

	# syscall dA
	# System call with call number indicated by the scalar data of `dA`
	Syscall = auto()
	#--------

# Group 5 Instructions
class Volt32Grp5Op(Enum):
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

class Volt32Grp6Op(Enum):
	#--------
	# 0 .. 3

	# extu16 dA, dB
	# This instruction tags `dA` as u16.
	# This instruction does nothing if `dB` is tagged as u16, u32, s32.

	# This instruction extends every vector element of dB to u16 and stores
	# the results in consecutive DLARs starting with `dA` and performing
	# descending storage, such that `dA` itself will have the
	# highest-numbered vector elements of the result.
	# Also, zero extension will be performed if `dB` is tagged as u8, u16,
	# or u8, but sign extension will be performed if `dB` is tagged as s8,
	# s16, or s8.
	# For example, if `dB` is tagged as u8, the results will be stored in
	# `dA` and `d{A+1}`, where `d{A+1}` will contain the low 32 16-bit
	# elements of the resulting vector.
	Extu16 = auto()

	# exts16 dA, dB
	Exts16 = auto()

	# extu32 dA, dB
	Extu32 = auto()

	# exts32 dA, dB
	Exts32 = auto()
	#--------

	#--------
	# 4 .. 7

	# ext64 dA, dB
	# Due to the lack of any 64-bit type tags, this instruction will not
	# change the type tag of `dA`
	Ext64 = auto()

	# tru8 dA, dB, imm6
	# This instruction trates every vector element of `dB` down to 8-bit
	# and sets the type tag of `dA` to u8.
	# This instruction uses `imm6` to determine where to place the
	# highest-numbered resulting vector element.  
	Tru8 = auto()

	# trs8 dA, dB, imm6
	Trs8 = auto()

	# tru16 dA, dB, imm6
	Tru16 = auto()
	#--------

	#--------
	# 8 .. 11

	# trs16 dA, dB, imm6
	Trs16 = auto()

	# tru32 dA, dB, imm6
	Tru32 = auto()

	# trs32 dA, dB, imm6
	Trs32 = auto()

	# tr64u8 da, dB, imm6
	# This instruction sets the type tag of `dA` to u8.
	Tr64u8 = auto()
	#--------

	#--------
	# 12 .. 15

	# tr64s8 da, dB, imm6
	# This instruction sets the type tag of `dA` to u8.
	# This instruction treats `dB` as if it were a vector of 64-bit
	# elements, downcasting them down 
	Tr64s8 = auto()

	# tr64u16 dA, dB, imm6
	Tr64u16 = auto()

	# tr64s16 dA, dB, imm6
	Tr64s16 = auto()

	# tr64u32 dA, dB, imm6
	Tr64u32 = auto()

	#--------
	# 16 .. 19

	# tr64s32 dA, dB, imm6
	Tr64s32 = auto()
	#--------

# DLARs
# `dzero`, the always-zero DLAR, is DLAR 0
# `dbcp`, the base constant-pool pointer, is DLAR 1
# `dres0`, the assembler-reserved DLAR #0, is DLAR 2
# `dres1`, the assembler-reserved DLAR #1, is DLAR 3
# `dres2`, the assembler-reserved DLAR #2, is DLAR 4
# `dres3`, the assembler-reserved DLAR #3, is DLAR 5
# `dres4`, the assembler-reserved DLAR #4, is DLAR 6
# `dres5`, the assembler-reserved DLAR #5, is DLAR 7
# `dfp`, the frame pointer, is DLAR 8
# `dsp`, the stack pointer, is DLAR 9
# DLARs 10 to 63, which are general-purpose, are `dg0` to `dg53`

# DLARs are 64 bytes long

# ILARs
# `izero`, the always-zero ILAR, is ILAR #0
# ILARs 1 to 63, which are general-purpose, are `ig0` to `ig62`

# ILARS are 64 bytes long
