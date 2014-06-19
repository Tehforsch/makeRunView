import logging, os, config, executor
import os, sys
path = os.path.abspath("/home/toni/.usrconfig/python/")
sys.path.append(path)
import ownUtils

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

def createDependencies(mrv, fileStates):
    for f in fileStates:
        # Check file for references of output files (like set output "../test.eps") so a dependency can be created
        if f.fileType == config.gnuplotFileType:
            targets = getGnuplotTargets(f)
        elif f.fileType == config.latexFileType:
            targets = getLatexTargets(f)
        elif f.fileType == config.pythonFileType:
            targets = getPythonTargets(f)
        else:
            continue
        if targets != []:
            mrv.addDependency(f.fname, targets)
    for f in fileStates:
        # Check file for references of imported files (like \subimport{../pics/}{test.eps})
        if f.fileType == config.latexFileType:
            # Latex files may include pictures (or tex files) so a dependency has to be created
            # but we don't want to execute latex texFile on them but instead we need to tell the
            # system that the file that imported the other one is now polluted
            # down the tree such that the final file gets cleaned by executing latex)
            starts = getLatexStarts(f)
            function = executor.emptyFunction
        else:
            starts = []
            function = None
        for start in starts:
            mrv.addDependency(start, [f.fname], function)

def getGnuplotTargets(f):
    assert(f.fileType == config.gnuplotFileType)
    # Check the gnuplot script for output files
    targets = []
    lines = f.readlines()
    for line in lines:
        if "set output" in line:
            if "\"" in line:
                quoteType = "\""
            elif "\'" in line:
                quoteType = "\'"
            if line.count(quoteType) > 2:
                logging.warning("Probably dynamic output set in plotfile: " + f.fname, ". Skipping outputfile. Resolve by adding dependency manually.")
                continue
            outputFile = ownUtils.charactersBetween(line, quoteType, quoteType)
            if outputFile is None:
                continue
            if outputFile[0] != "/":
                # Relative path.  Join relative path with filename of plot script
                fullPath = mergePaths(f.fname, outputFile)
            else:
                # Absolute path. Just accept it as it is.
                logging.warning("Absolute path in plot file? This may not behave properly.")
                fullPath = outputFile
            targets.append(fullPath)
    return targets

def getPythonTargets(f):
    return []

def getLatexTargets(f):
    lines = f.readlines()
    if lines is None:
        return []
    if isGnuplotLatexFile(lines):
        return []
    return [f.fname.replace(config.latexFileType, config.dviFileType)]

def getLatexStarts(f):
    lines = f.readlines()
    if lines is None:
        return []
    # Check if this tex file is the output of gnuplot
    if isGnuplotLatexFile(lines):
        return []
    starts = []
    for l in lines:
        if "subimport" in l:
            # String has the form \subimport{path}{file}
            # First find the path:
            path = ownUtils.charactersBetween(l, "{", "}")
            # Now search for the file by starting the search where the path begins, which ignores the first {
            fname = ownUtils.charactersBetween(l, "{", "}", l.find(path))
            if path is not None and fname is not None:
                starts.append(mergePaths(f.fname, os.path.join(path, fname)) + config.latexFileType)
    return starts
    
def isGnuplotLatexFile(lines):
    return "GNUPLOT" in lines[0]

def mergePaths(relPath1, relPath2):
    """Merge the two paths which point and convert them to a standard relative path
    (deleting .. links etc)"""
    return os.path.abspath(os.path.join(os.path.dirname(relPath1), relPath2))
