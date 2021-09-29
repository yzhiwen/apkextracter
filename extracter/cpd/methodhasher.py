from .factory import ClazzMethodTokenFactory
from .factory import SnippetMethodFactory

class MethodHasher:

    @staticmethod
    def methodhash(method, minitokens:int):
        methodHashMap = {} # <int`sub method tokens`, hashset`sub method tokens hash`>
        tokens = method.tokens
        n = len(tokens)
        r = ClazzMethodTokenFactory.R()
        q = ClazzMethodTokenFactory.Q()
        valueof = ClazzMethodTokenFactory.valueof

        def onSnippetHash(start, len, hash):
            SnippetMethodFactory.snippetMethod(method, start, len, hash)

        m = minitokens # m:`patten length`
        if(m > n): return methodHashMap
        rm = ClazzMethodTokenFactory.RM(r, m, q)
        rkhashset = MethodHasher.rkhash(tokens, m, n, r, rm, q, valueof, onSnippetHash) # O(n) time
        methodHashMap[m] = rkhashset
        return methodHashMap
    
    @staticmethod
    def rkhash(tokens, m, n, R, RM, Q, valueof, onSnippetHash):
        assert m <= n
        assert callable(valueof)
        
        rkhashset = set()

        hash = 0
        for i in range(m):
            hash = (hash * R + valueof(tokens[i])) % Q
        rkhashset.add(hash)
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

            rkhashset.add(hash)
            if callable(onSnippetHash):
                onSnippetHash(i+1, m, hash)
        return rkhashset
    pass