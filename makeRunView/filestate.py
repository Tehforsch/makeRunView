import config, os, logging
import utils.fileUtils

class FileState:
    def __init__(self, fname):
        self.fname = fname
        assert(self.fname[0] == "/") # All paths should be absolute.
        self.successors = []
        self.fileType = utils.fileUtils.getFileType(fname)
        # self.fileName = tools.getFileName(fname)
        self.fileName = fname

    def readlines(self):
        # First check if this file actually exists, which might not be the case
        # if not os.path.isfile(self.fname):
            # return None
        # try:
        with open(self.fname, "r") as f:
            lines = f.readlines()
            return lines
        return ""

    def shouldBeObserved(self):
        return self.fileType in config.fileTypesToWatch

    def __str__(self):
        return "<" + self.fileName + ">"