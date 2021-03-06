import logging, os, sys, time
from makeRunView import makerunview

def run(mrv, workPath):
    os.chdir(workPath)
    run = 0
    try:
        while True:
            run += 1
            time.sleep(0.1)
            mrv.handle()
    except (KeyboardInterrupt, SystemExit, Exception, AttributeError) as ex:
        # Kill threads at least
        mrv.obs.kill()
        logging.exception("Program died. Killed observer thread")
        sys.exit(0)

def readArgsAndRun():
    args = list(filter(lambda x : "-" not in x, sys.argv))
    parameters = list(map(lambda x : x.replace("-", ""), filter(lambda x : "-" in x, sys.argv)))

    if "vv" in parameters:
        level = logging.DEBUG
    elif "v" in parameters:
        level = logging.INFO
    else:
        level = logging.WARNING
    # Configure logs
    logging.basicConfig(level=level, format='%(message)s')
 
    if len(args) == 1:
        folder = "."
    elif len(args) == 2:
        folder = args[1]

    workPath = os.path.abspath(folder)
    mrv = makerunview.MakeRunView(workPath)

    logging.info("Running makeRunView on " + workPath)

    run(mrv, workPath)

readArgsAndRun()
