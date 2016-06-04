from makeRunView import tools
from makeRunView.dependency import Dependency
from makeRunView import config
import os

def check(f, lines):
    if f.fileType != "py":
        return None
    if os.path.split(f.fname)[1] != config.pythonMainFile:
        return None
    dependencies = []
    start = f.fname
    target = "terminalOutputThisIsAnnoying"
    return Dependency(starts = start, targets = target, command = config.haskellCommand + " " + config.startFilePlaceholder, runInStartFolder = True)
