#!/usr/bin/env python3

from colorama import init, Fore, Style
from random import randrange, seed

import vars
import functions

init()

# result = 35;
# operation = "3 x 4 = 8"
# functions.read("Correct! " + operation)

for elapsed in range(12):
    print(elapsed, functions.get_bonus(elapsed))