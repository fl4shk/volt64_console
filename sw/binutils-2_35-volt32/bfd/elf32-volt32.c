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
//#include "elf/volt32.h"

#define ELF_ARCH		bfd_arch_volt32
#define ELF_MACHINE_CODE	EM_VOLT32_UNOFFICIAL
#define ELF_MAXPAGESIZE		0x1

#define TARGET_BIG_SYM		volt32_elf32_vec
#define TARGET_BIG_NAME		"elf32-volt32"

//#define elf_info_to_howto_rel			NULL
//#define elf_info_to_howto			volt32_info_to_howto_rela
//#define elf_backend_relocate_section		volt32_elf_relocate_section
//#define elf_backend_gc_mark_hook		volt32_elf_gc_mark_hook
//#define elf_backend_check_relocs		volt32_elf_check_relocs
//
//#define elf_backend_can_gc_sections		1
//#define elf_backend_rela_normal			1
//
//#define bfd_elf32_bfd_reloc_type_lookup		volt32_reloc_type_lookup
//#define bfd_elf32_bfd_reloc_name_lookup		volt32_reloc_name_lookup

#define bfd_elf32_bfd_reloc_type_lookup bfd_default_reloc_type_lookup
#define bfd_elf32_bfd_reloc_name_lookup _bfd_norelocs_bfd_reloc_name_lookup
#define elf_info_to_howto _bfd_elf_no_info_to_howto

#include "elf32-target.h"
