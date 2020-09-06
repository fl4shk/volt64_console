/* tc-volt32.h -- Header file for tc-volt32.c.

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

   You should have received a copy of the GNU General Public License along
   with GAS; see the file COPYING.  If not, write to the Free Software
   Foundation, 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.  */

#define TC_VOLT32 1
#define TARGET_BYTES_BIG_ENDIAN 1

#define WORKING_DOT_WORD

struct fix;

/* This macro is the BFD architecture to pass to `bfd_set_arch_mach'.  */
#define TARGET_FORMAT "elf32-volt32"

#define TARGET_ARCH bfd_arch_volt32

#define LOCAL_LABEL_PREFIX '.'

/* GAS will call this function when a symbol table lookup fails, before it
 * creates a new symbol.  Typically this would be used to supply symbols
 * whose name or value changes dynamically, possibly in a context sensitive
 * way.  Predefined symbols with fixed values, such as register names or
 * condition codes, are typically entered directly into the symbol table
 * when `md_begin` is called.  One argument is passed, a `char *` for the
 * symbol. */
#define md_undefined_symbol(NAME) 0

/* These macros must be defined, but it will be a fatal assembler
   error if we ever hit them.  */
/* This function returns an estimate of the size of a
 * `rs_machine_dependent` frag before any relaxing is done.  It may also
 * create any necessary relocations. */
#define md_estimate_size_before_relax(A, B) \
	(as_fatal(_("estimate size\n")), 0)

/* GAS will call this for each rs_machine_dependent fragment.  The
 * instruction is completed using the data from the relaxation pass.  It
 * may also create any necessary relocations. */
#define md_convert_frag(B, S, F) as_fatal(_("convert_frag\n"))

/* GAS will call this function for each section at the end of the assembly,
 * to permit the CPU backend to adjust the alignment of a section.  The
 * function must take two arguments, a `segT` for the section and a
 * `valueT` for the size of the section, and return a `valueT` for the
 * rounded size. */
#define md_section_align(SEGMENT, SIZE) (SIZE)

///* We do relaxing in the assembler as well as the linker. */
//extern const struct relax_type md_relax_table[];
//#define TC_GENERIC_RELAX_TABLE md_relax_table
//
///* We do not want to adjust any relocations to make implementation of
// * linker relaxations easier. */
//#define tc_fix_adjustable(fixP) 0
//
///* We need to force out some relocations when relaxing.
// * We assume the smaller relaxation first until proven otherwise. */
//#define TC_FORCE_RELOCATION(FIXP) volt32_fix_relocation(FIXP)
//extern int volt32_force_relocation(struct fix *);
