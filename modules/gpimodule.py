import tools
from dependency import Dependency
def check(mrv, f, lines):
    dependencies = []
    start = f.fname
    targets = []
    for l in lines:
        if "set output" in l:
            targets.append(tools.charactersBetween(l, "\"", "\""))
    if len(targets) == 0:
        return None
    return Dependency(mrv = mrv, originFile = f, starts = start, targets = targets, command = "gnuplot", printOutput = True)
