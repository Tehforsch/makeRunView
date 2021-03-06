import os
from pyinotify import WatchManager, Notifier, ThreadedNotifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_CLOSE_WRITE, IN_CLOSE_NOWRITE
import logging

class Observer:
    """Monitor files and notify the main program when changes happen"""
    def __init__(self, makeRunView):
        self.wm = WatchManager()
        self.eh = EventHandler(makeRunView)
        self.notifier = ThreadedNotifier(self.wm, self.eh)
        self.notifier.start()
        # Watched events
        self.filemask = IN_CLOSE_WRITE
        self.foldermask = IN_CLOSE_WRITE 

    def kill(self):
        status = self.notifier.stop()
        logging.debug("Observer shut down")
        return status

    def addFile(self, fname):
        wdd = self.wm.add_watch(fname, self.filemask, rec=True)

    def addFolder(self, foldername):
        pass
        # self.wm.add_watch(foldername, self.foldermask, rec=True)

class EventHandler(ProcessEvent):
    def __init__(self, makeRunView):
        self.makeRunView = makeRunView
        self.doNotify = True

    def process_IN_CLOSE_WRITE(self, event):
        self.makeRunView.notifyChanged(event.pathname)

    def process_IN_DELETE(self, event):
        pass
