import numpy as np
import subprocess
import os
import config

def cleanFilename(fname):
    fname = fname.strip()
    fname = fname.replace("\"", "")
    return fname

def readFile(fname):
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

def readDataFile(fname, sep = " "):
    """Reads the file fname and returns a list of numpy arrays 
    where each array corresponds to a line in the file
    and each entry is separated by sep (default : " ")"""
    lines = readFile(fname)
    data = []
    for l in lines:
        splitted = l.replace("\n", "").split(sep)
        data.append(list(map(float, splitted)))
    return list(map(np.array, data))

def writeDataFile(fname, data, sep = " "):
    """Writes the data to the file fname, separating each list with
    a line break and each entry with sep (default " ")"""
    strData = map(lambda x : map(str, x), data)
    s = "\n".join(map(sep.join, strData))
    writeFile(fname, s)

def charactersBetween(string, start, end, startIndex=0):
    """Returns all characters in a string that are contained between the 
    first two occurences of start and end, starting at index startIndex"""
    startIndex = string.find(start, startIndex) + len(start)
    endIndex = string.find(end, startIndex)
    if startIndex == -1 or endIndex == -1:
        return None
    return string[startIndex:endIndex]

def getFileType(fname):
    """Extracts the file ending of file name by returning everything after the first point (including the point)"""
    return os.path.splitext(fname)[1]

def getFileName(fname):
    """Extracts the file name of path + file name by returning"""
    return os.path.split(fname)[1]

def mergePaths(relPath1, relPath2):
    """Merge the two paths which point and convert them to a standard relative path
    (deleting .. links etc)"""
    return os.path.abspath(os.path.join(os.path.dirname(relPath1), relPath2))

def isComment(line, fileType):
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

def runCommand(command):
    """Runs the system command and returns output and errors"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = p.communicate()
    return output, errors

# def plotData(pairs):
#     """Uses pyplot to quickly plot a list of (x, y) pairs"""
#     xs = []
#     ys = []
#     for pair in pairs:
#         xs.append(pair[0])
#         ys.append(pair[1])
#     plot.plot(xs, ys, 'ro')
#     #plot.axis([0, 6, 0, 20])
#     plot.show()

def transpose(lst):
    """Returns the transposed (rectangular) list"""
    for i in range(len(lst)-1):
        assert(len(lst[i]) == len(lst[i+1]))
    return list(map(list, zip(*lst)))

