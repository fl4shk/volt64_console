#!/usr/bin/env python3

from bitwise_stuff import *
from misc_util import *

GT_VEC_WIDTH = 4
case_vec = [["-" for i in range(GT_VEC_WIDTH)]
	for j in range(GT_VEC_WIDTH)]

for i in range(len(case_vec)):
	case_vec[i][i] = "1"
	for j in range(i + 1, len(case_vec)):
		case_vec[i][j] = "0"

print(case_vec)
