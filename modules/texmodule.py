import tools
from dependency import Dependency
def check(mrv, f, lines):
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
    return Dependency(mrv = mrv, originFile = f, starts = starts, targets = target, command = "pdflatex -interaction=nonstopmode -shell-escape", runCommandOnStartFile = False, printOutput = False)
