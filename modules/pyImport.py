from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "py":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if (tools.beginsWith(l, "import ") or tools.beginsWith(l, "from ")) and not tools.isComment(l, "#") : 
            start = None
            if "from" in l:
                # Python has two different types of "from .. import .." statements:
                # importing objects from a single file i.e. "import object from file"
                # importing files from a package i.e. "import file from package"
                # unfortunately these are a little hard to differentiate so I 
                # will just give up. Use explicit dependencies if needed
                continue
            else:
                start = l[l.index(" ")+1:]
                starts = start.split(",")
                starts = [start.replace(".", "/") for start in starts]
                starts = [start.strip() + ".py" for start in starts]
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, command = "python3", runCommandOnStartFile = False)
