/* volt32-specific support for 32-bit ELF.
   Copyright (C) 2020 Free Software Foundation, Inc.

   Copied from elf32-moxie.c which is..
   Copyright (C) 2009-2020 Free Software Foundation, Inc.

   This file is part of BFD, the Binary File Descriptor library.

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
   Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston,
   MA 02110-1301, USA.  */

#include "sysdep.h"
#include "bfd.h"
#include "libbfd.h"
#include "elf-bfd.h"
#include "elf/volt32.h"

#include <stdint.h>

/* Forward declarations */
static reloc_howto_type volt32_elf_howto_table[]
= {
	/* This reloc does nothing. */
	HOWTO(R_VOLT32_NONE,		/* type */
		0,						/* rightshift */
		3,						/* size (0 = byte, 1 = short, 2 = long) */
		0,						/* bitsize */
		FALSE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_dont,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_NONE",		/* name */
		FALSE,					/* partial_inplace */
		0,						/* src_mask */
		0,						/* dst_mask */
		FALSE),					/* pcrel_offset */

	/* A signed, 16-bit relocation. */
	HOWTO(R_VOLT32_16,		/* type */
		0,						/* rightshift */
		1,						/* size (0 = byte, 1 = short, 2 = long) */
		16,						/* bitsize */
		FALSE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_signed,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_16",			/* name */
		FALSE,					/* partial_inplace */
		0x00000000,				/* src_mask */
		0x0000ffff,				/* dst_mask */
		FALSE),					/* pcrel_offset */

	/* A signed, 20-bit relocation. */
	HOWTO(R_VOLT32_20,		/* type */
		0,						/* rightshift */
		2,						/* size (0 = byte, 1 = short, 2 = long) */
		20,						/* bitsize */
		FALSE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_signed,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_20",			/* name */
		FALSE,					/* partial_inplace */
		0x00000000,				/* src_mask */
		0x000fffff,				/* dst_mask */
		FALSE),					/* pcrel_offset */

	/* A signed, 20-bit pc-relative relocation. */
	HOWTO(R_VOLT32_20_PCREL,	/* type */
		2,						/* rightshift */
		2,						/* size (0 = byte, 1 = short, 2 = long) */
		20,						/* bitsize */
		TRUE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_signed,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_20_PCREL",	/* name */
		FALSE,					/* partial_inplace */
		0x00000000,				/* src_mask */
		0x000fffff,				/* dst_mask */
		TRUE),					/* pcrel_offset */

	/* A 32-bit absolute relocation */
	/* We want this to be converted to `R_VOLT32_16` or `R_VOLT32_20` if
	 * the immediate value fits. */
	HOWTO(R_VOLT32_32,	/* type */
		0,						/* rightshift */
		2,						/* size (0 = byte, 1 = short, 2 = long) */
		32,						/* bitsize */
		FALSE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_bitfield,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_32",	/* name */
		FALSE,					/* partial_inplace */
		0x00000000,				/* src_mask */
		0xffffffff,				/* dst_mask */
		FALSE),					/* pcrel_offset */

	/* A signed, 32-bit pc-relative relocation */
	/* We want this to be converted to `R_VOLT32_20_PCREL` if the immediate
	 * value fits. */
	HOWTO(R_VOLT32_20_PCREL_AS_32,	/* type */
		2,						/* rightshift */
		2,						/* size (0 = byte, 1 = short, 2 = long) */
		32,						/* bitsize */
		TRUE,					/* pc_relative */
		0,						/* bitpos */
		complain_overflow_bitfield,	/* complain_on_overflow */
		bfd_elf_generic_reloc,	/* special_function*/
		"R_VOLT32_20_PCREL_AS_32",	/* name */
		FALSE,					/* partial_inplace */
		0x00000000,				/* src_mask */
		0xffffffff,				/* dst_mask */
		TRUE),					/* pcrel_offset */

};

#define TABLE_SIZE(table) (sizeof(table) / sizeof(table[0]))

