from makeRunView import tools
from makeRunView.dependency import Dependency
from makeRunView import config

def check(f, lines):
    if f.fileType != "xml":
        return None
    dependencies = []
    start = f.fname
    jarFileLines = [line for line in lines if "jar" in line and "destfile" in line]
    assert(len(jarFileLines) == 1)
    jarFileLine = jarFileLines[0]
    target = tools.getString(jarFileLine)
    return Dependency(starts = [start], targets = [target], command = config.runJarCommand + " " + config.targetFilePlaceholder, runInStartFolder = False)

