# Copyright (C) 2019 baalajimaestro
# Copyright (C) 2020-2021 Giovix92

import re
import os
import sys, getopt
import shutil

version = "v1.0"
wfixes = []
namefile = ""
inputfile = "denials.txt"

if not os.path.exists("sepolicy"):
    os.makedirs("sepolicy")
else:
    shutil.rmtree("sepolicy")
    os.makedirs("sepolicy")

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
        write = True
        namefile = "verbose"
        print("Verbose mode enabled!")
        print("Outputting every denial into its respective file.")
    elif sys.argv[i] == "-o" or sys.argv[i] == "--custom-output":
        try:
            if not "-" in sys.argv[i+1]:
                namefile = "sepolicy/" + sys.argv[i+1]
                write = False
            else:
            	sys.exit()
        except:
            print("No filename specified. Exiting.")
            sys.exit()
    elif sys.argv[i] == "-i" or sys.argv[i] == "--custom-input":
        try:
            if os.path.isfile(sys.argv[i+1]):
                inputfile = sys.argv[i+1]
            else:
            	sys.exit()
        except:
            print("The specified filename doesn't exist. Exiting.")
            sys.exit()
    elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
    	print("Giovix92's SELinux denial fixer,", version)
    	print("Usage: denials.py [-v] [-c custom_output_file] [-i custom_input_file]")
    	sys.exit()

if namefile == "":
    namefile = "sepolicy/fixes.txt"
    write = False

if not os.path.isfile("denials.txt") and not os.path.isfile(inputfile):
	print("denials.txt is missing! Exiting.")
	sys.exit()

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
