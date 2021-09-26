from livereload import Server, shell

def buildjs():
      shell('parcel build src/main.js --no-minify', output="dist/logparcel")()
      print(">>> exec parcel build src/main.js --no-source-maps --no-minify")
      with open("dist/logparcel") as file:
        for line in file:
          print(line)

def buildhtml():
      """基于index.html创建新html，并在结束的时候删除"""
      pass

# livereload python server
server = Server()

# 能够输入html，解析html中的js，监听这些，以及其他输入js或目录的变化吗
server.watch("*.html")
# server.watch("src/*.js", buildjs)
server.watch("src/", buildjs)

buildjs()
buildhtml()
server.serve(host='localhost', liveport=35729,
    open_url_delay=1, default_filename='index.html', 
    root=".")

"""
request
- livereload
- parcel

js bundler
- rollupjs
- parceljs
  - from react jsx? https://v2.parceljs.org/recipes/react/
  - await feature? not support now. https://github.com/parcel-bundler/parcel/issues/4028

hot reload:
- liverreload
- hmr
  - `基于node` react hot loader
  - `基于node` https://www.parceljs.cn/hmr.html

how debug?
vs https://blog.logrocket.com/benchmarking-bundlers-2020-rollup-parcel-webpack/
"""