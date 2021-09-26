import { parse } from "./confusion/parser.js"
import ConfusionBar from "./confusion/confusion.js"

parse("static/_douyin", onDataReady);

let bar = new ConfusionBar();

bar.setBarClickCallback((data) => {
    onBuildBar(data);
})

function onDataReady(data) {
    onBuildBar(data);
}

function onBuildBar(root) {
    if (!root || !root.children || root.children.length === 0) return;
    let list = root.children.sort((a, b) => b.value - a.value)
    bar.build(list);
}

let list = ["a", "b", "c"]
d3.select(".sidebar")
    .append("div")
    .style("display", "flex")
    .style("flex-direction", "column")
    .style("align-items", "center")
    .style("justify-content", "center")
    .selectAll("div")
    .data(list)
    .enter()
    .append("div")
    .style("width", "100%")
    .style("align", "center")
    .on("click", function(event, item) { onSideItemClick(item); })
    .append("p")
    .text(d => d)


function onSideItemClick(item) {
    console.log(item);
}