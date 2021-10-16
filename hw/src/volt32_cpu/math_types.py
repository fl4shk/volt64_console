#!/usr/bin/env python3

import math
from misc_util import *

from nmigen import *
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from nmigen.sim import Simulator, Delay, Tick

from enum import Enum, auto
#--------
class ArithShape(Enum):
	Unsigned = 0
	Signed = auto()
#--------
