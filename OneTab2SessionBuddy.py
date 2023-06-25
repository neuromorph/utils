#!/usr/bin/env python
"""
Convert bookmarks exported from OneTab to SessionBuddy format to import in SessionBuddy.
python OneTab2SessionBuddy.py <path to OneTab file> <path to target SessionBuddy file>
"""
import sys

with open(sys.argv[1], 'r') as fOT,\
    open(sys.argv[2], 'w+') as fSB:
    
    lines = fOT.readlines()
    
    for l in lines:
        if l.strip():
            l2, l1 = l.split(" ",1)
            fSB.write(f'{l1}{l2}\n\n')
        



