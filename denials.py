# Copyright (C) 2019 baalajimaestro
# Copyright (C) 2020-2021 Giovix92

import argparse
import getopt, re
import os, sys, shutil


version = "v1.3"
wfixes = []
write = False
namefile = "fixes.txt"
inputfile = "denials.txt"
logname = None

print(f"Giovix92's SELinux denial fixer, {version}.")

if os.path.exists("sepolicy"):
    shutil.rmtree("sepolicy")

if os.path.exists("denials.txt"):
    os.remove("denials.txt")
    
if os.path.exists("fixes.txt"):
    os.remove("fixes.txt")

parser = argparse.ArgumentParser(description="Generate Fixes for your SELinux Denials.", prog="denials.py")
group = parser.add_mutually_exclusive_group()
parser.add_argument("-v", "--verbose", action='store_true',
    help="Enable verbose mode: outputs every denial into its respective file.")
parser.add_argument("-c", "--cleanup", action='store_true',
    help="Cleans up the working directory.")
group.add_argument("-l", "--logcat", default="logcat.txt", metavar="logcat_name", nargs='?',
    help="Uses a custom logcat file instead of the logcat.txt default file.")
group.add_argument("-d", "--dmesg", default="dmesg.txt", metavar="dmesg_name", nargs='?',
    help="Uses a custom dmesg file instead of the dmesg.txt default file.")
args = parser.parse_args()

if args.cleanup:
    print("Cleaned up!")
    sys.exit()

if args.verbose:
    write = True
    os.makedirs("sepolicy")
    print("Verbose mode enabled!")
    print("Outputting every denial into its respective file.")

if args.dmesg is None or args.dmesg != "dmesg.txt":
    print("Parsing denials from dmesg!")
    logname = args.dmesg
    if args.dmesg is None:
        logname = "dmesg.txt"
    print(f"Using dmesg: {logname}")
    if not os.path.isfile(logname):
        print("Dmesg file is missing! Exiting.")
        sys.exit()
    os.system('cat %s | grep "avc: denied" > denials.txt' % logname)

if args.logcat is None or logname is None:
    print("Parsing denials from logcat!")
    logname = args.logcat
    if args.logcat is None:
        logname = "logcat.txt"
    print(f"Using logcat: {logname}")
    if not os.path.isfile(logname):
        print("Logcat file is missing! Exiting.")
        sys.exit()
    os.system('cat %s | grep "avc: denied" > denials.txt' % logname)

if not os.path.isfile(inputfile):
	print("Denials file is missing! Exiting.")
	sys.exit()

with open(inputfile) as denfile:
    data = denfile.read()
data = data.split("\n")
data.remove(data[-1])

# Parsin' the data
for i in data:
    test = re.search("{",i)
    test2 = re.search("}",i)
    se_context = i[test.span()[0]:test2.span()[0]+1]
    test = re.search("scontext",i)
    scontext = i[(test.span()[0]):].split(":")[2]
    test = re.search("tcontext",i)
    tcontext = i[(test.span()[0]):].split(":")[2]
    test = re.search("tclass",i)
    tclass = i[(test.span()[0]):].split("=")[1].split(" ")[0]
    if scontext == tcontext:
        tcontext="self"
    fix = f"allow {scontext} {tcontext}:{tclass} {se_context};\n"
    if tclass == "binder" and "call" in se_context or "transfer" in se_context:
        fix = f"binder_call({scontext}, {tcontext})\n"
    wfixes.append(fix)

wfixes = list(dict.fromkeys(wfixes))
for i in wfixes:
    tempvar = i.split(" ")
    if write:
        namefile = "sepolicy/" + tempvar[1] + ".te"
    if not os.path.exists(namefile):
        tmp = open(namefile, "w+")
        tmp.close()
    with open(namefile, "a") as ffnew:
        ffnew.write(i)
