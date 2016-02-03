from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "py":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if not tools.isComment(l, "#") and "import " in l:
            start = None
            if "from" in l:
                start = tools.charactersBetween(l, " ", " ")
            else:
                start = l[l.index(" ")+1:]
            starts = start.split(",")
            starts = [start.replace(".", "/") for start in starts]
            starts = [start.strip() + ".py" for start in starts]
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, command = "python3", runCommandOnStartFile = False)
