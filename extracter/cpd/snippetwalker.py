from .factory import SnippetMethodFactory

class SnippetWaler:

    def startup(self):
        SnippetMethodFactory.inflateAllSnippet()
        inflatable = SnippetMethodFactory.inflatable
        hashdataset = SnippetMethodFactory.HASHDATASET
        for snippettokenlen, dataset in hashdataset.items():
            for hash, snippets in dataset.items():
                _snippets = [snippet for snippet in snippets if not inflatable(snippet)]
                if len(list(_snippets)) <= 1: continue
                for snippet in _snippets:
                    print(snippet.method.clazz.file)
                print("with tokens number:", str(snippettokenlen))
                # print(_snippets[0].tokenstr())
                print()
            pass
    pass