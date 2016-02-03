from makeRunView import tools
from makeRunView.dependency import Dependency

def check(f, lines):
    if f.fileType != "java":
        return None
    dependencies = []
    target = f.fname
    # 
    # Find which package this file belongs to
    packageLines = [line for line in lines if "package" in line]
    assert(len(packageLines) == 1)
    package = getStatementTarget(packageLines[0])
    # Every import starts a dependency
    importLines = [line for line in lines if "import" in line]
    starts = []
    for line in importLines:
        for statement in line.split(";"):
            if not "import" in statement:
                continue
            importedFile = getStatementTarget(line + ";") # append the semicolon again since split strips it.
            starts.append(tools.getRelativeJavaPath(package, importedFile))
    if starts == []:
        return
    return Dependency(starts = starts, targets = target)

def getStatementTarget(statement):
    # for statements like "import java.util.Vector;" or "package main"
    # return "java.util.Vector" or "main" respectively.
    return tools.charactersBetween(statement, " ", ";").strip()
