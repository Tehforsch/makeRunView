import subprocess, os, config, logging

def cleanFilename(fname):
    fname = fname.strip()
    fname = fname.replace("\"", "")
    return fname

def readFile(fname):
    """Return a list containing all lines in the file fname"""
    """Returns the lines contained in fname in standard list format"""
    f = open(fname, "r")
    lines = f.readlines()
    f.close()
    return lines

def writeFile(fname, content):
    """Writes the content into a file of path fname"""
    f = open(fname, "w")
    f.write(content)
    f.close()

def charactersBetween(string, start, end, startIndex=0):
    """Returns all characters in a string that are contained between the 
    first two occurences of start and end, starting at index startIndex"""
    startIndex = string.find(start, startIndex) + len(start)
    endIndex = string.find(end, startIndex)
    if startIndex == -1 or endIndex == -1:
        return None
    return string[startIndex:endIndex]

def getFileType(fname):
    """Extracts the file ending of file name by returning everything after the first point (not including the point)"""
    ending = os.path.splitext(fname)[1]
    if ending == "":
        return None
    return ending.replace(".", "")

def getFilePath(fname):
    """Extracts the file path of path + file name"""
    return os.path.split(fname)[0] + "/"

def getFileName(fname):
    """Extracts the file name of path + file name"""
    return os.path.split(fname)[1]

def mergePaths(relPath1, relPath2):
    """Merge the two paths which point and convert them to a standard absolute path
    (deleting .. links etc)"""
    return os.path.abspath(os.path.join(os.path.dirname(relPath1), relPath2))

def ensureAbsPath(fileName, path):
    """Check if fileName is not yet absolute. If this is true merge the filename with path to make it absolute."""
    if fileName[0] != "/":
        return mergePaths(path, fileName)
    return fileName
        
def isComment(line, fileType):
    """Use cofig.commentStrings to determine if a line in a file of type fileType is a comment"""
    whitespace = [" ", "\t"]
    if fileType not in config.commentStrings.keys():
        return False
    else:
        commentString = config.commentStrings[fileType]
    for z in line:
        if z in whitespace:
            pass
        elif z == commentString:
            return True
        else:
            return False
    return False

def ensureList(maybeList):
    if maybeList == None:
        return []
    if type(maybeList) != list:
        return [maybeList]
    return maybeList

def executeExactCommand(workFolder, command):
    """Run a command system command and return the output. Change to the workfolder afterwards. """
    out, err = runCommand(command)
    # Change back for safety
    os.chdir(workFolder)
    return out + err

def executeStandardCommand(workFolder, fname, command):
    """Execute the command on the file fname by switching into the path of fname, running the command
    and switching back to workFolder afterwards."""
    # cd into the directory 
    folder, filename = os.path.split(fname)
    os.chdir(folder)
    out, err = runCommand(command + " " + filename)
    # And then change back
    os.chdir(workFolder)
    return out + err

def runCommand(command):
    """Runs the system command and returns output and errors"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = p.communicate()
    return output, errors

def isGnuplotLatexFile(lines):
    if len(lines) > 0:
        if "GNUPLOT" in lines[0]:
            return True
    return False
