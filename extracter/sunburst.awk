

# labels,ids,filesizes,zipsizes,zipmethods

BEGIN {
    init()
}

END	{
    outputNode2CSV()
}

NF == 10 {
    fileSize=$4
    fileZipSize=$6
    fileCompressMethod=$7
    filePath=$10

    # if(filePath ~ /\.dex$/) { #.dex结果
    #     parseDex()
    # } else if (filePath ~ /\.so$/) {
    #     # print
    #     parseFile()
    # } else {
    #     parseFile()
    # }
    # parseFile()
}

NF == 10 && $10 ~ /\.jpg$|\.jpeg$/ {
    print 
}

##### init some struct
##### @filed _files: list<path>
##### @filed _nodes: map<path,filed>
function init() {
    _files["apk"] = "apk"
    _nodes["apk", "id"] = "apk"
    _nodes["apk", "pid"] = ""
    _nodes["apk", "label"] = "/"
    _nodes["apk", "filesize"] = 0
    _nodes["apk", "zipsize"] = 0
    _nodes["apk", "filetype"] = "d" # in ["d", "-"]
}

function parseFile() {
    i=1
    path="apk"
    len=split(filePath, paths, "/")
    while(i <= len) {
        label = paths[i]
        parent = path
        path = sprintf("%s/%s", path, label)
        filetype = i == len ? "-" : "d"
        saveNode(label, path, parent, fileSize, fileZipSize, fileCompressMethod, filetype)
        i++
    }
}

function parseDex() {
    label = filePath
    parent = "dex"
    path = filePath
    filetype = "-"
    saveNode(label, path, parent, fileSize, fileZipSize, fileCompressMethod, filetype)
}

function saveNode(label, path, parent, filesize, zipsize, fileCompressMethod, filetype) {
    # printf("_save %s,%s,%s,%s,%s,%s,%s\n", label, path, parent, filesize, zipsize, fileCompressMethod, filetype)

    _files[path] = path
    _node[path, "id"] = path
    _node[path, "pid"] = parent
    _node[path, "label"] = label
    _node[path, "zipsize"] += zipsize
    _node[path, "filesize"] += filesize
    _node[path, "filetype"] = filetype
}

function outputNode2CSV() {
    print "ids,pids,labels,zipsizes,filesizes,filetypes" > "apk.csv"
    for(path in _files) {
        id = _node[path, "id"]
        pid = _node[path, "pid"]
        label = _node[path, "label"]
        zipsize = _node[path, "zipsize"]
        filesize = _node[path, "filesize"]
        filetype = _node[path, "filetype"]
        print id "," pid "," label "," zipsize "," filesize "," filetype > "apk.csv"
        # printf("%s,%s,%s,%s\n", id, pid, label, zipsize,  parentName, fileZipSize, compressMethod) > "apk.csv"
    }
}

function test() {
    # other struct
    # _apk["label"] = "/"
    # _dirs["/"] = _apk # illegal reference to array _apk

    # _dirs["/", "label"] = "/"
    # for(value in _dirs) print value, _dirs[value] # /label /
    # for((id, key) in _dirs) print id, key # 不支持

    # len=split(path, paths, "/")
    # for(value in paths) { } // for n ... 1

    # https://stackoverflow.com/questions/12349546/awk-issue-return-an-array-from-user-defined-function
    # return _ref
}