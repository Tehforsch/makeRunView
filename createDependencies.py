import logging, os, config
import os, sys
path = os.path.abspath("/home/toni/.usrconfig/python/")
sys.path.append(path)
import ownUtils

class FileState:
    def __init__(self, fname):
        self.fname = fname
        self.successors = []
        self.predecessors = []
        self.fileType = ownUtils.getFileType(fname)
        self.polluted = []
    
    def readlines(self):
        f = open(self.fname, "r")
        lines = f.readlines()
        f.close()
        return lines

def scanForFiles(currentFolder,fileStates):
    logging.debug("RUN " + currentFolder)
    for thing in os.listdir(currentFolder):
        fullPathToThing = os.path.join(currentFolder, thing)
        logging.debug("CHK " + fullPathToThing)
        if os.path.isdir(fullPathToThing):
            scanForFiles(os.path.join(currentFolder, thing), fileStates)
        elif os.path.isfile(fullPathToThing):
            logging.debug("ADD " + fullPathToThing)
            fileStates.append(FileState(fullPathToThing))
        else:
            logging.error("OH MY GOD ITS THE THING, CALL JOHN CARPENTER")
    return fileStates

def createDependencies(filenames):
    dependencies = []
    for f in filenames:
        if f.fileType == config.gnuplotFileType:
            dependencies += createGnuplotDependencies(f)
    print (dependencies)

def createGnuplotDependencies(f):
    assert(f.fileType == config.gnuplotFileType)
    # Check the gnuplot script for output files
    dependencies = []
    lines = f.readlines()
    for line in lines:
        if "set output" in line:
            if "\"" in line:
                quoteType = "\""
            elif "\'" in line:
                quoteType = "\'"
            if line.count(quoteType) > 2:
                logging.warning("Probably dynamic output set in plotfile: " + f.fname, ". Skipping outputfile. Resolve by adding dependency manually.")
            outputFile = ownUtils.charactersBetween(line, quoteType, quoteType)
            if outputFile[0] != "/":
                # Relative path.
                # Join relative path with filename of plot script
                fullPath = os.path.relpath(os.path.join(os.path.dirname(f.fname), outputFile))
            else:
                fullPath = outputFile
            dependencies.append((f.fname, fullPath))
    return dependencies


files = (scanForFiles("example", []))
print(createDependencies(files))
