from os.path import expanduser
fileTypesToWatch = ["hs", "gpi", "py", "tex", "sh", "dat", "png", "jpg", "bib", "svg", "pdf", "pmf", "java", "xml", "jar"]
fileTypesToCheckImplicitDependencies = ["hs", "gpi", "py", "tex", "sh", "pmf", "java", "xml"]

safetyTime = 0.3

globalPath = "{home}/projects/makeRunView/modules/".format(home=expanduser("~"))
projectSubfolder = ".makeRunView/"
explicitDependenciesFilename = "explicit"

latexCommand = "pdflatex -interaction=nonstopmode -shell-escape"
latexOutputFormat = "pdf"

pythonCommand = "python3.4"
pythonMainFile = "main.py"

haskellCommand = "runghc"

runJarCommand = "java -jar"

startFilePlaceholder = "%s"
targetFilePlaceholder = "%t"

explicitFileSeparator = "->"
