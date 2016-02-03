from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "xml":
        return None
    dependencies = []
    start = f.fname
    jarFileLines = [line for line in lines if "jar" in line and "destfile" in line]
    assert(len(jarFileLines) == 1)
    jarFileLine = jarFileLines[0]
    target = tools.getString(jarFileLine)
    return Dependency(starts = [start], targets = [target], command = "java -jar", runCommandOnStartFile = False)

