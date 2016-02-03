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
            if tools.numQuotes(l) > 2 or outputFile == None: # This occurs with lines like 'set output pic'.x.'.gpi' which sets outputfiles dynamically (should happen very rarely). Just ignore it
                continue
            targets.append(outputFile)
    if len(targets) == 0:
        return None
    return Dependency(starts = start, targets = targets, command = "gnuplot", printOutput = True)