/* Map BFD reloc types to VOLT32 ELF reloc types. */
typedef struct volt32_reloc_map_t
{
	bfd_reloc_code_real_type bfd_reloc_val;
	unsigned volt32_reloc_val;
} volt32_reloc_map_t;

static const volt32_reloc_map_t volt32_reloc_map[]
= {
	{BFD_RELOC_NONE, R_VOLT32_NONE},
	{BFD_RELOC_16, R_VOLT32_16},
	{BFD_RELOC_VOLT32_20, R_VOLT32_20},
	{BFD_RELOC_VOLT32_20_PCREL, R_VOLT32_20_PCREL},
	{BFD_RELOC_32, R_VOLT32_32},
	{BFD_RELOC_VOLT32_20_PCREL_AS_32, R_VOLT32_20_PCREL_AS_32},
};

static reloc_howto_type *
volt32_reloc_type_lookup(bfd *abfd ATTRIBUTE_UNUSED,
	bfd_reloc_code_real_type code)
{
	for (unsigned i=TABLE_SIZE(volt32_reloc_map); i!=0; --i)
	{
		if (volt32_reloc_map[i].bfd_reloc_val == code)
		{
			return &volt32_elf_howto_table[volt32_reloc_map[i]
				.volt32_reloc_val];
		}
	}
	return NULL;
}
static reloc_howto_type *
volt32_reloc_name_lookup(bfd *abfd ATTRIBUTE_UNUSED, const char *r_name)
{
	for (unsigned i=0; i<TABLE_SIZE(volt32_elf_howto_table); ++i)
	{
		if ((volt32_elf_howto_table[i].name != NULL)
			&& strcasecmp(volt32_elf_howto_table[i].name, r_name) == 0)
		{
			return &volt32_elf_howto_table[i];
		}
	}

	return NULL;
}

/* Set the howto pointer for a VOLT32 ELF reloc. */
static bfd_boolean
volt32_info_to_howto_rela(bfd *abfd, arelent *cache_ptr,
	Elf_Internal_Rela *dst)
{
	/* Extract the type from the relocation info */
	unsigned r_type = ELF32_R_TYPE(dst->r_info);

	if (r_type >= (unsigned)R_VOLT32_max)
	{
		/* xgettext:c-format */
		_bfd_error_handler(_("%pB: unsupported relocation type %#x"),
			abfd, r_type);
		bfd_set_error(bfd_error_bad_value);
		return FALSE;
	}
	cache_ptr->howto = &volt32_elf_howto_table[r_type];
	return TRUE;
}

/* Perform a single relocation.  By default we use the standard BFD
 * routines, but we have to do a few relocs ourselves. */
static bfd_reloc_status_type
volt32_final_link_relocate(reloc_howto_type *howto, bfd *input_bfd,
	asection *input_section, bfd_byte *contents, Elf_Internal_Rela *rel,
	bfd_vma relocation)
{
	bfd_reloc_status_type r = bfd_reloc_ok;

	switch (howto->type)
	{
	/* -------- */
	default:
		r = _bfd_final_link_relocate(howto, input_bfd, input_section,
			contents, rel->r_offset, relocation, rel->r_addend);
	/* -------- */
	}

	return r;
}

