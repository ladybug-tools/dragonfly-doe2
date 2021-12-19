
import fileblocks as fb


class InpFile(object):
    """ A standard blank *.inp File with all file blocks """

    def __init__(self, host):
        self.host = None
        self.out_file = None

    @property
    def file_start(self):
        return self._make_file_start()

    @staticmethod
    def _make_file_start(_objs=None):
        # TODO:  Make this not hard coded
        block = fb.topLevel+fb.abortDiag+fb.globalParam+fb.ttrpddh + \
            'TITLE\n   LINE-1          = *simple_example*\n   ..\n\n' + \
            '"Entire Year" = RUN-PERIOD-PD\n  BEGIN-MONTH     = 1\n  ' + \
            'BEGIN-DAY      =1'
