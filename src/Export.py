from shutil import copyfile

class Export:
    def __init__(self, db_name, filetype, filename):
        self.filetype = filetype
        self.filename = filename
        self.db_name = db_name

    def scan(self):
        copyfile(self.db_name, "%s.%s" % (self.filename, self.filetype))
        pass
