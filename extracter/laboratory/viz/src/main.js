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