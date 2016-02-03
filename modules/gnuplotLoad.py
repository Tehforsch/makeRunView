from makeRunView import tools
from makeRunView.dependency import Dependency
def check(f, lines):
    if f.fileType != "gpi":
        return None
    dependencies = []
    starts = []
    target = f.fname
    for l in lines:
        if "load" in l:
            loadedFile = tools.getString(l)
            # This occurs with lines like 'load template'.x.'.gpi' which load files dynamically (should happen very rarely). Just ignore it
            if loadedFile == None:
                continue
            starts.append(loadedFile)
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runCommandOnStartFile = False, printOutput = False)
