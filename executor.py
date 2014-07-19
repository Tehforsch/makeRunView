import os, tools

def executeStandardCommand(workFolder, fname, command):
    # cd into the directory 
    folder, filename = os.path.split(fname)
    os.chdir(folder)
    out, err = tools.runCommand(command + " " + filename)
    # And then change back
    os.chdir(workFolder)
    return out + err

def gnuplot(workFolder, start, targets):
    return executeStandardCommand(workFolder, start.fname, "gnuplot")

def python(workFolder, start, targets):
    return executeStandardCommand(workFolder, start.fname, "python")

def latex(workFolder, start, targets):
    s1 = executeStandardCommand(workFolder, start.fname, "latex -interaction=nonstopmode")
    #s2 = executeStandardCommand(workFolder, start.fname, "bibtex")
    #s3 = executeStandardCommand(workFolder, start.fname, "latex -interaction=nonstopmode")
    return s1

def emptyFunction(workFolder, start, targets):
    # Needed for dependencies that don't need to be resolved
    return ""
