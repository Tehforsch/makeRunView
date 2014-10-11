import logging
import os, sys
import tools
import makeRunView
import time
import config

# Configure logs
logging.basicConfig(level=logging.INFO, format='%(message)s')
 
def run(mrv, workPath):
    os.chdir(workPath)
    run = 0
    try:
        while True:
            run += 1
            time.sleep(0.1)
            mrv.handle()
            # Pollute so shit hits the fan
            # if run == 5:
                # os.system("touch plot.gpi")
    except (KeyboardInterrupt, SystemExit, Exception, AttributeError) as ex:
        # Kill threads at least
        mrv.obs.kill()
        logging.exception("Program died. Killed observer thread")
        sys.exit(0)

def readArgsAndRun():
    args = list(filter(lambda x : "-" not in x, sys.argv))
    parameters = list(map(lambda x : x.replace("-", ""), filter(lambda x : "-" in x, sys.argv)))

    if len(args) == 1:
        folder = "."
    elif len(args) == 2:
        folder = args[1]

    workPath = os.path.abspath(folder)
    mrv = makeRunView.MakeRunView(workPath)

    logging.info("Running makeRunView on " + workPath)

    run(mrv, workPath)

readArgsAndRun()
