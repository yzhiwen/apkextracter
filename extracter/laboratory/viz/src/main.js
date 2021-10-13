import { parse } from "./confusion/parser.js"
import ConfusionBar from "./confusion/confusion.js"
import ConfusionTable from "./confusion/table.js"

parse("dist/staticfile", onDataReady);

let table = new ConfusionTable();
let bar = new ConfusionBar();
bar.setBarClickCallback((data) => {
    onBuildBar(data);
})

function onDataReady(data) {
    onBuildBar(data);
}

function onBuildBar(root) {
    console.log(root);
    if (!root) return;

    let list = root.getChildrenList();
    if (!list || list.length === 0) return;

    bar.build(list);
    if (tip === null) tip = d3.select("#my_dataviz").append("div");
    tip
        .style("width", "60%")
        .style("padding", "10px")
        .text(root.clazz)
        .on("click", function() {
            onBuildBar(root.parent)
        })
    table.build(root);
}

let tip = null;