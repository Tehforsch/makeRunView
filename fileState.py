import ownUtils, config, os

class FileState:
    def __init__(self, fname):
        self.fname = fname
        assert(self.fname[0] == "/") # All paths should be absolute.
        self.successors = []
        self.fileType = ownUtils.getFileType(fname)

    def readlines(self):
        # First check if this file actually exists, which might not be the case
        if not os.path.isfile(self.fname):
            return None
        f = open(self.fname, "r")
        lines = f.readlines()
        f.close()
        return lines

    def shouldBeObserved(self):
        return self.fileType in config.fileTypesToWatch
