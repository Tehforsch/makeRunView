import os
from pyinotify import WatchManager, Notifier, ThreadedNotifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_CLOSE_WRITE
import logging

class Observer:
    """Monitor files and notify the main program when changes happen"""
    def __init__(self, makeRunView):
        self.wm = WatchManager()
        self.eh = EventHandler(makeRunView)
        self.notifier = ThreadedNotifier(self.wm, self.eh)
        self.notifier.start()
        # Watched events
        self.mask = IN_DELETE | IN_CREATE | IN_CLOSE_WRITE

    def addFile(self, fname):
        wdd = self.wm.add_watch(fname, self.mask, rec=True)
        logging.info("Observer now watches " + fname)

class EventHandler(ProcessEvent):
    def __init__(self, makeRunView):
        self.makeRunView = makeRunView
        self.doNotify = True

    def process_IN_CREATE(self, event):
        pass

    def process_IN_CLOSE_WRITE(self, event):
        self.makeRunView.notifyChanged(event.pathname)

    def process_IN_DELETE(self, event):
        pass
