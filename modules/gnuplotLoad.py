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
            if l.count("\"") == 2:
                starts.append(tools.charactersBetween(l, "\"", "\""))
            elif l.count("\'") == 2:
                starts.append(tools.charactersBetween(l, "\'", "\'"))
            else:
                # This occurs with lines like 'load template'.x.'.gpi' which load files dynamically (should happen very rarely). Just ignore it
                continue
    if len(starts) == 0:
        return None
    return Dependency(starts = starts, targets = target, runCommandOnStartFile = False, printOutput = False)
