import tools, os,logging
from dependency import Dependency
def check(f, lines):
    if f.fileType != "tex":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if "includegraphics" in l:
            filename = tools.charactersBetween(l, "{", "}")
            if tools.getFileType(filename) is None or tools.getFileType(filename) == "":
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
                    logging.info("Didn't find a file with this name, ignoring this dependency.")
            starts.append(filename)
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runCommandOnStartFile = False, printOutput = False)
