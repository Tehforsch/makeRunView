import os, ownUtils

def gnuplot(workFolder, fname):
    # We have to cd into the plot directory 
    folder, filename = os.path.split(fname)
    os.chdir(folder)
    out, err = ownUtils.runCommand("gnuplot " + filename)
    # And then change back
    os.chdir(workFolder)
    return out + err

def python(workFolder, fname):
    # We have to cd into the plot directory 
    folder, filename = os.path.split(fname)
    os.chdir(folder)
    out, err = ownUtils.runCommand("python3 " + filename)
    # And then change back
    os.chdir(workFolder)
    return out + err
