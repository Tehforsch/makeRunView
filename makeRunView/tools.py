import os
from makeRunView import config

def cleanFilename(fname):
    fname = fname.strip()
    fname = fname.replace("\"", "")
    return fname

def charactersBetween(string, start, end, startIndex=0):
    """Returns all characters in a string that are contained between the 
    first occurences of start and end, starting at index startIndex"""
    startIndex = string.find(start, startIndex)
    if startIndex == -1:
        return None
    startIndex = startIndex + len(start)
    endIndex = string.find(end, startIndex)
    if endIndex == -1:
        return None
    return string[startIndex:endIndex]

def isCommentInFile(line, fileType):
    """Use config.commentStrings to determine if a line in a file of type fileType is a comment"""
    if fileType not in config.commentStrings:
        return False # No comment string defined for this filetype
    commentString = config.commentStrings[fileType]
    return isComment(line, commentString)

def isComment(line, commentString):
    whitespace = [" ", "\t"]
    if commentString in line:
        everythingBeforeComment = line[:line.index(commentString)]
        return set(everythingBeforeComment).issubset(whitespace)
    return False

def isGnuplotLatexFile(lines):
    if len(lines) > 0:
        if "GNUPLOT" in lines[0]:
            return True
    return False

def ensureList(maybeList):
    if maybeList == None:
        return []
    if type(maybeList) != list:
        return [maybeList]
    return maybeList

def resolveJavaFilename(srcFolder, filename):
    # The dots should just mean subpackages, i.e. subfolders, replace with slashes
    filename = filename.replace(".", "/")
    return os.path.join(srcFolder, filename) + ".java"

def getRelativeJavaPath(package, importedFile):
    # Return the path of the file given by importedFile relative to a file which is contained in package.
    # For example: if 
    # package = "main.foo.bar"
    # importedFile = "main.foo.baz.Main"
    # then the relative path should be "../baz/Main.java"
    # easy solution: go upwards to the src folder by using ../ for each subpackage in package
    # then convert importedFile to a path and append it.
    srcFolder = "../" * (package.count(".")+1)
    return resolveJavaFilename(srcFolder, importedFile)
