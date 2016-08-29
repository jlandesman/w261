#!/usr/bin/python
import sys
sum = 0
for line in sys.stdin.readlines():
    sum = sum + int(line)
print(sum)