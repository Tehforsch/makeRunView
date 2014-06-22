import logging
import os, sys
import tools
import makeRunView
import time
import config

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
    except (KeyboardInterrupt, SystemExit, Exception, AttributeError) as ex:
        # Kill threads at least
        mrv.obs.kill()
        logging.exception("Program died. Killed observer thread")
        sys.exit(0)

def readArgsAndRun():
    configFile = None
    args = list(filter(lambda x : "-" not in x, sys.argv))
    parameters = list(filter(lambda x : "-" in x, sys.argv))

    if len(args) == 1:
        folder = "."
    elif len(args) == 2:
        folder = args[1]

    workPath = os.path.abspath(folder)
    mrv = makeRunView.MakeRunView(workPath)

    logging.info("Running makeRunView on " + workPath + " and looking for dependencies")

    if "-p" in parameters:
        # Replot all gpi files. Just a helper
        mrv.pollute(config.gnuplotFileType)

    run(mrv, workPath)

readArgsAndRun()
