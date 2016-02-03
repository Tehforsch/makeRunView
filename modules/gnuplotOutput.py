from makeRunView import tools
from makeRunView.dependency import Dependency
def check(f, lines):
    if f.fileType != "gpi":
        return None
    dependencies = []
    start = f.fname
    targets = []
    for l in lines:
        if "set output" in l:
            outputFile = tools.getString(l)
            # This occurs with lines like 'set output pic'.x.'.gpi' which sets outputfiles dynamically (should happen very rarely). Just ignore it
            if outputFile == None:
                continue
            targets.append(outputFile)
    if len(targets) == 0:
        return None
    return Dependency(starts = start, targets = targets, command = "gnuplot", printOutput = True)
