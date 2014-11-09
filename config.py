fileTypesToWatch = ["gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf"]
fileTypesToCheckImplicitDependencies = ["gpi", "py", "tex", "sh"]

# targetString = "writes"
# startString = "needs"
# fileListSeparator = ","

# gnuplotFileType = ".gpi"
# latexFileType = ".tex"
# dviFileType = ".dvi"
# pythonFileType = ".py"
# bashFileType = ".sh"


# commentStrings = {}
# commentStrings[gnuplotFileType] = "#"
# commentStrings[latexFileType] = "%"
# commentStrings[pythonFileType] = "#"
# commentStrings[bashFileType] = "#"

safetyTime = 0.3

globalPath = "/home/toni/Projects/makeRunView/modules/"
moduleFolderName = ".modules"

latexCommand = "pdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"
