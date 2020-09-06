/* Definitions for decoding the volt32 opcode table.
   Copyright (C) 2020 Free Software Foundation, Inc.
   Contributed by Andrew Clark (FL4SHK).

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA
   02110-1301, USA.  */

typedef enum volt32_opc_args_type_t
{
	/* instr */
	VOLT32_ARGS_NONE,

	/* instr rA, rB */
	VOLT32_ARGS_TWO_REGS,

	/* instr rA, rB, rC */
	VOLT32_ARGS_THREE_REGS,

	/* instr rA, rB, rC, rD */
	VOLT32_ARGS_FOUR_REGS,

	/* instr rA, rB, simm16 */
	VOLT32_ARGS_TWO_REGS_SIMM16,

	/* instr simm24 */
	VOLT32_ARGS_SIMM24,

	/* instr rA, simm20 */
	VOLT32_ARGS_ONE_REG_SIMM20,

	/* instr rA, [rB, simm16] */
	VOLT32_ARGS_LDST,
} volt32_opc_args_type_t;

typedef enum volt32_op_t
{
	VOLT32_OP_ADD,
	VOLT32_OP_SUB,
	VOLT32_OP_ADDSI,
	VOLT32_OP_SLTU,

	VOLT32_OP_SLTS,
	VOLT32_OP_MULU,
	VOLT32_OP_MULS,
	VOLT32_OP_DIVU,

	VOLT32_OP_DIVS,
	VOLT32_OP_AND,
	VOLT32_OP_OR,
	VOLT32_OP_XOR,

	VOLT32_OP_LSL,
	VOLT32_OP_LSR,
	VOLT32_OP_ASR,
	VOLT32_OP_PRE,

	VOLT32_OP_ADDSI_PC,
	VOLT32_OP_JL,
	VOLT32_OP_JMP,
	VOLT32_OP_BZ,

	VOLT32_OP_BNZ,
	VOLT32_OP_LD,
	VOLT32_OP_ST,
	VOLT32_OP_LDH,

	VOLT32_OP_LDSH,
	VOLT32_OP_STH,
	VOLT32_OP_LDB,
	VOLT32_OP_LDSB,

	VOLT32_OP_STB,
	VOLT32_OP_ZEH,
	VOLT32_OP_ZEB,
	VOLT32_OP_SEH,

	VOLT32_OP_SEB,
	VOLT32_OP_EI,
	VOLT32_OP_DI,
	VOLT32_OP_RETI,
} volt32_op_t;

typedef struct volt32_opc_info_t
{
	unsigned short opcode;
	volt32_opc_args_type_t args_type;
	const char * name;
} volt32_opc_info_t;

#define VOLT32_NUM_OPCODES 36u
#define VOLT32_NUM_REGS 16u

extern const volt32_opc_info_t volt32_opc_info[VOLT32_NUM_OPCODES];

extern const char *reg_names[NUM_REGS];
extern int reg_index(const char *name);

/* 8 bytes for every frag.  The high 4 bytes are where immediates are
 * stored. */
#define VOLT32_FRAG_SIZE 8
#define VOLT32_FRAG_INDEX_IMM_START 4
#define VOLT32_FRAG_INDEX_IMM_END 7


#define VOLT32_INSTR_WIDTH 32u
#define VOLT32_OP_WIDTH 8u
#define VOLT32_REG_WIDTH 4u
#define VOLT32_REGS_SIZE \
	(uint32_t)((VOLT32_INSTR_WIDTH - VOLT32_OP_WIDTH) / VOLT32_REG_WIDTH)

/* What type of signed immediate is it? */
typedef enum volt32_which_simm_t
{
	VOLT32_WHICH_SIMM_NONE,
	VOLT32_WHICH_SIMM_SIMM16,
	VOLT32_WHICH_SIMM_SIMM20,
	VOLT32_WHICH_SIMM_SIMM24,
	VOLT32_WHICH_SIMM_BAD,
} volt32_which_simm_t;

/* A decoded instruction */
typedef struct volt32_dec_instr_t
{
	uint32_t op: VOLT32_OP_WIDTH;

	uint32_t regs[VOLT32_REGS_SIZE];

	int32_t simm24: 24;
	int32_t simm20: 20;
	int32_t simm16: 16;

	const volt32_opc_info_t * opc_info;

	volt32_which_simm_t which_simm;
} volt32_dec_instr_t;

extern volt32_dec_instr_t
volt32_decode_instr(uint32_t enc_instr);

