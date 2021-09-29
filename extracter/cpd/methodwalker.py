import collections
from .factory import ClazzMethodFactory
from .methodhasher import MethodHasher

class MethodWalker:
    def startup(self, minitokens):
        methods = ClazzMethodFactory.CLAZZMETHODMAP
        for method in methods:
            method.methodhash = MethodHasher.methodhash(method, minitokens)
        pass

    def groupbylen(self):
        methods = ClazzMethodFactory.CLAZZMETHODMAP
        group = {} # <int`methodstrlen`, list<ClazzMethod>>
        for method in methods:
            methodlen = len(method.tokens)
            if methodlen not in group: group[methodlen] = []
            group[methodlen].append(method)
        return group

    def medianMethodLen(self):
        group = self.groupbylen()
        median = -1
        maxHeight = -1
        for methodlen, methodlist in group.items():
            height = len(methodlist)
            if height > maxHeight:
                maxHeight = height
                median = methodlen
        return median

    def printMedianMethod(self):
        median = self.medianMethodLen()
        print("media ", str(median) + "\n")
        group = self.groupbylen()
        group = collections.OrderedDict(sorted(group.items()))
        for methodlen, methodlist in group.items():
            if(methodlen == median):
                for method in methodlist:
                    print(method.methodstr)
                    pass
                break

    def printMedianMethodLen(self):
        median = self.medianMethodLen()
        print("media ", str(median) + "\n")
        pass
    
    def printAllMethodGroup(self):
        group = self.groupbylen()
        group = collections.OrderedDict(sorted(group.items()))
        for methodlen, methodlist in group.items():
            print(methodlen)
            print(len(methodlist))
            print()
        pass

    def printAllMethodHash(self):
        methods = ClazzMethodFactory.CLAZZMETHODMAP
        for method in methods:
            print(method.methodhash)
            print()
        pass