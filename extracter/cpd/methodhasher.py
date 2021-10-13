from .factory import ClazzMethodFactory
from .factory import ClazzMethodTokenFactory
from .factory import SnippetMethodFactory

class MethodHasher:

    @staticmethod
    def startup(minitokens):
        """hash all method"""
        methods = ClazzMethodFactory.CLAZZMETHODMAP
        for method in methods:
            MethodHasher.methodhash(method, minitokens)
        pass

    @staticmethod
    def methodhash(method, minitokens:int):
        tokens = method.tokens
        n = len(tokens)
        m = minitokens # m:`patten length`
        if(m > n): return
        
        r = ClazzMethodTokenFactory.R()
        q = ClazzMethodTokenFactory.Q()
        rm = ClazzMethodTokenFactory.RM(r, m, q)
        valueof = ClazzMethodTokenFactory.valueof

        def onSnippetHash(start, len, hash):
            SnippetMethodFactory.snippetMethod(method, start, len, hash)

        MethodHasher.rkhash(tokens, m, n, r, rm, q, valueof, onSnippetHash) # O(n) time
    
    @staticmethod
    def rkhash(tokens, m, n, R, RM, Q, valueof, onSnippetHash):
        assert m <= n
        assert callable(valueof)
        
        hash = 0
        for i in range(m):
            hash = (hash * R + valueof(tokens[i])) % Q
        if callable(onSnippetHash): 
            onSnippetHash(0, m, hash)

        for i in range(n-m):
            # leading digit
            leading = valueof(tokens[i])
            # remove leading digit
            hash = (hash - leading * RM % Q + Q) % Q
            # trailing digit
            trailing = valueof(tokens[m+i])
            # add trailing digit
            hash = (hash*R + trailing) % Q

            if callable(onSnippetHash):
                onSnippetHash(i+1, m, hash)
        pass
    pass