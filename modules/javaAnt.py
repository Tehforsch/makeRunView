from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "java":
        return None
    dependencies = []
    start = f.fname
    # We don't know how where the build.xml lies with respect to this file. Assume that
    # this file is in ./src/subpackage1/subpackage2/.../ where . is the project root where
    # build.xml is. Use the amount of dots in the first package statement of the file to determine
    # the path. THIS IS TERRIBLE BUT IT WORKS
    packageLines = [line for line in lines if "package" in line]
    assert(len(packageLines) == 1)
    numSubDirectories = packageLines[0].count(".") + 1
    target = "../" * numSubDirectories + "build.xml"
    return Dependency(starts = start, targets = target, command = "ant compile -S -q && ant jar -S -q && ant run", runCommandOnStartFile = False, doNotAppendFilenameToCommand = True)
