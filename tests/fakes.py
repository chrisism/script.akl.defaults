import os
import random 

from akl.utils import io
from akl.executors import ExecutorABC
from akl.utils.kodi import ProgressDialog

def random_string(length:int):
    return ''.join(random.choice([chr(i) for i in range(ord('a'),ord('z'))]) for _ in range(length))

class FakeFile(io.FileName):

    def __init__(self, pathString, isdir=False):
        self.fakeContent  = ''
        self.path_str     = pathString
        self.path_tr      = pathString       

        self.exists = self.exists_fake
        self.write = self.write_fake

    def setFakeContent(self, content):
        self.fakeContent = content
        
    def getFakeContent(self):
        return self.fakeContent   

    def loadFileToStr(self, encoding = 'utf-8'):
        return self.fakeContent     

    def readAllUnicode(self, encoding='utf-8'):
        contents = self.fakeContent
        return contents

    def saveStrToFile(self, data_str, encoding = 'utf-8'):
        self.fakeContent = data_str       

    def write_fake(self, bytes):
        self.fakeContent = self.fakeContent + bytes

    def open(self, mode):pass
    def close(self): pass
    
    def makedirs(self): pass
    
    def getDirAsFileName(self):
        return FakeFile(self.getDir())
    
    def writeAll(self, bytes, flags='w'):
        self.fakeContent = self.fakeContent + bytes


    def pjoin(self, path_str, isdir = False):
        child = FakeFile(os.path.join(path_str, self.path_str),isdir)
        child.setFakeContent(self.fakeContent)
        return child      

    def changeExtension(self, targetExt):
        switched_fake = super(FakeFile, self).changeExtension(targetExt)
        switched_fake = FakeFile(switched_fake.getPath())
        
        switched_fake.setFakeContent(self.fakeContent)
        return switched_fake

    def exists_fake(self):
        return True

    def scanFilesInPathAsFileNameObjects(self, mask = '*.*'):
        return []
    
class FakeExecutor(ExecutorABC):
    
    def __init__(self):
        self.actualApplication = None
        self.actualArgs = None
        self.actualKwargs = None
        super(FakeExecutor, self).__init__(None)
        
    def getActualApplication(self):
        return self.actualApplication

    def getActualArguments(self):
        return self.actualArgs

    def getActualKwargs(self):
        return self.actualKwargs

    def execute(self, application, *args, **kwargs):
        self.actualApplication = application
        self.actualArgs = list(args)
        self.actualKwargs = dict(kwargs)
        pass        

class FakeProgressDialog(ProgressDialog):
    def startProgress(self, message, num_steps = 100):pass
    def updateProgress(self, step_index, message = None):pass
    def updateMessage(self, message):pass
    def isCanceled(self): return False
    def close(self): pass
    def endProgress(self): pass
    def reopen(self): pass