import tools, config
from dependency import Dependency
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
            return Dependency(starts = start, targets = target, command = config.latexCommand, runCommandOnStartFile = True, printOutput = False)
    return None
