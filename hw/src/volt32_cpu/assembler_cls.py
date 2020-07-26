#!/usr/bin/env python3

from misc_util import *

from enum import Enum, auto

from volt32_cpu.asm_misc import *

class Volt32CpuAssembler:
	def __init__(self, instr_list):
		self.__instr_list = instr_list

	def run(self):
		pass
