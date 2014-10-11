configurationFileName = ".mrvConf"

fileTypesToWatch = [".gpi", ".py", ".tex", ".sh", ".dat"]
fileTypesToCheckImplicitDependencies = [".gpi", ".py", ".tex", ".sh"]
fileTypesToCheckExplicitDependencies = [".gpi", ".py", ".tex"]

targetString = "writes"
startString = "needs"

fileListSeparator = ","

gnuplotFileType = ".gpi"
latexFileType = ".tex"
dviFileType = ".dvi"
pythonFileType = ".py"
bashFileType = ".sh"

safetyTime = 0.3

commentStrings = {}
commentStrings[gnuplotFileType] = "#"
commentStrings[latexFileType] = "%"
commentStrings[pythonFileType] = "#"
commentStrings[bashFileType] = "#"

latexCommand = "pdflatex -shell-espace -interaction=nonstopmode"

globalPath = "/home/toni/Projects/makeRunView/modules/"
localPathName = ".modules"
