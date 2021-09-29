class Clazz:
    def __init__(self, file):
        self.file = file
        self.method = []

    def addMethod(self, method):
        self.method.append(method);
    pass

class ClazzMethod:
    def __init__(self, clazz: Clazz, methodstr:str):
        self.clazz = clazz
        self.clazz.addMethod(self)
        self.methodstr = methodstr
        self.tokens = methodstr.split(" ")
    pass

class SnippetMethod:
    def __init__(self, method: ClazzMethod, start, len, hash):
        self.method = method
        self.start = start
        self.len = len
        self.hash = hash
        self.inflated = False
    
    def tokens(self):
        if(self.method is None): return []
        methodtokens = self.method.tokens
        if methodtokens is None or len(methodtokens) == 0: return []
        return methodtokens[self.start: self.start+self.len]
    
    def tokenstr(self):
        return " ".join(self.tokens())
        # return str(self.tokens())
    pass