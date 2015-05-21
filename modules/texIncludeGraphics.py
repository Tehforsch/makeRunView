import os, logging
from makeRunView import tools
from makeRunView.utils import fileUtils
from makeRunView.dependency import Dependency
def check(f, lines):
    if f.fileType != "tex":
        return None
    if tools.isGnuplotLatexFile(lines):
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if "\\includegraphics" in l and "{" in l and "}" in l:
            filename = tools.charactersBetween(l, "{", "}")
            if fileUtils.getFileType(filename) is None or fileUtils.getFileType(filename) == "":
                possibleExtensions = [".png", ".bmp", ".gif", ".jpg", ".pdf"]
                possibleExtensions = possibleExtensions + [x.upper() for x in possibleExtensions]
                found = False
                for fileEnding in possibleExtensions:
                    if os.path.isfile(filename + fileEnding):
                        logging.info("Found a file named " + filename + fileEnding + ", will assume that this file is meant by")
                        logging.info(l.replace("\n", ""))
                        filename = filename + fileEnding
                        found = True
                        break
                if not found:
                    logging.info("Didn't find a file with this name, ignoring this dependency:" + str(l.replace("\n", "")))
            starts.append(filename)
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runCommandOnStartFile = False, printOutput = False)
