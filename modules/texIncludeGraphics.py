import tools
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
            if tools.getFileType(filename) is None:
                # Lets try png i dont want to check how the file could be named
                filename = filename + ".png"
            starts.append(filename)
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runCommandOnStartFile = False, printOutput = False)
