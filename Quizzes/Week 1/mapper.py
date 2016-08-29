#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[2]
findword = sys.argv[1]

with open (filename, "r") as myfile:
    for line in myfile.readlines():
        words = line.lower().split()
        num_matches = [1 for x in words if x.strip('!@#$%^&*,?/.') == findword.lower()]
        count += sum(num_matches)

print(count)