/* Relocate a VOLT32 ELF section. */
static bfd_boolean
volt32_elf_relocate_section(bfd *output_bfd, struct bfd_link_info *info,
	bfd *input_bfd, asection *input_section, bfd_byte *contents,
	Elf_Internal_Rela *relocs, Elf_Internal_Sym *local_syms,
	asection **local_sections)
{
	/* Section header */
	Elf_Internal_Shdr *symtab_hdr;

	/* ELF linker hash table entries */
	struct elf_link_hash_entry **sym_hashes;

	/* Relocation entries, which are
	 * for loop variables */
	Elf_Internal_Rela *rel;
	Elf_Internal_Rela *relend;

	symtab_hdr = &elf_tdata(input_bfd)->symtab_hdr;
	sym_hashes = elf_sym_hashes(input_bfd);

	/* Basic pointer arithmetic */
	relend = relocs + input_section->reloc_count;

	for (rel=relocs; rel<relend; ++rel)
	{
		reloc_howto_type *howto;
		unsigned long r_symndx;

		/* Symbol table entry */
		Elf_Internal_Sym *sym;

		asection *sec;

		/* ELF linker hash table entries */
		struct elf_link_hash_entry *h;

		bfd_vma relocation;
		bfd_reloc_status_type r;
		const char *name;
		int r_type;

		r_type = ELF32_R_TYPE(rel->r_info);
		r_symndx = ELF32_R_SYM(rel->r_info);
		howto = volt32_elf_howto_table + r_type;
		h = NULL;
		sym = NULL;
		sec = NULL;

		if (r_symndx < symtab_hdr->sh_info)
		{
			sym = local_syms + r_symndx;
			sec = local_sections[r_symndx];
			relocation = _bfd_elf_rela_local_sym(output_bfd, sym, &sec,
				rel);

			name = bfd_elf_string_from_elf_section
				(input_bfd, symtab_hdr->sh_link, sym->st_name);
			name = name == NULL ? bfd_section_name(sec) : name;
		}
		else
		{
			bfd_boolean unresolved_reloc, warned, ignored;

			RELOC_FOR_GLOBAL_SYMBOL(info, input_bfd, input_section, rel,
				r_symndx, symtab_hdr, sym_hashes, h, sec, relocation,
				unresolved_reloc, warned, ignored);

			name = h->root.root.string;
		}

		if (sec != NULL && discarded_section (sec))
		{
			RELOC_AGAINST_DISCARDED_SECTION (info, input_bfd,
				input_section, rel, 1, relend, howto, 0, contents);
		}

		if (bfd_link_relocatable(info))
		{
			continue;
		}

		r = volt32_final_link_relocate(howto, input_bfd, input_section,
			contents, rel, relocation);

		if (r != bfd_reloc_ok)
		{
			const char * msg = NULL;

			switch (r)
			{
			case bfd_reloc_overflow:
				(*info->callbacks->reloc_overflow)
					(info, (h ? &h->root : NULL), name, howto->name,
					(bfd_vma)0, input_bfd, input_section, rel->r_offset);
				break;

			case bfd_reloc_undefined:
				(*info->callbacks->undefined_symbol)
					(info, name, input_bfd, input_section, rel->r_offset,
					TRUE);
				break;

			case bfd_reloc_outofrange:
				msg = _("internal error: out of range error");
				break;

			case bfd_reloc_notsupported:
				msg = _("internal error: unsupported relocation error");
				break;

			case bfd_reloc_dangerous:
				msg = _("internal error: dangerous relocation");
				break;

			default:
				msg = _("internal error: unknown error");
				break;
			}

			if (msg)
			{
				(*info->callbacks->warning)(info, msg, name, input_bfd,
					input_section, rel->r_offset);
			}
		}
	}

  return TRUE;
}

/* Return the section that should be marked against GC for a given
 * relocation.  */

static asection *
volt32_elf_gc_mark_hook(asection *sec, struct bfd_link_info *info,
	Elf_Internal_Rela *rel, struct elf_link_hash_entry *h,
	Elf_Internal_Sym *sym)
{
  return _bfd_elf_gc_mark_hook (sec, info, rel, h, sym);
}

/* Look through the relocs for a section during the first phase.
 * Since we don't do .gots or .plts, we just need to consider the
 * virtual table relocs for gc.  */
static bfd_boolean
volt32_elf_check_relocs(bfd *abfd, struct bfd_link_info *info,
	asection *sec, const Elf_Internal_Rela *relocs)
{
	Elf_Internal_Shdr *symtab_hdr;
	struct elf_link_hash_entry **sym_hashes;
	const Elf_Internal_Rela *rel;
	const Elf_Internal_Rela *rel_end;

	if (bfd_link_relocatable (info))
	{
		return TRUE;
	}

	symtab_hdr = &elf_tdata(abfd)->symtab_hdr;
	sym_hashes = elf_sym_hashes(abfd);

	rel_end = relocs + sec->reloc_count;
	for (rel=relocs; rel<rel_end; ++rel)
	{
		struct elf_link_hash_entry *h;
		unsigned long r_symndx;

		r_symndx = ELF32_R_SYM(rel->r_info);
		if (r_symndx < symtab_hdr->sh_info)
		{
			h = NULL;
		}
		else
		{
			h = sym_hashes[r_symndx - symtab_hdr->sh_info];
			while (h->root.type == bfd_link_hash_indirect
				|| h->root.type == bfd_link_hash_warning)
			{
				h = (struct elf_link_hash_entry *)h->root.u.i.link;
			}
		}
	}

	return TRUE;
}

