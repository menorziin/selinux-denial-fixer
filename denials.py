# Copyright (C) 2019 baalajimaestro
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Save all denials line by line to denials.txt in the same folder as code
# Fixes are saved to fixes.txt

import re
import os
import sys, getopt
import shutil

wfixes = []
namefile = ""
inputfile = "denials.txt"

if not os.path.exists("sepolicy"):
    os.makedirs("sepolicy")
else:
    shutil.rmtree("sepolicy")
    os.makedirs("sepolicy")

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-v":
        write = True
        namefile = "verbose"
    elif sys.argv[i] == "-c":
        namefile = "sepolicy/" + sys.argv[i+1]
        write = False
    elif sys.argv[i] == "-i":
        inputfile = sys.argv[i+1]
    elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
        print("Usage: denials.py [-v] [-c custom_output_file] [-i custom_input_file]")
        sys.exit()

if namefile == "":
    namefile = "sepolicy/fixes.txt"
    write = False

with open(inputfile) as denfile:
    data=denfile.read()
data=data.split("\n")
data.remove(data[-1])
for i in data:
    test=re.search("{",i)
    test2=re.search("}",i)
    se_context=i[test.span()[0]:test2.span()[0]+1]
    test=re.search("scontext",i)
    scontext=i[(test.span()[0]):].split(":")[2]
    test=re.search("tcontext",i)
    tcontext=i[(test.span()[0]):].split(":")[2]
    test=re.search("tclass",i)
    tclass=i[(test.span()[0]):].split("=")[1].split(" ")[0]
    fix="allow "
    fix+=scontext
    fix+=" "
    if scontext == tcontext:
        tcontext="self"
    fix+=tcontext
    fix+=":"
    fix+=tclass
    fix+=" "
    fix+=se_context
    fix+=";"
    fix+="\n"
    wfixes.append(fix)
    if write:
        namefile="sepolicy/" + scontext + ".te"
    if not os.path.exists(namefile):
        os.mknod(namefile)
    with open (namefile, "a+") as ffnew:
        for line in wfixes:
            if line.strip("\n") == fix.strip("\n"):
                pass
        else:
            ffnew.write(fix)
