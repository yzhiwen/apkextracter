import time
from .smaliwalker import SmalierWalker
from .methodhasher import MethodHasher
from .snippetwalker import SnippetWaler
from .factory import ClazzFactory, ClazzMethodFactory

class Cpder:
    def startup(self, path, packageref, minitokens=100):
        start = time.time()
        ler = SmalierWalker(packageref)
        ler.startup(path)
        smalierWalkerTime = time.time() - start

        start = time.time()
        MethodHasher.startup(minitokens)
        methodWalkerTime = time.time() - start

        start = time.time()
        hashWalker = SnippetWaler()
        hashWalker.startup()
        hashWalkerTime = time.time() - start

        print("class total: ", str(ClazzFactory.clazzCount()))
        print("method total: ", str(ClazzMethodFactory.methodCount()))
        print("smali file walker time: ", str(smalierWalkerTime))
        print("method hash time: ", str(methodWalkerTime))
        print("hash walker time: ", str(hashWalkerTime))
        pass
    pass