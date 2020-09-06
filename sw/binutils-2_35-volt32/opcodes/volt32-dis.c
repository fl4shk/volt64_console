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

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "sysdep.h"

#define STATIC_TABLE
#define DEFINE_TABLE

#include "opcode/volt32.h"
#include "disassemble.h"

static fprintf_ftype fpr;
static void *stream;

//#define VOLT32_INSTR_WIDTH 32u
//#define VOLT32_OP_WIDTH 8u
//#define VOLT32_REG_WIDTH 4u
//#define VOLT32_REGS_SIZE (uint32_t)((VOLT32_INSTR_WIDTH - VOLT32_OP_WIDTH) / VOLT32_REG_WIDTH)

//#define VOLT32_NUM_REGS 16u

#define REG(index) reg_names[main_dec_instr->regs[index]]

/* Instructions are 32-bit */
#define UNIT_INSTR_LENGTH ((uint32_t)sizeof(uint32_t))


const char *reg_names[VOLT32_NUM_REGS]
= {
	"zero", "a0", "a1", "a2",
	"a3", "r0", "r1", "u0",
	"u1", "u2", "u3", "u4",
	"ira", "lr", "fp", "sp"
};

int reg_index(const char *name)
{
	for (int i=0; i<(int)VOLT32_NUM_REGS; ++i)
	{
		if (strcmp(reg_names[i], name) == 0)
		{
			return i;
		}
	}

	return -1;
}

volt32_dec_instr_t
volt32_decode_instr(uint32_t enc_instr)
{
	volt32_dec_instr_t ret;

	/* Most of this is pretty self-explanatory. */
	ret.simm24 = enc_instr & ((1u << 24u) - 1u);
	ret.simm20 = enc_instr & ((1u << 20u) - 1u);
	ret.simm16 = enc_instr & ((1u << 16u) - 1u);

	for (int32_t i=VOLT32_REGS_SIZE - 1; i>0; --i)
	{
		ret.regs[i] = enc_instr & ((1u << VOLT32_REG_WIDTH) - 1u);
		enc_instr >>= VOLT32_REG_WIDTH;
	}
	ret.op = enc_instr & ((1u << VOLT32_OP_WIDTH) - 1u);

	/* Default value. */
	ret.which_simm = VOLT32_WHICH_SIMM_BAD;

	if (ret.op < VOLT32_NUM_OPCODES)
	{
		ret.opc_info = &volt32_opc_info[ret.op];
		switch (ret.opc_info->args_type)
		{
		/* -------- */
		case VOLT32_ARGS_NONE:
		case VOLT32_ARGS_TWO_REGS:
		case VOLT32_ARGS_THREE_REGS:
		case VOLT32_ARGS_FOUR_REGS:
			ret.which_simm = VOLT32_WHICH_SIMM_NONE;
			break;

		case VOLT32_ARGS_TWO_REGS_SIMM16:
		case VOLT32_ARGS_LDST:
			ret.which_simm = VOLT32_WHICH_SIMM_SIMM16;
			break;

		case VOLT32_ARGS_ONE_REG_SIMM20:
			ret.which_simm = VOLT32_WHICH_SIMM_SIMM20;
			break;

		case VOLT32_ARGS_SIMM24:
			ret.which_simm = VOLT32_WHICH_SIMM_SIMM24;
			break;
		/* -------- */
		}
	}
	else /* if (ret.op >= VOLT32_NUM_OPCODES) */
	{
		ret.opc_info = NULL;
	}

	return ret;
}

