import config

def cleanFilename(fname):
    fname = fname.strip()
    fname = fname.replace("\"", "")
    return fname

def charactersBetween(string, start, end, startIndex=0):
    """Returns all characters in a string that are contained between the 
    first two occurences of start and end, starting at index startIndex"""
    startIndex = string.find(start, startIndex) + len(start)
    endIndex = string.find(end, startIndex)
    if startIndex == -1 or endIndex == -1:
        return None
    return string[startIndex:endIndex]

def isComment(line, fileType):
    """Use config.commentStrings to determine if a line in a file of type fileType is a comment"""
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
