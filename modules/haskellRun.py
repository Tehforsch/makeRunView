from makeRunView import tools
from makeRunView.dependency import Dependency
from makeRunView import config

def check(f, lines):
    if f.fileType != "hs":
        return None
    dependencies = []
    start = f.fname
    target = "terminalOutputThisIsAnnoying"
    return Dependency(starts = start, targets = target, command = config.haskellCommand + " " + config.startFilePlaceholder, runInStartFolder = True)
