fileTypesToWatch = ["gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf", "pmf"]
fileTypesToCheckImplicitDependencies = ["gpi", "py", "tex", "sh", "pmf"]

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

globalPath = "/home/toni/projects/makeRunView/modules/"
projectSubfolder = ".makeRunView/"
explicitDependenciesFilename = "explicit"


latexCommand = "pdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"
