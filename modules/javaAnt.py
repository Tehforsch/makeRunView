from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "xml":
        return None
    dependencies = []
    target = f.fname
    # 
    mainClassLines = [line for line in lines if "Main-Class" in line]
    srcFolderLines = [line for line in lines if "srcdir" in line]
    assert(len(mainClassLines) == 1)
    assert(len(srcFolderLines) == 1)
    mainClassLine = mainClassLines[0]
    srcFolderLine = srcFolderLines[0]
    assert("Main-Class" in mainClassLine)
    index = mainClassLine.index("Main-Class") + 11 # look behind the end string of "Main-Class"
    filename = getStringAfterIndex(mainClassLine, index)
    srcFolder = getStringAfterIndex(srcFolderLine, 0)
    start = tools.resolveJavaFilename(srcFolder, filename)
    if start == None:
        return None
    return Dependency(starts = start, targets = target, command = "ant compile -S -q && ant jar -S -q && ant run", runCommandOnStartFile = False, doNotAppendFilenameToCommand = True)