/* Relax a section.
 * Pass 0 shortens code sequences unless disabled.
 * Pass 1 deletes the bytes that pass 0 made obsolete.
 * Pass 2, which cannot be disabled, handles code alignment directives. */
	/* pseudo code:
	 *	if section shouldn't be relaxed:
	 *		return DONE
	 *	for each relocation:
	 *		if relocation if relaxable:
	 *			store per-relocation function pointer
	 *		read the symbol table
	 *		obtain the symbol's address
	 *		call the per-relocation function */

/* Relax a section.
 * */
static bfd_boolean
volt32_bfd_relax_section(bfd *abfd, asection *sec,
	struct bfd_link_info *info, bfd_boolean *again)
{
	Elf_Internal_Shdr *symtab_hdr;
	Elf_Internal_Rela *relocs;
	Elf_Internal_Rela *rel, *relend;
	bfd_byte *contents = NULL;
	Elf_Internal_Sym *symbuf = NULL;

	/* Assume nothing changes. */
	*again = FALSE;

	/* We don't have to do anything for a relocatable link, if
	 * this section does not have relocs, or if this is not a
	 * code section. */
	if (bfd_link_relocatable(link_info)
		|| ((sec->flags & SEC_RELOC) == 0)
		|| (sec->reloc_count == 0)
		|| ((sec->flags & SEC_CODE) == 0))
	{
		return TRUE;
	}

	symtab_hdr = &elf_tdata(abfd)->symtab_hdr;

	/* Get a copy of the native relocations. */
	relocs = _bfd_elf_link_read_relocs(abfd, sec, NULL, NULL,
		link_info->keep_memory);

	if (relocs == NULL)
	{
		goto error_return;
	}

