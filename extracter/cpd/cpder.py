import time
from .smaliwalker import SmalierWalker
from .methodwalker import MethodWalker
from .hashwalker import HashWaler
from .factory import ClazzFactory, ClazzMethodFactory

class Cpder:
    def startup(self, path):
        start = time.time()
        ler = SmalierWalker()
        ler.startup(path)
        smalierWalkerTime = time.time() - start

        start = time.time()
        methodWalker = MethodWalker()
        methodWalker.startup(minitokens=70)
        methodWalkerTime = time.time() - start

        start = time.time()
        hashWalker = HashWaler()
        hashWalker.startup()
        hashWalkerTime = time.time() - start

        print("total class: ", str(ClazzFactory.clazzCount()))
        print("total method: ", str(ClazzMethodFactory.methodCount()))
        print("smalier walker time: ", str(smalierWalkerTime))
        print("method walker time: ", str(methodWalkerTime))
        print("hash walker time: ", str(hashWalkerTime))
        pass
    pass