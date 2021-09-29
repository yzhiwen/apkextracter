import time
from .smaliwalker import SmalierWalker
from .methodhasher import MethodHasher
from .hashwalker import HashWaler
from .factory import ClazzFactory, ClazzMethodFactory

class Cpder:
    def startup(self, path):
        start = time.time()
        ler = SmalierWalker()
        ler.startup(path)
        smalierWalkerTime = time.time() - start

        start = time.time()
        MethodHasher.startup(minitokens=70)
        methodWalkerTime = time.time() - start

        start = time.time()
        hashWalker = HashWaler()
        hashWalker.startup()
        hashWalkerTime = time.time() - start

        print("class total: ", str(ClazzFactory.clazzCount()))
        print("method total: ", str(ClazzMethodFactory.methodCount()))
        print("smali file walker time: ", str(smalierWalkerTime))
        print("method hash time: ", str(methodWalkerTime))
        print("hash walker time: ", str(hashWalkerTime))
        pass
    pass