	/* Walk through them looking for relaxing opportunities. */
	relend = relocs + sec->reloc_count;
	for (rel=relocs; rel<relend; ++rel)
	{
		bfd_vma symval;

		const int r_type = ELF32_R_TYPE(rel->r_info);
		const int r_sym = ELF32_R_SYM(rel->r_info);

		/* If this isn't something that can be relaxed, then ignore this
		 * reloc. */
		if ((r_type != (int)R_VOLT32_NONE)
			&& (r_type != (int)R_VOLT32_16)
			&& (r_type != (int)R_VOLT32_20)
			&& (r_type != (int)R_VOLT32_20_PCREL))
		{
			continue;
		}

		/* Get the section contents if we haven't done so already. */
		if (contents == NULL)
		{
			/* Get cached copy if it exists.  */
			if (elf_section_data(sec)->this_hdr.contents != NULL)
			{
				contents = elf_section_data(sec)->this_hdr.contents;
			}
			/* Go get them off disk.  */
			else if (!bfd_malloc_and_get_section(abfd, sec, &contents))
			{
				goto error_return;
			}
		}

		/* Read this BFD's local symbols if we haven't done so already.  */
		if ((symbuf == NULL) && (symtab_hdr->sh_info != 0))
		{
			symbuf = (Elf_Internal_Sym *)symtab_hdr->contents;

			if (symbuf == NULL)
			{
				symbuf = bfd_elf_get_elf_syms(abfd, symtab_hdr,
					symtab_hdr->sh_info, 0, NULL, NULL, NULL);
			}
			if (symbuf == NULL)
			{
				goto error_return;
			}
		}

		/* Get the value of the symbol referred to by the reloc. */
		if (r_sym < symtab_hdr->sh_info)
		{
			/* A local symbol.  */
			Elf_Internal_Sym *sym;
			asection *sym_sec;

			sym = symbuf + r_sym;

			if (sym->st_shndx == SHN_UNDEF)
			{
				sym_sec = bfd_und_section_ptr;
			}
			else if (sym->st_shndx == SHN_ABS)
			{
				sym_sec = bfd_abs_section_ptr;
			}
			else if (sym->st_shndx == SHN_COMMON)
			{
				sym_sec = bfd_com_section_ptr;
			}
			else
			{
				sym_sec = bfd_section_from_elf_index(abfd, sym->st_shndx);
			}

			symval = (sym->st_value + sym_sec->output_section->vma
				+ sym_sec->output_offset);
		}
		else
		{
			unsigned long indx;
			struct elf_link_hash_entry *h;

			/* An external symbol.  */
			indx = r_sym - symtab_hdr->sh_info;
			h = elf_sym_hashes(abfd)[indx];
			BFD_ASSERT(h != NULL);

			if ((h->root.type != bfd_link_hash_defined)
				&& (h->root.type != bfd_link_hash_defweak))
			{
				/* This appears to be a reference to an undefined symbol.
				 * Just ignore it--it will be caught by the regular reloc
				 * processing.  */
				continue;
			}

			symval = (h->root.u.def.value
				+ h->root.u.def.section->output_section->vma
				+ h->root.u.def.section->output_offset);
		}

		/* For simplicity of coding, we are going to modify the section
		 * contents, the section relocs, and the BFD symbol table.  We must
		 * tell the rest of the code not to free up this information.  It
		 * would be possible to instead create a table of changes which
		 * have to be made, as is done in coff-mips.c; that would be more
		 * work, but would require less memory when the linker is run.  */

		/* Try to turn a 32-bit relative branch into a 20-bit relative
		* branch. */
		if (r_type == (int)R_VOLT32_20_PCREL)
		{
			bfd_vma value = symval;

			/* Deal with pc-relative gunk. */
			/* TODO:  See if this actually works. */
			value -= (sec->output_section->vma + sec->output_offset);
			value -= rel->r_offset;
			value += rel->r_addend;


			/* See if the value will fit into 20 bits.  Note that the high
			 * value is 0xfffc + 4 as the target will be four bytes closer
			 * if we are able to relax. */
			struct 
			{
				int32_t value: 20;
				int32_t padding: 12;
			} val_struct;
			val_struct.value = value;
			//if (((int32_t)value > -0x100004) && ((int32_t)value < 0x100000))
			if (val_struct.value == value)
			{
				uint64_t code = bfd_get_64(abfd, contents + rel->offset);

				/* This will change things, so we should relax again.  Note
				 * that this is not required, and it may be slow.  However,
				 * it may produce smaller and faster code. */ 
				*again = TRUE;
			}
		}

		/* Try to turn a 32-bit immediate into 16-bit or 20-bit. */
		else if (r_type == (int)R_VOLT32_32)
		{
		}
	}
}

#define ELF_ARCH							bfd_arch_volt32
#define ELF_MACHINE_CODE					EM_VOLT32_UNOFFICIAL
#define ELF_MAXPAGESIZE						0x1

#define TARGET_BIG_SYM						volt32_elf32_vec
#define TARGET_BIG_NAME						"elf32-volt32"

#define elf_info_to_howto_rel				NULL
#define elf_info_to_howto					volt32_info_to_howto_rela
#define elf_backend_relocate_section		volt32_elf_relocate_section
#define elf_backend_gc_mark_hook			volt32_elf_gc_mark_hook
#define elf_backend_check_relocs			volt32_elf_check_relocs

#define elf_backend_can_gc_sections			1
#define elf_backend_rela_normal				1

#define bfd_elf32_bfd_relax_section			volt32_bfd_relax_section

#define bfd_elf32_bfd_reloc_type_lookup		volt32_reloc_type_lookup
#define bfd_elf32_bfd_reloc_name_lookup		volt32_reloc_name_lookup

#include "elf32-target.h"
