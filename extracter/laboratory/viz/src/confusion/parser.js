import Node from './model.js'

function parse(file, callback) {
    let start = performance.now();
    let root = new Node("apk");
    if (!file) file = "static/_douyin";
    d3.text(file).then(function(dataset) {
        let list = d3.csvParseRows(dataset, (d, i) =>
            // { return null; });
            { return parseLine(d); });
        list.shift();
        for (const item of list) { // not for(cost item in list)
            if (item.fRawPrivateCount === 0 && item.mRawPrivateCount === 0) {
                continue;
            }

            if (item.clazz.indexOf("R") != -1) {
                continue;
            }
            root.build(item);
        }
        console.log("cost is", `${performance.now() - start}ms`);
        callback(root);
    });
}

function parseLine(d) {
    return {
        fRawPrivateCount: parseInt(d[0], 10),
        fPrivateCount: parseInt(d[1], 10),
        fCount: parseInt(d[2], 10),
        mRawPrivateCount: parseInt(d[3], 10),
        mPrivateCount: parseInt(d[4], 10),
        mCount: parseInt(d[5], 10),
        clazz: d[6].substring(1, d[6].length - 1)
    };
}

export { parse };