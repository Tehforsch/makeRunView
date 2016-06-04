fileTypesToWatch = ["hs", "gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf", "pmf", "java", "xml", "jar"]
fileTypesToCheckImplicitDependencies = ["hs", "gpi", "py", "tex", "sh", "pmf", "java", "xml"]

safetyTime = 0.3

globalPath = "/home/toni/projects/makeRunView/modules/"
projectSubfolder = ".makeRunView/"
explicitDependenciesFilename = "explicit"

latexCommand = "pdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"

pythonCommand = "python3.4"

haskellCommand = "runghc"

runJarCommand = "java -jar"

startFilePlaceholder = "%s"
targetFilePlaceholder = "%t"

explicitFileSeparator = "->"
