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
    return resolveFilename(srcFolder, filename, ".java")

def resolvePythonFilename(srcFolder, filename):
    return resolveFilename(srcFolder, filename, ".py")

def resolveFilename(srcFolder, filename, ending):
    # The dots should just mean subpackages, i.e. subfolders, replace with slashes
    # Don't accidentally replace double dots too, so just move them to some temporary placeholder ... Sorry I'M TIRED
    filename = filename.replace("..", "####")
    filename = filename.replace(".", "/")
    filename = filename.replace("####", "..")
    return os.path.join(srcFolder, filename) + ending

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

def getRelativePythonPath(package, importedFile):
    # Return the path of the file given by importedFile relative to a file which is contained in package.
    # For example: if 
    # package = "main.foo.bar"
    # importedFile = "main.foo.baz.Main"
    # then the relative path should be "../baz/Main.java"
    # easy solution: go upwards to the src folder by using ../ for each subpackage in package
    # then convert importedFile to a path and append it.
    srcFolder = os.path.join("../" * (package.count(".")+1), package)
    return resolvePythonFilename(srcFolder, importedFile)

def getString(line, index=0):
    if "\"" in line:
        return charactersBetween(line, "\"", "\"", index)
    elif "'" in line:
        return charactersBetween(line, "'", "'", index)
    else:
        return None

def numQuotes(line, index=0):
    return line[index+1:].count("\"") + line[index+1:].count("'")

def beginsWith(line, string):
    # Does the line begin with string (except for whitespace?)
    if string in line and line.strip().index(string) == 0:
        return True
    return False

def isSuperDirectory(path1, path2):
    # Check whether path1 is above path2
    print( os.path.realpath(path1), os.path.realpath(path2))
