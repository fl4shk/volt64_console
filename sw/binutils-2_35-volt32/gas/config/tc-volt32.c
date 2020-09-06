/* tc-volt32.c -- Assemble code for volt32
   Copyright (C) 2020 Free Software Foundation, Inc.

   This file is part of GAS, the GNU Assembler.

   GAS is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   GAS is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with GAS; see the file COPYING.  If not, write to
   the Free Software Foundation, 51 Franklin Street - Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* Contributed by Andrew Clark (FL4SHK). */

#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "as.h"
#include "safe-ctype.h"
#include "opcode/volt32.h"
#include "elf/volt32.h"

const char comment_chars[] = "#";
const char line_separator_chars[] = ";";
const char line_comment_chars[] = "#";

static int pending_reloc;
static struct hash_control *opcode_hash_control;

const pseudo_typeS md_pseudo_table[]
= {
	{0, 0, 0}
};

/* Floating point characters */
const char FLT_CHARS[] = "rRsSfFdDxXpP";
const char EXP_CHARS[] = "eE";

void
md_operand(expressionS *op __attribute__((unused)))
{
	/* Empty for now. */
}

/* This function is called once, at assembler startup time.  It sets up the
 * hash table with all the opcodes in it, and also initializes some aliases
 * for compatibility with other assemblers. */
void
md_begin(void)
{
	opcode_hash_control = hash_new();

	/* Insert instruction names into hash table. */
	for (size_t i=0; i<VOLT32_NUM_OPCODES; ++i)
	{
		const volt32_opc_info_t *opcode = &volt32_opc_info[i];
		hash_insert(opcode_hash_control, opcode->name, (char *)opcode);
	}

	/* I don't really know what this is for, but it's in `tc-moxie.c`. */
	bfd_set_arch_mach(stdoutput, TARGET_ARCH, 0);
}

/* Parse an expression and then restore the input line pointer. */
static char *
parse_exp_save_ilp(char *s, expressionS *op)
{
	char *save = input_line_pointer;

	input_line_pointer = s;
	expression(op);
	s = input_line_pointer;
	input_line_pointer = save;
	return s;
}

///* This stores the length of `to_cmp` within `*len` */
//static bool
//my_strcmp(char *self, const char *to_cmp, size_t *len)
//{
//	*len = strlen(to_cmp);
//	if (strncmp((const char *)self, to_cmp, *len) == 0)
//	{
//		return true;
//	}
//	else
//	{
//		return false;
//	}
//}

static int
parse_reg_operand(char **ptr)
{
	int reg;
	char *s = *ptr;

	for (int i=0; i<(int)NUM_REGS; ++i)
	{
		const size_t len = strlen(reg_names[i]);
		if (strncmp((const char *)s, reg_names[i], len) == 0)
		{
			*ptr += len;
			return i;
		}
	}

	as_bad(_("expecting register"));
	ignore_rest_of_line();
	return -1;

	//bad_reg_num:
	//	as_bad(_("illegal register number"));
	//	ignore_rest_of_line();
	//	return -1;
}

static void
eat_whitespace(char **op_end)
{
	while (ISSPACE(**op_end))
	{
		++(*op_end);
	}
}
static void
parse_char_then_eat_ws(char **op_end, char c, const char *warn_msg)
{
	if (**op_end != c)
	{
		as_warn(_(warn_msg));
	}
	++(*op_end);

	eat_whitespace(op_end);
}
static inline void
parse_comma(char **op_end)
{
	parse_char_then_eat_ws(op_end, ',', "expecting comma");
}

static inline int
volt32_op_shift(void)
{
	return 24;
}
static inline int
volt32_ra_shift(void)
{
	return 20;
}
static inline int
volt32_rb_shift(void)
{
	return 16;
}
static inline int
volt32_rc_shift(void)
{
	return 12;
}
static inline int
volt32_rd_shift(void)
{
	return 8;
}
static inline int
volt32_re_shift(void)
{
	return 4;
}
static inline int
volt32_rf_shift(void)
{
	return 0;
}

#define PARSE_REG(shift) \
	iword |= (parse_reg_operand(&op_end) << shift) & 0xfu

/* This is the guts of the machine-dependent assembler.  STR points to
   a machine dependent instruction.  This function is supposed to emit the
   frags/bytes it assembles to.  */
