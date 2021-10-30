#!/usr/bin/env python3

from misc_util import *
from nmigen import *

class Volt32GpuBus:
	def __init__(self):
		pass


class Volt32Gpu(Elaboratable):
	def __init__(self):
		self.__bus = Volt32GpuBus()
