fileTypesToWatch = ["gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf", "pmf", "java", "xml", "jar"]
fileTypesToCheckImplicitDependencies = ["gpi", "py", "tex", "sh", "pmf", "java", "xml"]

safetyTime = 0.3

globalPath = "/home/toni/projects/makeRunView/modules/"
projectSubfolder = ".makeRunView/"
explicitDependenciesFilename = "explicit"

latexCommand = "ppdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"

pythonCommand = "python3.4"

runJarCommand = "java -jar"

startFilePlaceholder = "%s"
targetFilePlaceholder = "%t"
