import os
import sys

table = {}

def cache_initialize():
    global table

    for f in os.listdir("cache"):
        table[f] = True

def cache_lookup(rpm):
    return table.get(rpm, False)
