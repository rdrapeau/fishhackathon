import atexit
import binascii
from subprocess import Popen, PIPE
import os
import os.path
import sysimport numpy as np
import cv2

myDir = os.path.dirname(os.path.realpath(__file__))
os.environ['TERM'] = 'linux'

class NeuralNet:
    def __init__(self, model, imgDim=96, cuda=False, layer=1, gpu=1):
        assert model is not None
        assert imgDim is not None
        assert cuda is not None
        assert layer is not None
        assert gpu is not None

        self.cmd = ['th', os.path.join(myDir, 'torch_server.lua'),
                    '-model', model, '-imgDim', str(imgDim), '-gpuSelect', str(gpu), '-layer', str(layer)]
        if cuda:
            self.cmd.append('-cuda')
        self.p = Popen(self.cmd, stdin=PIPE, stdout=PIPE,
                       stderr=PIPE, bufsize=0)

        def exitHandler():
            if self.p.poll() is None:
                self.p.kill()
        atexit.register(exitHandler)

    def forwardPath(self, imgPath):
        assert imgPath is not None

        rc = self.p.poll()
        if rc is not None and rc != 0:
            raise Exception("""