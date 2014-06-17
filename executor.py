import os, ownUtils

def executeStandardCommand(workFolder, fname, command):
    # cd into the directory 
    folder, filename = os.path.split(fname)
    os.chdir(folder)
    out, err = ownUtils.runCommand(command + " " + filename)
    # And then change back
    os.chdir(workFolder)
    return out + err

def gnuplot(workFolder, fname):
    return executeStandardCommand(workFolder, fname, "gnuplot")

def python(workFolder, fname):
    return executeStandardCommand(workFolder, fname, "python")

def latex(workFolder, fname):
    return executeStandardCommand(workFolder, fname, "latex -interaction=nonstopmode")
