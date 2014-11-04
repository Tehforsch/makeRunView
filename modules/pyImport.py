import tools
from dependency import Dependency
def check(f, lines):
    if f.fileType != "py":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if "import" in l:
            start = None
            if "from" in l:
                start = tools.charactersBetween(l, " ", " ")
            else:
                start = l[l.index(" ")+1:]
            start = start.replace(".", "/") # Python uses . to denote submodules which are folders
            start = start.replace("\n", "")
            start = start + ".py"
            starts.append(start)
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, command = "python3", runCommandOnStartFile = False)
