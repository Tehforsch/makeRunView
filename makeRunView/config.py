fileTypesToWatch = ["gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf", "pmf", "java", "xml", "jar"]
fileTypesToCheckImplicitDependencies = ["gpi", "py", "tex", "sh", "pmf", "java", "xml"]

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


latexCommand = "ppdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"
