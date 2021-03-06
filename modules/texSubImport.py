from makeRunView import tools
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
        if "subimport" in l:
            path = tools.charactersBetween(l, "{", "}")
            fname = tools.charactersBetween(l, "{", "}", l.find(path))
            filename = path + fname
            starts.append(filename + ".tex")
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runInStartFolder = False, printOutput = False)
