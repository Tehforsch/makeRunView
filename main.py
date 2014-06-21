import logging
import os, sys
import tools
import makeRunView
import time

# Configure logs
#logging.basicConfig(filename='makeRunView.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

def cleanFilename(fname):
    fname = fname.strip()
    fname = fname.replace("\"", "")
    return fname

def readConfigFile(mrv, workPath, fname):
    lines = tools.readFile(fname)
    # Each line is a single dependency.
    dependencies = []
    for l in lines:
        f1, f2 = l.replace("\n","").split("->")
        f1 = cleanFilename(f1)
        f1 = os.path.join(workPath, f1)
        f2 = cleanFilename(f2)
        f2 = os.path.join(workPath, f2)
        mrv.addDependency(f1, f2)
    logging.info("Read config file. " + str(len(dependencies)) + " dependencies found.")
    return dependencies

def run(mrv, workPath):
    os.chdir(workPath)
    run = 0
    try:
        while True:
            run += 1
            time.sleep(0.1)
            mrv.handle()
            #Pollute so shit hits the fan
            #if run == 5:
                #os.system("touch plots/plot.gpi")
    except (KeyboardInterrupt, SystemExit, Exception) as ex:
        # Kill threads at least
        mrv.obs.kill()
        logging.exception("Program died. Killed observer thread")
        sys.exit(0)

def readArgsAndRun():
    configFile = None
    args = sys.argv
    if len(args) == 1:
        logging.info("No folder or config file given, assuming that . is the folder to work on and config file has to be created")
        folder = "."
    elif len(args) == 2:
        logging.info("No config file given, assuming that it has to be created")
        folder = args[1]
    else:
        folder = args[1]
        configFile = args[2]
    workPath = os.path.abspath(folder)
    mrv = makeRunView.MakeRunView(workPath)
    if configFile is not None:
        config = readConfigFile(mrv, workPath, os.path.join(workPath, configFile))
        logging.info("Running makeRunView on " + workPath + " with config " + configFile)
    else:
        config = None
        logging.info("Running makeRunView on " + workPath + " and creating config file")
    run(mrv, workPath)

readArgsAndRun()
