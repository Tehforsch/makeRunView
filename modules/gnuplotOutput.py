import tools
from dependency import Dependency
def check(f, lines):
    if f.fileType != "gpi":
        return None
    dependencies = []
    start = f.fname
    targets = []
    for l in lines:
        if "set output" in l:
            if l.count("\"") == 2:
                targets.append(tools.charactersBetween(l, "\"", "\""))
            elif l.count("\'") == 2:
                targets.append(tools.charactersBetween(l, "\'", "\'"))
            else:
                logging.info("Dangerous gnuplot output line, not adding dependency:")
                logging.info(l)
    if len(targets) == 0:
        return None
    return Dependency(starts = start, targets = targets, command = "gnuplot", printOutput = True)
