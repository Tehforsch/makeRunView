configurationFileName = ".mrvConf"

fileTypesToWatch = [".gpi", ".py", ".tex", ".sh", ".dat"]
fileTypesToPrintOutput = [".gpi", ".py"]
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
