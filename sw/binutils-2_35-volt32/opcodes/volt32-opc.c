/* volt32-opc.c -- Definitions for volt32 opcodes.
   Copyright (C) 2020 Free Software Foundation, Inc.
   Contributed by Andrew Clark (FL4SHK).

   This file is part of the GNU opcodes library.

   This library is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   It is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
   License for more details.

   You should have received a copy of the GNU General Public License
   along with this file; see the file COPYING.  If not, write to the
   Free Software Foundation, 51 Franklin Street - Fifth Floor, Boston,
   MA 02110-1301, USA.  */

#include "sysdep.h"
#include "opcode/volt32.h"

const volt32_opc_info_t volt32_opc_info[VOLT32_NUM_OPCODES]
= {
	/* -------- */
	/* 0 .. 3 */

	/* add rA, rB, rC */
	{VOLT32_OP_ADD, VOLT32_ARGS_THREE_REGS, "add"},

	/* sub rA, rB, rC */
	{VOLT32_OP_SUB, VOLT32_ARGS_THREE_REGS, "sub"},

	/* addsi rA, rB, simm16 */
	{VOLT32_OP_ADDSI, VOLT32_ARGS_TWO_REGS_SIMM16, "addsi"},

	/* sltu rA, rB, rC */
	{VOLT32_OP_SLTU, VOLT32_ARGS_THREE_REGS, "sltu"},
	/* -------- */

	/* -------- */
	/* 4 .. 7 */

	/* slts rA, rB, rC */
	{VOLT32_OP_SLTS, VOLT32_ARGS_THREE_REGS, "slts"},

	/* mulu rA, rB, rC, rD */
	/* multiply, unsigned full product, high in `rA`, low in `rB` */
	{VOLT32_OP_MULU, VOLT32_ARGS_FOUR_REGS, "mulu"},

	/* muls rA, rB, rC, rD */
	/* multiply, signed full product, high in `rA`, low in `rB` */
	{VOLT32_OP_MULS, VOLT32_ARGS_FOUR_REGS, "muls"},

	/* divu rA, rB, rC, rD */
	/* divmod unsigned, quotient in `rA`, remainder in `rB` */
	{VOLT32_OP_DIVU, VOLT32_ARGS_FOUR_REGS, "divu"},
	/* -------- */

	/* -------- */
	/* 8 .. 11 */

	/* divs rA, rB, rC, rD */
	/* divmod signed, quotient in `rA`, remainder in `rB` */
	{VOLT32_OP_DIVS, VOLT32_ARGS_FOUR_REGS, "divs"},

	/* and rA, rB, rC */
	{VOLT32_OP_AND, VOLT32_ARGS_THREE_REGS, "and"},

	/* or rA, rB, rC */
	{VOLT32_OP_OR, VOLT32_ARGS_THREE_REGS, "or"},

	/* xor rA, rB, rC */
	{VOLT32_OP_XOR, VOLT32_ARGS_THREE_REGS, "xor"},
	/* -------- */

	/* -------- */
	/* 12 .. 15 */

	/* lsl rA, rB, rC */
	{VOLT32_OP_LSL, VOLT32_ARGS_THREE_REGS, "lsl"},

	/* lsr rA, rB, rC */
	{VOLT32_OP_LSR, VOLT32_ARGS_THREE_REGS, "lsr"},

	/* asr rA, rB, rC */
	{VOLT32_OP_ASR, VOLT32_ARGS_THREE_REGS, "asr"},

	/* pre simm24 */
	{VOLT32_OP_PRE, VOLT32_ARGS_SIMM24, "pre"},
	/* -------- */

	/* -------- */
	/* 16 .. 19 */

	/* addsipc rA, simm20 */
	{VOLT32_OP_ADDSI_PC, VOLT32_ARGS_ONE_REG_SIMM20, "addsi.pc"},

	/* jl rA, simm20 */
	/* Jump and link, jumping to location `rA + to_s32(simm20)` */
	{VOLT32_OP_JL, VOLT32_ARGS_ONE_REG_SIMM20, "jl"},

	/* jmp rA, simm20 */
	/* Jump to location `rA + to_s32(simm20)` */
	{VOLT32_OP_JMP, VOLT32_ARGS_ONE_REG_SIMM20, "jmp"},

	/* bz rA, simm20 */
	{VOLT32_OP_BZ, VOLT32_ARGS_ONE_REG_SIMM20, "bz"},
	/* -------- */

	/* -------- */
	/* 20 .. 23 */

	/* bnz rA, simm20 */
	{VOLT32_OP_BNZ, VOLT32_ARGS_ONE_REG_SIMM20, "bnz"},

	/* ld rA, [rB, simm16] */
	{VOLT32_OP_LD, VOLT32_ARGS_LDST, "ld"},

	/* st rA, [rB, simm16] */
	{VOLT32_OP_ST, VOLT32_ARGS_LDST, "st"},

	/* ldh rA, [rB, simm16] */
	{VOLT32_OP_LDH, VOLT32_ARGS_LDST, "ldh"},
	/* -------- */

	/* -------- */
	/* 24 .. 27 */

	/* ldsh rA, [rB, simm16] */
	{VOLT32_OP_LDSH, VOLT32_ARGS_LDST, "ldsh"},

	/* sth rA, [rB, simm16] */
	{VOLT32_OP_STH, VOLT32_ARGS_LDST, "sth"},

	/* ldb rA, [rB, simm16] */
	{VOLT32_OP_LDB, VOLT32_ARGS_LDST, "ldb"},

	/* ldsb rA, [rB, simm16] */
	{VOLT32_OP_LDSB, VOLT32_ARGS_LDST, "ldsb"},
	/* -------- */

	/* -------- */
	/* 28 .. 31 */

	/* stb rA, [rB, simm16] */
	{VOLT32_OP_STB, VOLT32_ARGS_LDST, "stb"},

	/* zeh rA, rB */
	{VOLT32_OP_ZEH, VOLT32_ARGS_TWO_REGS, "zeh"},

	/* zeb rA, rB */
	{VOLT32_OP_ZEB, VOLT32_ARGS_TWO_REGS, "zeb"},

	/* seh rA, rB */
	{VOLT32_OP_SEH, VOLT32_ARGS_TWO_REGS, "seh"},
	/* -------- */

	/* -------- */
	/* 32 .. 35 */

	/* seb rA, rB */
	{VOLT32_OP_SEB, VOLT32_ARGS_TWO_REGS, "seb"},

	/* ei */
	{VOLT32_OP_EI, VOLT32_ARGS_NONE, "ei"},

	/* di */
	{VOLT32_OP_DI, VOLT32_ARGS_NONE, "di"},

	/* reti */
	{VOLT32_OP_RETI, VOLT32_ARGS_NONE, "reti"},
	/* -------- */
};
