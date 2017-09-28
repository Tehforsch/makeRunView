from makeRunView.dependency import Dependency
from makeRunView import tools, config
def check(f, lines):
    """Checks if the given tex file is one that will actually compile to a pdf. If it isn't, we probably don't want to run pdflatex on it either."""
    if f.fileType != "tex":
        return None
    if tools.isGnuplotLatexFile(lines):
        return None
    start = f.fname
    target = f.fname.replace(".tex","." + config.latexOutputFormat)
    for l in lines:
        if "\\begin{document}" in l:
            command = getCommand(start)
            return Dependency(starts=start, targets=target, command=command, runInStartFolder=True, printOutput=True)
    return None

def getCommand(start):
    assert ".tex" in start
    command = config.latexCommand + " " + config.startFilePlaceholder
    logFile = start.replace(".tex", ".log")
    command = command + "; cat {} | grep multiply".format(logFile)
    command = command + "; cat {} | grep undefined".format(logFile)
    return command