int
print_insn_volt32(bfd_vma addr, struct disassemble_info * info)
{
	/*
	`length` is either 32-bit or 64-bit, with 64-bit only happening if
	we find a `pre` instruction. 
	*/
	uint32_t length = UNIT_INSTR_LENGTH;
	int status;
	stream = info->stream;
	const volt32_opc_info_t * opcode;

	bfd_byte instr_buffer[UNIT_INSTR_LENGTH];
	fpr = info->fprintf_func;

	dec_instr_t dec_instr[2u];

	if ((status = info->read_memory_func
		(addr, instr_buffer, UNIT_INSTR_LENGTH, info)))
	{
		goto read_mem_fail;
	}

	dec_instr_t * main_dec_instr = &dec_instr[0];
	dec_instr[0] = volt32_decode_instr((uint32_t)bfd_getb32(instr_buffer));
	int32_t full_simm = 0;

	/* Handle `pre` specially. */
	if (dec_instr[0].op == VOLT32_OP_PRE)
	{
		length += UNIT_INSTR_LENGTH;
		full_simm = dec_instr[0].simm24;

		if ((status = info->read_memory_func
			(addr, instr_buffer, UNIT_INSTR_LENGTH, info)))
		{
			goto read_mem_fail;
		}
		dec_instr[1] = decode_instr((uint32_t)bfd_getb32(instr_buffer));
		main_dec_instr = &dec_instr[1];
	}

	switch (main_dec_instr->which_simm)
	{
	/* -------- */
	case VOLT32_WHICH_SIMM_NONE:
		break;
	case VOLT32_WHICH_SIMM_SIMM16:
		full_simm = (full_simm << 16) | main_dec_instr->simm16;
		break;
	case VOLT32_WHICH_SIMM_SIMM20:
		full_simm = (full_simm << 20) | main_dec_instr->simm20;
		break;
	case VOLT32_WHICH_SIMM_SIMM24:
		full_simm = (full_simm << 24) | main_dec_instr->simm24;
		break;
	default:
		abort();
	/* -------- */
	}

	opcode = main_dec_instr->opc_info;
	if (opcode == NULL)
	{
		fpr(stream, "invalid instr");
	}
	else /* if (opcode != NULL) */
	{
		switch (opcode->args_type)
		{
		/* -------- */
		case VOLT32_ARGS_NONE:
			fpr(stream, "%s", opcode->name);
			break;

		case VOLT32_ARGS_TWO_REGS:
			fpr(stream, "%s\t%s, %s", opcode->name,
				REG(0),
				REG(1));
			break;
		case VOLT32_ARGS_THREE_REGS:
			fpr(stream, "%s\t%s, %s, %s", opcode->name,
				REG(0),
				REG(1),
				REG(2));
			break;
		case VOLT32_ARGS_FOUR_REGS:
			fpr(stream, "%s\t%s, %s, %s, %s", opcode->name,
				REG(0),
				REG(1),
				REG(2),
				REG(3));
			break;

		case VOLT32_ARGS_TWO_REGS_SIMM16:
			fpr(stream, "%s\t%s, %s, ", opcode->name,
				REG(0),
				REG(1));
			if (dec_instr[0].op == VOLT32_OP_PRE)
			{
				fpr(stream, "0x%x", full_simm);
			}
			else /* if (dec_instr[0].op != VOLT32_OP_PRE) */
			{
				info->print_address_func((bfd_vma)full_simm, info);
			}
			break;
		case VOLT32_ARGS_SIMM24:
			fpr(stream, "%s\t", opcode->name);
			if (dec_instr[0].op == VOLT32_OP_PRE)
			{
				fpr(stream, "0x%x", full_simm);
			}
			else /* if (dec_instr[0].op != VOLT32_OP_PRE) */
			{
				info->print_address_func((bfd_vma)full_simm, info);
			}
			break;

		case VOLT32_ARGS_ONE_REG_SIMM20:
			fpr(stream, "%s\t%s, ", opcode->name,
				REG(0));
			if (dec_instr[0].op == VOLT32_OP_PRE)
			{
				fpr(stream, "0x%x", full_simm);
			}
			else /* if (dec_instr[0].op != VOLT32_OP_PRE) */
			{
				info->print_address_func((bfd_vma)full_simm, info);
			}
			break;

		case VOLT32_ARGS_LDST:
			fpr(stream, "%s\t%s, [%s, ", opcode->name,
				REG(0),
				REG(1));
			if (dec_instr[0].op == VOLT32_OP_PRE)
			{
				fpr(stream, "0x%x", full_simm);
			}
			else /* if (dec_instr[0].op != VOLT32_OP_PRE) */
			{
				info->print_address_func((bfd_vma)full_simm, info);
			}
			fpr(stream, "]");
			break;

		default:
			abort();
			break;
		/* -------- */
		}
	}

	return length;

	read_mem_fail:
		info->memory_error_func(status, addr, info);
		return -1;
}
