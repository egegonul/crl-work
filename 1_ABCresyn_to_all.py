#!/usr/bin/env python3

import os
import subprocess


inDir = "0_sanitized"
outDir = "1_minimized"
allFileList = os.listdir(inDir)

fileList = []
for name in allFileList:
    # skip hidden files
    if name.startswith("."):
        continue
    # take verilog files
    if name.endswith(".v"):
        fileList.append(name)
os.mkdir(outDir)
# convert all the files
for fileName in fileList:
    # Initialize the list of arguments to call ABC with
    abcArgs = ["../../abc/abc", "-q read_verilog {0}/{1}"
               .format(inDir, fileName)]
    abcArgs.append("-q resyn")
    abcArgs.append("-q write_verilog {0}/{1}_min.v"
                   .format(outDir, fileName.split(".")[0]))
    # Create a Popen object with the ABC arguments and redirect
    # the stdout and stderr to the PIPE. This way we can write ABC's
    # output to a variable instead that to the stdout/stderr
    abc = subprocess.Popen(abcArgs, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    # Run ABC and save its output and error data
    abcOutput, abcError = abc.communicate()
    # If the output data is not empty
    if abcOutput:
        # Print it
        print("ABC says:")
        print("%s" % abcOutput.decode().strip())
        print("")
    # If the error data is not empty
    if abcError:
        # Print it
        print("ABC returned an error while working on '%s' "
              % fileName)
        print("ABC says:")
        print("%s" % abcError.decode().strip())
        print("")