void
md_assemble(char *str)
{
	char *op_start;
	char *op_end;

	volt32_opc_info_t *opc_info;
	char *p;
	char pend;

	/* Instruction word */
	uint32_t iword;

	/* */
	int nlen = 0;

	/* Drop leading whitespace. */
	while ((str[0] == ' ') || (str[0] == '\t'))
	{
		++str;
	}

	/* Find the opc_info end. */
	op_start = str;
	for (op_end=str;
		(op_end[0] != '\0') && (!is_end_of_line[op_end[0] & 0xff])
		&& (op_end[0] != ' ') && (op_end[0] != '\t');
		++op_end)
	{
		++nlen;
	}


	pend = op_end[0];

	/* Null terminate */
	op_end[0] = '\0';

	if (nlen == 0)
	{
		as_bad(_("can't find instruction"));
	}

	opc_info = (volt32_opc_info_t *)hash_find(opcode_hash_control,
		op_start);
	op_end[0] = pend;

	if (opc_info == NULL)
	{
		as_bad(_("unknown instruction %s"), op_start);
		return;
	}

	/* This is the frag we use for the current instruction. */
	p = frag_more(FRAG_SIZE);

	iword = (opc_info->opcode << volt32_op_shift()) & 0xffu;
	switch (opc_info->args_type)
	{
	/* -------- */
	case VOLT32_ARGS_NONE:
		{
		}
		break;

	case VOLT32_ARGS_TWO_REGS:
		{
			eat_whitespace(&op_end);

			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rb_shift());
		}
		break;
	case VOLT32_ARGS_THREE_REGS:
		{
			eat_whitespace(&op_end);

			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rb_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rc_shift());
		}
		break;
	case VOLT32_ARGS_FOUR_REGS:
		{
			eat_whitespace(&op_end);

			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rb_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rc_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rd_shift());
		}
		break;
	case VOLT32_ARGS_TWO_REGS_SIMM16:
		{
			eat_whitespace(&op_end);

			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rb_shift());

			expressionS arg;
			char *offset;
			op_end = parse_exp_save_ilp(op_end, &arg);
			fix_new_exp
			(
				frag_now, /* fragS *frag; Which frag? */

				/* Store immediate values starting at offset 2 */
				(p + FRAG_INDEX_IMM_START) - frag_now->fr_literal,
					/* unsigned long where; Where in that frag? */

				sizeof(uint32_t),
					/* unsigned long size; 1, 2, or 4 usually. */

				&arg, /* expressionS *exp; Expression. */

				FALSE, /* int pcrel; TRUE If PC-relative relocation. */

				BFD_RELOC_16 /* RELOC_ENUM r_type; Relocation type. */
			);
		}
		break;
	case VOLT32_ARGS_SIMM24:
		{
			if (opc_info->opcode == VOLT32_OP_PRE)
			{
				as_bad(_("Invalid use of the `pre` instruction."));
			}
			else
			{
				eat_whitespace(&op_end);
			}
		}
		break;
	case VOLT32_ARGS_ONE_REG_SIMM20:
		{
			eat_whitespace(&op_end);
			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
		}
		break;
	case VOLT32_ARGS_LDST:
		{
			eat_whitespace(&op_end);

			PARSE_REG(volt32_ra_shift());
			parse_comma(&op_end);
			PARSE_REG(volt32_rb_shift());
			parse_comma(&op_end);
		}
		break;
	default:
		abort();
		break;
	/* -------- */
	}

	md_number_to_chars(p, iword, sizeof(iword));
	dwarf2_emit_insn(sizeof(iword));

	eat_whitespace(&op_end);

	if (*op_end != '\0')
	{
		as_warn(_("extra stuff on line ignored"));
	}

	if (pending_reloc)
	{
		as_bad(_("Something forgot to clean up\n"));
	}
}

/* Put number into target byte order.  */
void
md_number_to_chars(char *ptr, valueT use, int nbytes)
{
	number_to_chars_bigendian(ptr, use, nbytes);
}


/* Turn a string in input_line_pointer into a floating point constant
   of type type, and store the appropriate bytes in *LITP.  The number
   of LITTLENUMS emitted is stored in *SIZEP .  An error message is
   returned, or NULL on OK.  */
const char *
md_atof (int type, char *litP, int *sizeP)
{
	int prec;
	LITTLENUM_TYPE words[4];
	char *t;
	int i;

	switch (type)
	{
	case 'f':
		prec = 2;
		break;

	case 'd':
		prec = 4;
		break;

	default:
		*sizeP = 0;
		return _("bad call to md_atof");
	}

	t = atof_ieee(input_line_pointer, type, words);
	if (t)
	{
		input_line_pointer = t;
	}

	*sizeP = prec * 2;

	for (i=prec - 1; i>=0; --i)
	{
		md_number_to_chars(litP, (valueT)words[i], 2);
		litP += 2;
	}

	return NULL;
}
