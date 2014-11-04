import tools
from dependency import Dependency
def check(f, lines):
    if f.fileType != "tex":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if "input" in l:
            filename = tools.charactersBetween(l, "{", "}")
            starts.append(filename + ".tex")
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, command = "pdflatex -interaction=nonstopmode -shell-escape", runCommandOnStartFile = False, printOutput = False)
